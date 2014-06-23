from django.db import connection
import pprint
import logging
import networkx as nx
import numpy as np
import os, sys

def create_shortest_path_matrix(weighted=False):
    G = nx.DiGraph()

    logging.info("Loading graph to NetworkX from database...")
    c = connection.cursor()
    c.execute("SELECT l.beg_node_id, l.end_node_id, (CASE WHEN l.link_type="3" THEN 0.0 WHEN l.link_type="4" THEN 0.0 ELSE l.length/l.lane_count END) AS resistance FROM microsim_link l")
    G.add_weighted_edges_from(c.fetchall())

    logging.debug("Road network is strongly connected: %s" % repr(nx.is_strongly_connected(G)))

    logging.info("Computing shortest paths...")
    if weighted:
        sp = nx.all_pairs_dijkstra_path_length(G)
    else:
        sp = nx.all_pairs_shortest_path_length(G)

    logging.info("Converting shortest paths into matrix...")
    c.execute("SELECT ROW_NUMBER() OVER (ORDER BY id), beg_node_id, end_node_id FROM microsim_link")
    links = c.fetchall()
    N_LINKS = len(links)
    shortest_paths = np.zeros((N_LINKS, N_LINKS))
    for col_idx, _, col_end_node in links:
        for row_idx, _, row_end_node in links:
            if col_idx == row_idx:
                continue
            nodes = sp[col_end_node]
            if row_end_node not in nodes:
                shortest_paths[row_idx - 1, col_idx - 1] = float(N_LINKS)
            else:
                shortest_paths[row_idx - 1, col_idx - 1] = nodes[row_end_node]
    logging.info("Shortest path matrix complete.")
    return shortest_paths
