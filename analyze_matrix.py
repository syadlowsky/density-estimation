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
    args = parser.parse_args()
    if args.log in ACCEPTED_LOG_LEVELS:
        logging.basicConfig(level=eval('logging.'+args.log))

    return args

args = configure_and_parse_arguments()

P, R = probability_matrix.get_probabilities(c_true)
Xi = shortest_paths.similarity_matrix(np.exp(np.array([-5., 15.])))

for (beta, xi) in Xi:
    regularization_range = tuple([float(x.strip()) for x in args.regularization[1:-1].split(',')])
    alpha_to_c_map = xi.dot(P)
    A = P.T.dot(alpha_to_c_map)
    fig_image = plt.figure()
    plt.imshow(A, extent=[0, 1, 0, 1])
    #fig_image.savefig(string.replace('results/matrix_true_probabilities_shortest_path_beta'+str(beta)+'_reg'+str(reg), '.','_')+'.png')
    fig_dist = plt.figure()
    plt.hist(A[:])
    plt.show()
    # plt.close(fig_image)
