import numpy as np
import scipy.special as sc
from numba.types import int32, int64, float64
from numba.experimental import jitclass
from numba import njit, prange

from claravy.ibcc.annotator import ConfusionMatrixAnnotator
from claravy.ibcc.utils import unique, psi_0d, psi_1d

spec = [
    ("scan_labels", int64[:]),
    ("scan_offsets", int64[:]),
    ("beta0", float64[:]),
    ("L", int64),
    ("n_jobs", int64),
    ("C", int32[:, :]),
    ("A", ConfusionMatrixAnnotator.class_type.instance_type),
    ("N", int64),
    ("lnB", float64[:]),
    ("Et", float64[:]),
]

@jitclass(spec)
class IndependentLabelModel:

    def __init__(self, scan_labels, scan_offsets, beta0, L, n_jobs):
        """
        Estimate B, the probability of each family. Also, estimate Et, the
        expecation of the posterior.

        Arguments:
        scan_labels -- Encodes a mapping between scan reports and the set of
                       malware families within those reports
        scan_offsets -- An array of length N mapping from each scan its set of
                        families in co_occurs
        beta0 -- The Dirichlet prior for B, the probability of each label
        L -- The number of malware families
        n_jobs -- The number of threads to use
        """

        self.scan_labels = scan_labels
        self.scan_offsets = scan_offsets
        self.beta0 = beta0
        self.L = L
        self.n_jobs = n_jobs


    def init_t(self, C, A):
        """Initialize Et. For each VirusTotal scan, the corresponding entry in
        Et is initialized to the percent of votes for each family in the scan.

        Arguments:
        C -- The annotations
        A -- A ConfusionMatrixAnnotator object
        """

        self.C = C
        self.A = A
        self.N = C.shape[0]

        # lnB stores the log probabilities of each family
        # Initialize lnB using beta0
        self.lnB = psi_1d(self.beta0) # (L)
        beta0_sum = psi_0d(np.sum(self.beta0))
        self.lnB -= beta0_sum

        # For each VirusTotal scan, we initialize the corresponding entry in Et
        # using the percent of the vote that each family recieved
        self.Et = np.zeros(self.scan_labels.shape[0], dtype=np.float64)

        # Iterate over each VirusTotal scan
        for scan_idx in range(self.N):
            scan = C[scan_idx]

            # To avoid using a ragged array, scan_labels (the mapping from
            # each to the set of families in that scan) is stored as a large
            # 1D array.

            # This gets the index in scan_labels where the current scan begins
            start_off = self.scan_offsets[scan_idx]

            # And this gets the index where the next scan begins
            end_off = self.scan_offsets[scan_idx+1]

            # Count how many votes there are for each family
            labels = self.scan_labels[start_off:end_off]
            vals, label_counts = unique(scan[scan != -1])

            # Then, initialize the current entry in Et based on the percentage
            # of the vote each family recieved
            for label_idx, label in enumerate(labels):
                self.Et[start_off+label_idx] = label_counts[label_idx] + 0.01
            self.Et[start_off:end_off] /= np.sum(self.Et[start_off:end_off])

        return self.Et


    def update_B(self):
        """Update lnB, the log probabilities of each family."""
        beta = np.copy(self.beta0)
        self.lnB = p_update_B(self.Et, self.scan_labels, self.scan_offsets,
                              beta, self.N)
        return


    def update_t(self):
        """Update Et, the expectation of the posterior."""
        Elnpi = self.A.read_lnPi(self.C)
        self.Et = p_update_t(Elnpi, self.scan_labels, self.scan_offsets,
                             self.lnB, self.N)
        return self.Et


    def most_likely_labels(self):
        """Compute the most likely families (and their probabilities) for each
        VirusTotal scan report.
        """
        pred_labels = np.zeros(self.N, dtype=np.int32)
        pred_label_probs = np.zeros(self.N, dtype=np.float32)
        for scan_idx in range(self.N):
            start_off = self.scan_offsets[scan_idx]
            end_off = self.scan_offsets[scan_idx+1]
            labels = self.scan_labels[start_off:end_off]
            probs = self.Et[start_off:end_off]
            pred_idx = np.argmax(probs)
            pred_labels[scan_idx] = labels[pred_idx]
            pred_label_probs[scan_idx] = probs[pred_idx]
        return pred_label_probs, pred_labels


@njit(parallel=True)
def p_update_B(Et, scan_labels, scan_offsets, beta, N):
    """Update lnB, the log probabilities of each family, in parallel.

    Arguments:
    Et -- The current expectation of the posterior
    scan_labels -- Encodes a mapping between scan reports and the set of
                   malware families within those reports
    scan_offsets -- An array of length N mapping from each scan its set of
                    families in co_occurs
    beta -- A copy of beta0 that will be updated as the function runs
    N -- The number of VirusTotal scans
    """

    # Iterate over each VirusTotal scan report in parallel
    L = beta.shape[0]
    for scan_idx in prange(N):

        # Iterate over each family in the current VirusTotal scan
        start_off = scan_offsets[scan_idx]
        end_off = scan_offsets[scan_idx+1]
        labels = scan_labels[start_off:end_off]
        probs = Et[start_off:end_off]

        # Update beta using the probability of the current family in the scan
        for label_idx, label in enumerate(labels):
            beta[label] += probs[label_idx]

    # Compute lnB using beta
    lnB = psi_1d(beta)
    lnB -= psi_0d(np.sum(beta, -1))
    return lnB


@njit(parallel=True)
def p_update_t(Elnpi, scan_labels, scan_offsets, lnB, N):
    """Update Et, the expectation of the posterior, in parallel.

    Arguments --
    Elnpi -- The return value of read_lnPi() from the ConfusionMatrixAnnotator
    scan_labels -- Encodes a mapping between scan reports and the set of
                   malware families within those reports
    scan_offsets -- An array of length N mapping from each scan its set of
                    families in co_occurs
    lnB -- The log probabilities of each family
    N -- The number of VirusTotal scans
    """

    # Add lnB to Elnpi
    Et = np.zeros_like(Elnpi)
    for scan_idx in prange(N):
        start_off = scan_offsets[scan_idx]
        end_off = scan_offsets[scan_idx+1]
        for label_idx in prange(start_off, end_off):
            label = scan_labels[label_idx]
            Et[label_idx] = Elnpi[label_idx] + lnB[label]

    # Apply softmax to each row in Et
    for scan_idx in prange(N):
        start_off = scan_offsets[scan_idx]
        end_off = scan_offsets[scan_idx+1]
        Et[start_off:end_off] = np.exp(Et[start_off:end_off])
        Et[start_off:end_off] /= np.sum(Et[start_off:end_off])
    return Et
