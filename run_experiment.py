from matrix_generators import call_vector, shortest_paths_network_x, probability_matrix, density_vector
import logging
import scipy.io as sio
import numpy as np
import math
import argparse

ACCEPTED_LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'WARN']

def configure_and_parse_arguments():
    parser = argparse.ArgumentParser(description='Find density estimates for links in a network.')
    parser.add_argument('--log', dest='log', nargs='?', const='INFO',
                       default='WARN', help='Set log level (default: WARN)')
    parser.add_argument('--compute-matrices', '-m', dest='compute_dual_matrix',
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

def shortest_path_matrix():
    shortest_path_matrix = shortest_paths_network_x.create_shortest_path_matrix()
    return shortest_path_matrix

def similarity_matrix(beta):
    shortest_paths = shortest_path_matrix()
    beta_type = getattr(beta, "__iter__", None)
    if callable(beta_type):
        return ((b, np.exp(-b*shortest_paths)) for b in beta)
    else:
        return np.exp(-beta*shortest_paths)

args = configure_and_parse_arguments()

if args.simulate_calls:
    c_true = density_vector.density_vector(26589.2, 300)
    y = call_vector.get_counts_in_tower(26589.2, 300)
    sio.savemat('data/y_vector.mat', {'y':y, 'c_true':c_true})
else:
    y = sio.loadmat('data/y_vector.mat')
    c_true = y['c_true']
    y = np.squeeze(np.asarray(y['y']))

if args.compute_dual_matrix:
    Xi = similarity_matrix([0.001, 0.0031, 0.01, 0.031, 0.1, 0.31])
    P = probability_matrix.get_probabilities()
else:
    dual_matrices = sio.loadmat('data/kmatrix.mat')
    P = dual_matrices['p']
    Xi = dual_matrices['xi']
    A = dual_matrices['k']
    alpha_to_c_map = Xi.dot(P)

if args.cross_validation:
    print np.linalg.norm(y)
    n = A.shape[0]
    for reg in np.arange(0.0, 1.0, 0.01):
        indices = np.random.permutation(n)
        hold_out_sets = np.array_split(indices, 10)
        average_norm_error = 0.
        for hold_out_set in hold_out_sets:
            test_idx = indices[hold_out_set]
            training_idx = np.delete(indices, hold_out_set)
            training_A = A[training_idx, :]
            training_y = y[training_idx]
            test_A = A[test_idx, :]
            test_y = y[test_idx]

            train_mat = np.concatenate((training_A, reg*np.eye(n)))
            train_target = np.concatenate((training_y, np.zeros(n)))
            A_inv = np.linalg.pinv(train_mat)
            alpha = A_inv.dot(train_target)
            error = test_A.dot(alpha) - test_y
            norm_error = np.linalg.norm(error,2)
            average_norm_error += np.square(norm_error)
        print "Lambda:", reg, "Total error:", np.sqrt(average_norm_error)
else:
    for (beta, xi) in Xi:
        for reg in np.arange(0.0, 1.0, 0.1):
            alpha_to_c_map = xi.dot(P)
            A = P.T.dot(alpha_to_c_map)
            n = A.shape[0]
            train_mat = np.concatenate((A, reg*np.eye(n)))
            train_target = np.concatenate((y, np.zeros(n)))
            A_inv = np.linalg.pinv(A)
            alpha = A_inv.dot(y)
            c_hat = alpha_to_c_map.dot(alpha)
            r_squared = 1. - (np.square(np.linalg.norm(c_hat - c_true, 2)) / np.square(np.linalg.norm(c_true, 2)))
            print beta, "r^2:", r_squared
