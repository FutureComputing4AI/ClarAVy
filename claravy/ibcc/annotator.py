import copy
import numpy as np
import scipy.special as sc
from numba import jit, njit, prange
from numba.types import int64, float64
from numba.experimental import jitclass

from claravy.ibcc.utils import psi


# Adapted from https://github.com/UKPLab/arxiv2018-bayesian-ensembles/blob/
# master/src/bayesian_combination/annotator_models/cm.py
spec = [
    ("co_occurs", int64[:]),
    ("scan_labels", int64[:]),
    ("label_offsets", int64[:]),
    ("scan_offsets", int64[:]),
    ("alpha0", float64[:, :]),
    ("alpha", float64[:, :]),
    ("lnPi", float64[:, :]),
    ("L", int64),
    ("K", int64),
    ("n_jobs", int64),
]

@jitclass(spec)
class ConfusionMatrixAnnotator:

    def __init__(self, co_occurs, scan_labels, label_offsets, scan_offsets, L,
                 K, n_jobs):
        """Estimate the confusion matrix Pi for each annotator. We assume that
        most malware families don't co-occur within VirusTotal scans, allowing
        a sparse format to be used.

        Arguments:
        co_occurs -- Encodes which malware families co-occur
        scan_labels -- Encodes a mapping between scan reports and the set of
                       malware families within those reports
        label_offsets -- An array of length L mapping from each family to
                         its set of co-occuring families in co_occurs
        scan_offsets -- An array of length N mapping from each scan its set of
                        families in co_occurs
        L -- The number of malware families
        K -- The number of antivirus products
        n_jobs -- The number of threads to use
        """

        self.co_occurs = co_occurs
        self.scan_labels = scan_labels
        self.label_offsets = label_offsets
        self.scan_offsets = scan_offsets
        self.n_jobs = n_jobs
        self.L = L
        self.K = K

        # alpha0 is the initial state of the  Dirichlet prior on the
        # confusion matrix Pi. Entries where two families never co-occur are
        # implicitly 0 due to the sparse format. # Entries representing one
        # family being confused for another are initialized to 1. Entries
        # representing the predicted family being correct are initialized to 2.
        alpha0 = []

        # Iterate over each of the L malware families
        for i in range(L):

            # Each family can co-occur with any number of other families. To
            # avoid a ragged 2D array, we instead store the co-occurring
            # malware families in a large 1D array.

            # This gets the index in self.co_occurs where the current family
            # begins in self.co_occurs
            start_off = self.label_offsets[i]

            # And this gets the index where the next family begins
            end_off = self.label_offsets[i+1]

            # Using list slicing, we get just the elements representing which
            # families co-occur with family i. Note that family i always co-
            # occurs with itself, so this slice has at least length 1.
            co_occur_row = self.co_occurs[start_off:end_off]
            for j in co_occur_row:
                if j == i:
                    alpha0.append(2.0)
                else:
                    alpha0.append(1.0)

        # Repeat alpha0 for each of the K antivirus products
        np_alpha0 = np.array(alpha0, dtype=np.float64)
        self.alpha0 = np_alpha0.repeat(K).reshape((-1, K))
        return


    def update_alpha(self, Et, C):
        """Update alpha, the Dirichlet prior on the confusion matrix Pi.

        Arguments:
        Et -- The current expectation of the posterior
        C -- The annotations
        """
        self.alpha = np.copy(self.alpha0)
        self.alpha = p_update_alpha(C, self.L, self.co_occurs,
                                    self.scan_labels, self.label_offsets,
                                    self.scan_offsets, self.alpha, Et)
        return


    def q_pi(self):
        """Compute ln of the confusion matrix Pi."""
        self.lnPi = p_q_pi(self.L, self.K, self.co_occurs, self.label_offsets,
                           self.alpha)
        return


    def read_lnPi(self, C):
        """Will be called by the IndependentLabelModel class. The return value
        is used to compute the updated expectation of the posterior Et.

        Arguments:
        C -- The annotations
        """
        return p_read_lnPi(C, self.L, self.co_occurs, self.scan_labels,
                           self.label_offsets, self.scan_offsets, self.lnPi)


@njit(parallel=True)
def p_update_alpha(C, L, co_occurs, scan_labels, label_offsets, scan_offsets,
                   alpha, Et):
    """
    Updates alpha using the most recent expectation of the posterior Et.

    Arguments:
    L -- The number of malware families
    K -- The number of antivirus products
    co_occurs -- Encodes which malware families co-occur
    scan_labels -- Encodes a mapping between scan reports and the set of
                   malware families within those reports
    label_offsets -- An array of length L mapping from each family to its set
                     of co-occuring families in co_occurs
    scan_offsets -- An array of length N mapping from each scan its set of
                    families in co_occurs
    alpha -- A copy of alpha0. This will be updated as the function runs
    Et -- The current expectation of the posterior
    """

    # The annotations have shape (N, C), where N is the number of VirusTotal
    # scans, and K is the number of AV products.
    N, K = C.shape

    # Iterate over each AV product in parallel
    for k in prange(K):

        # Iterate over each VirusTotal scan
        for scan_idx in range(N):

            # To avoid using a ragged array, scan_labels (the mapping from
            # each to the set of families in that scan) is stored as a large
            # 1D array.

            # This gets the index in scan_labels where the current scan begins
            start_s_off = scan_offsets[scan_idx]

            # This gets the index in scan_labels where the next scan beigns
            end_s_off = scan_offsets[scan_idx+1]

            # Iterate over each malware family in the current scan
            for label_idx in range(start_s_off, end_s_off):
                label = scan_labels[label_idx]

                # Process annotations that match the current malware family
                if C[scan_idx, k] != label:
                    continue

                # Iterate over families that co-occur with the current one
                co_label = scan_labels[start_s_off]
                co_label_idx = start_s_off
                start_l_off = label_offsets[label]
                end_l_off = label_offsets[label+1]
                for idx in range(start_l_off, end_l_off):
                    if co_occurs[idx] != co_label:
                        continue

                    # Update the entry in alpha for the co-occurring family and
                    # for the current AV product using the entry in Et for the
                    # current scan and the current family
                    alpha[idx, k] += Et[co_label_idx]

                    # Done iterating if we'd move past the scan in scan_offsets
                    co_label_idx += 1
                    if co_label_idx >= end_s_off:
                        break
                    co_label = scan_labels[co_label_idx]

    # When returned, this will be alpha
    return alpha


@jit(nopython=True)
def p_q_pi(L, K, co_occurs, label_offsets, alpha):
    """Compute ln of the confusion matrix Pi in parallel.

    Arguments:
    L -- The number of malware families
    K -- The number of antivirus products
    co_occurs -- Encodes which malware families co-occur
    label_offsets -- An array of length L mapping from each family to its set
                     of co-occuring families in co_occurs
    alpha -- The Dirichlet prior on the confusion matrix Pi
    """

    # Compute sum(alpha) for each family and for each AV product. This would
    # cause a race condition if parallelized, so it is not.
    alpha_sum = np.zeros((L, K), dtype=np.float64)
    for i in range(L):
        start_off = label_offsets[i]
        end_off = label_offsets[i+1]
        for idx in range(start_off, end_off):
            j = co_occurs[idx]
            alpha_sum[j, :] += alpha[idx, :]

    # Compute psi(sum of alpha) for each family and for each AV product.
    psi_alpha_sum = psi(alpha_sum) # (L, K)

    # Compute psi(alpha)
    psi_alpha = psi(alpha) # (?, K)

    # Compute lnPi
    lnPi = np.zeros(alpha.shape, dtype=np.float64)
    for i in range(L):
        start_off = label_offsets[i]
        end_off = label_offsets[i+1]
        for idx in range(start_off, end_off):
            j = co_occurs[idx]
            lnPi[idx, :] = psi_alpha[idx, :] - psi_alpha_sum[j, :]

    return lnPi



@njit(parallel=True)
def p_read_lnPi(C, L, co_occurs, scan_labels, label_offsets, scan_offsets,
                lnPi):
    """The is used to compute the updated expectation of the posterior Et.

    Arguments:
    C -- The annotations
    L -- The number of malware families
    co_occurs -- Encodes which malware families co-occur
    scan_labels -- Encodes a mapping between scan reports and the set of
                   malware families within those reports
    label_offsets -- An array of length L mapping from each family to its set
                     of co-occuring families in co_occurs
    scan_offsets -- An array of length N mapping from each scan its set of
                    families in co_occurs
    lnPi -- The ln of the confusion matrix Pi
    """

    N, K = C.shape
    result = np.zeros_like(scan_labels, dtype=np.float64)

    # Iterate over each scan in parallel
    for scan_idx in prange(N):
        start_s_off = scan_offsets[scan_idx]
        end_s_off = scan_offsets[scan_idx+1]

        # Iterate over each family in the scan
        for label_idx in range(start_s_off, end_s_off):
            label = scan_labels[label_idx]
            co_label = scan_labels[start_s_off]
            co_label_idx = start_s_off
            start_l_off = label_offsets[label]
            end_l_off = label_offsets[label+1]

            # Iterate over each family in the scan, again
            for idx in range(start_l_off, end_l_off):
                if co_occurs[idx] != co_label:
                    continue

                # Iterate over each AV product
                for k in range(K):

                    # If the annotation matches the current label, update
                    # the corresponding entry in the return value
                    if C[scan_idx, k] == label:
                        result[co_label_idx] += lnPi[idx, k]

                # Done iterating if we'd move past the scan in scan_offsets
                co_label_idx += 1
                if co_label_idx >= end_s_off:
                    break
                co_label = scan_labels[co_label_idx]

    return result
