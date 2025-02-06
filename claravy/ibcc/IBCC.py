import os
import sys
import logging
import operator
import numpy as np
from itertools import chain
from joblib import Parallel, cpu_count, effective_n_jobs

from claravy.ibcc.annotator import ConfusionMatrixAnnotator
from claravy.ibcc.labelmodel import IndependentLabelModel

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("ClarAVy")


# Adapted from https://github.com/UKPLab/arxiv2018-bayesian-ensembles/blob/
# master/src/bayesian_combination/bayesian_combination.py
class IBCC:
    def __init__(self, L, K, max_iter=100, eps=1e-3, beta0_factor=1.0,
                 n_jobs=-1, verbose=False):
        """
        L - Number of labels
        K - Number of annotators
        max_iter - Maximum number of Variational Bayes iterations
        eps - Convergence threshold
        beta0_factor - hyperparameter for the label model. This acts as
                       smoothing, so increasing the value of beta0_factor
                       increases the weight of the prior and causes a more
                       random distribution over the labels.
        n_jobs - Number of threads for parallel computation.
        verbose - Print additional information.
        """

        self.L = L
        self.K = K
        self.max_iter = max_iter
        self.eps = eps
        self.beta0_factor = beta0_factor
        self.n_jobs=n_jobs
        self.verbose = verbose
        self.iter = 0

        # Determine how many threads to use
        if n_jobs == -1:
            self.n_jobs = int(effective_n_jobs() / 2)
        os.environ["NUMBA_NUM_THREADS"] = str(self.n_jobs)
        os.environ["NUMEXPR_MAX_THREADS"] = str(self.n_jobs)
        if self.verbose:
            msg = "Running SparseIBCC using {} thread(s)"
            logger.info(msg.format(self.n_jobs))

        # Et and Et_old will have shape (N, L) once initialized
        self.Et = None
        self.Et_old = None


    def fit_predict(self, C):
        """
        Fit Dawid-Skene using Variational Bayes

        C - A matrix of annotations with shape (N, K). Use -1 to indicate where
            the annotations were not provided by a particular annotator.
        """

        # Re-construct annotations without empty scans
        orig_N, K = C.shape
        empty_scan_idxs = []
        for scan_idx in range(orig_N):
            if np.all(C[scan_idx] == -1):
                empty_scan_idxs.append(scan_idx)
        C = np.delete(C, empty_scan_idxs, axis=0)
        N = C.shape[0]
        if self.verbose:
            msg = "Fitting SparseIBCC on {} total scans ({} empty)"
            logger.info(msg.format(orig_N, len(empty_scan_idxs)))

        # Track malware families that co-occur with each other. Each family
        # can co-occur with any number of other families. To avoid a ragged
        # 2D array, we instead store the co-occurring malware families in a
        # large 1D array.
        scan_labels = []
        co_occurs = [set([l]) for l in range(self.L)]
        for i in range(N):
            scan = C[i]
            labels = set(scan[scan != -1])
            scan_labels.append(sorted(labels))
            for label in labels:
                co_occurs[label].update(labels)

        # Define label_offsets as an array of length L, mapping from each
        # family to its set of co-occuring families in co_occurs. We use it to
        # index into co_occurs.
        off = 0
        label_offsets = [0]
        for i in range(self.L):
            co_occurs[i] = sorted(co_occurs[i])
            off += len(co_occurs[i])
            label_offsets.append(off)
        label_offsets = np.array(label_offsets, dtype=np.int64)
        co_occurs = np.array(list(chain.from_iterable(co_occurs)),
                             dtype=np.int64)

        # scan_labels encodes a mapping between scan reports and the set of
        # malware families within those reports. To avoid a ragged 2D array,
        # scan_labels is stored as a large 1D array. We use scan_offsets to
        # index into scan_labels.
        off = 0
        scan_offsets = [0]
        for i in range(N):
            off += len(scan_labels[i])
            scan_offsets.append(off)
        scan_offsets = np.array(scan_offsets, dtype=np.int64)
        scan_labels = np.array(list(chain.from_iterable(scan_labels)),
                               dtype=np.int64)

        # Initialize the label model
        beta0 = np.ones(self.L) * self.beta0_factor
        self.LM = IndependentLabelModel(scan_labels, scan_offsets, beta0,
                                        self.L, self.n_jobs)

        # Initialize the annotator model
        self.A = ConfusionMatrixAnnotator(co_occurs, scan_labels,
                                          label_offsets, scan_offsets, self.L,
                                          self.K, self.n_jobs)

        # Run the Variational Bayes inference loop
        while not self._converged():
            self.Et_old = np.copy(self.Et)
            if self.iter == 0:
                self.Et = self.LM.init_t(C, self.A)
            else:
                self.Et = self.LM.update_t()
            self.LM.update_B()
            self.A.update_alpha(self.Et, C)
            self.A.q_pi()
            self.iter += 1

        # VB has converged or quit -- now, compute the most likely sequence
        if self.verbose:
            msg = "SparseIBCC iteration {}: computing most likely labels..."
            logger.info(msg.format(self.iter))

        # Update Et after the inference loop  so that we get up-to-date values
        # for the posterior. Then, predict the most likely malware families.
        self.Et = self.LM.update_t()
        label_probs, labels = self.LM.most_likely_labels()
        if self.verbose:
            msg = "SparseIBCC iteration {}: fitting/predicting complete."
            logger.info(msg.format(self.iter))

        # We discarded empty scans earlier. Add them back into the correct
        # locations of the posterior. The predicted family for all empty scans
        # is -1, indicating "unknown".
        posterior = []
        i = 0
        j = 0
        for scan_idx in range(orig_N):
            if j < len(empty_scan_idxs) and scan_idx == empty_scan_idxs[j]:
                posterior.append([(-1, 1.0)])
                j += 1
                continue
            start_off = scan_offsets[i]
            end_off = scan_offsets[i+1]
            labels = scan_labels[start_off:end_off]
            probs = self.Et[start_off:end_off]
            scan_posterior = []
            for l, p in list(zip(labels, probs)):
                scan_posterior.append((l, p))
            posterior.append(scan_posterior)
            i += 1

        return posterior, labels, label_probs


    def _converged(self):
        """
        Calculates whether the bayesian_combination has _converged or the
        maximum number of iterations is reached
        """

        # Don't bother to check because some of the variables have not even
        # been initialised yet!
        if self.iter <= 1:
            msg = "SparseIBCC: Completed iteration {}"
            logger.info(msg.format(self.iter))
            return False

        converged = self.iter >= self.max_iter

        # We have not reached max number of iterations yet. Check to see if
        # updates have already converged.
        if not converged:
            diffs = np.abs(self.Et - self.Et_old)
            max_diff = np.max(diffs)

            if self.verbose:
                msg = "SparseIBCC: Max difference at iteration {}: {:.5f}"
                logger.info(msg.format(self.iter, max_diff))

            converged = max_diff < self.eps

        return converged
