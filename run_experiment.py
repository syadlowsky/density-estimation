from matrix_generators import call_vector, shortest_paths, probability_matrix, density_vector
import string
import logging
import scipy.io as sio
from scipy.optimize import nnls
import numpy as np
import math
import itertools
import argparse

import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

ACCEPTED_LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'WARN']

def configure_and_parse_arguments():
    parser = argparse.ArgumentParser(description='Find density estimates for links in a network.')
    parser.add_argument('--log', dest='log', nargs='?', const='INFO',
                       default='WARN', help='Set log level (default: WARN)')
    parser.add_argument('--regularization', dest='regularization', nargs='?', const='(0.0, 1.0, 0.1)',
                       default='(0.0, 0.1, 0.1)', help='Set regularization (default: No regularization)')
    parser.add_argument('--compute-matrices', '-m', dest='compute_dual_matrix',
                       const=True, default=False, action='store_const',
                       help='Compute the matrices needed to solve the dual problem instead of loading from file (default: False)')
    parser.add_argument('--compute-p-matrix', '-p', dest='compute_P_matrix',
                       const=True, default=False, action='store_const',
                       help='Compute the matrices needed to solve the dual problem instead of loading from file (default: False)')
    parser.add_argument('--simulate-calls', '-c', dest='simulate_calls',
                       const=True, default=False, action='store_const',
                       help='Simulate calls from microsim instead of loading from file (default: False)')
    parser.add_argument('--cross-validation', '-x', dest='cross_validation',
                       const=True, default=False, action='store_const',
                       help='Do cross validation on dual variables (default: False)')
    args = parser.parse_args()
    if args.log in ACCEPTED_LOG_LEVELS:
        logging.basicConfig(level=eval('logging.'+args.log))

    return args

args = configure_and_parse_arguments()

if args.simulate_calls:
    c_true = density_vector.density_vector(26589.2, 300)
    y = call_vector.get_counts_in_tower(26589.2, 300)
    sio.savemat('data/y_vector.mat', {'y':y, 'c_true':c_true})
    logging.info("Call vector and split vector saved")
else:
    y = sio.loadmat('data/y_vector_full_2.mat')
    c_true = np.squeeze(np.asarray(y['c_true']))
    y = np.squeeze(np.asarray(y['y']))

if args.compute_P_matrix:
    P, R = probability_matrix.get_probabilities(c_true)
    sio.savemat('data/pmatrix.mat', {'P':P, 'R':R})
else:
    p_matrix = sio.loadmat('data/pmatrix.mat')
    P = p_matrix['P']
    R = p_matrix['R']

if args.compute_dual_matrix:
    Xi = shortest_paths.similarity_matrix(np.exp(np.array([-5., 15.])))
else:
    dual_matrices = sio.loadmat('data/ximatrix.mat')
    Xi = dual_matrices['Xi']

for (beta, xi) in Xi:
    regularization_range = tuple([float(x.strip()) for x in args.regularization[1:-1].split(',')])
    alpha_to_c_map = xi.dot(P)
    A = P.T.dot(alpha_to_c_map)
    for reg in np.arange(*regularization_range):
        fig_image = plt.figure()
        plt.imshow(A, extent=[0, 1, 0, 1])
        fig_image.savefig(string.replace('results/matrix_true_probabilities_shortest_path_beta'+str(beta)+'_reg'+str(reg), '.','_')+'.png')
        plt.close(fig_image)
        n = A.shape[0]
        train_mat = np.concatenate((A, reg*np.eye(n)))
        train_target = np.concatenate((y, np.zeros(n)))
        # A_inv = np.linalg.pinv(train_mat)
        # alpha = A_inv.dot(train_target)
        alpha, res = nnls(train_mat, train_target)
        print "Beta:", beta
        print "A*alpha - y:", np.linalg.norm(A.dot(alpha) - y) / np.linalg.norm(y)
        c_hat = alpha_to_c_map.dot(alpha)*P.sum(axis=1)
        r_squared = np.corrcoef(c_hat, c_true)
        print "r^2(c_hat, c_true):", r_squared[0,1]
        sio.savemat('results/c_'+str(beta)+'_'+str(reg)+'.mat', {'c_hat':c_hat, 'c_true':c_true})
        print "norm(c_true):", np.linalg.norm(c_true)
        print "norm(c_hat):", np.linalg.norm(c_hat)
        print "norm(alpha):", np.linalg.norm(alpha)
        fig = plt.figure()
        plt.scatter(c_true, c_hat, marker='x')
        fig.savefig(string.replace('results/true_probabilities_shortest_path_beta'+str(beta)+'_reg'+str(reg), '.','_')+'.png')
        plt.close(fig)
