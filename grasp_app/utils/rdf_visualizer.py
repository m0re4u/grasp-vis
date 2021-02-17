import rdflib
from rdflib.extras.external_graph_libs import rdflib_to_networkx_multidigraph
import networkx as nx
import matplotlib.pyplot as plt


def get_pred_type(p):
    PRED_TYPES = ['default', 'lexical']
    if 'denotedBy' in str(p):
        pred_type = 'lexical'
    else:
        pred_type = 'default'

    assert pred_type in PRED_TYPES
    return pred_type

def visualize(g):
    G = rdflib_to_networkx_multidigraph(g)

    # Plot Networkx instance of RDF Graph
    pos = nx.spring_layout(G, scale=2)
    edge_labels = nx.get_edge_attributes(G, 'r')
    nx.draw_networkx_edge_labels(G, pos)
    f = plt.figure(figsize=(90, 90), dpi=80)
    nx.draw(G, with_labels=True, ax=f.add_subplot(111))
    f.savefig("graph.png")