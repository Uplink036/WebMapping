from Node import Node
import plotly.graph_objects as go
import networkx as nx

def plot_nodes(root: Node):
    """
    Plot a graph of the nodes in the graph starting from the root node.
    """
    # Create a directed graph
    G = nx.DiGraph()
    # Add the root node to the graph
    G.add_node(root.get_website())
    # Add the edges to the graph
    add_edges_to_graph(G, root)
    # Create a layout for the graph
    pos = nx.spring_layout(G)
    # Create a list of edges
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    # Create a list of nodes
    node_x = [] 
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    # Create a figure
    fig = go.Figure()
    # Add edges to the figure
    fig.add_trace(go.Scatter(x=edge_x, y=edge_y, mode='lines', line=dict(color='rgb(210,210,210)', width=1)))
    # Add nodes to the figure
    fig.add_trace(go.Scatter(x=node_x, y=node_y, mode='markers', name='nodes', marker=dict(symbol='circle-dot', size=10, color='rgb(0,240,0)', line=dict(color='rgb(50,50,50)', width=1))))
    # Show the figure
    fig.show()

def add_edges_to_graph(G, node: Node):
    """
    Add the edges of the node to the graph.
    """
    for edge in node.get_edges().values():
        G.add_node(edge.get_website())
        G.add_edge(node.get_website(), edge.get_website())
        if not edge.visited:
            edge.visited = True
            add_edges_to_graph(G, edge)
