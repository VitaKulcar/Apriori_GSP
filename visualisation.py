import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.sankey import Sankey
import plotly.graph_objects as go


def plot_sankey_like_plotly(sankey_data):
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=15,
            thickness=20,
            label=["A", "B", "C", "D", "E", "F"],
        ),
        link=dict(
            arrowlen=15,
            source=[0, 0, 1, 2, 5, 4, 3, 5],
            target=[5, 3, 4, 3, 0, 2, 2, 3],
            value=[1, 2, 1, 1, 1, 1, 1, 2]
        )
    )])
    fig.show()


def prepare_sankey_data(rules):
    nodes = set()
    links = []
    values = []

    # Parse rules and confidence levels
    for rule, confidence in rules.items():
        antecedent, consequent = rule.split('=>')
        antecedent = antecedent.strip('{}').split(',')
        consequent = consequent.strip('{}').split(',')

        # Add nodes to set
        nodes.update(antecedent)
        nodes.update(consequent)

        # Add links
        for a in antecedent:
            for c in consequent:
                links.append((a, c))
                values.append(confidence)

    # Assign indices to nodes
    node_indices = {node: i for i, node in enumerate(nodes)}

    # Create source, target, and value arrays for links
    sources = [node_indices[link[0]] for link in links]
    targets = [node_indices[link[1]] for link in links]

    return {
        "node": {
            "label": list(nodes),
        },
        "link": {
            "source": sources,
            "target": targets,
            "value": values
        }
}


def parse_rule(rule_str):
    antecedent, consequent = rule_str.split('=>')
    antecedent = [item.strip('{} ') for item in antecedent.split(',')]
    consequent = [item.strip('{} ') for item in consequent.split(',')]
    return antecedent, consequent


def preparation(df):
    weighted_graph_data = []
    sankey_data = {'Source': [], 'Target': [], 'Confidence': []}
    tree_data = []

    for index, row in df.iterrows():
        antecedent, consequent = parse_rule(row['Rule'])
        confidence = float(row['Confidence'])

        # Weighted graph
        for a in antecedent:
            for c in consequent:
                weighted_graph_data.append((a, c, confidence))

        # Sankey diagram
        sankey_data['Source'].extend(antecedent)
        sankey_data['Target'].extend(consequent)
        sankey_data['Confidence'].extend([confidence] * len(antecedent))

        # Tree diagram
        tree_data.append((antecedent, consequent, confidence))
    return tree_data, sankey_data, weighted_graph_data


def plot_tree(tree_data):
    G = nx.DiGraph()

    for antecedent, consequent, confidence in tree_data:
        antecedent_str = ', '.join(antecedent)
        consequent_str = ', '.join(consequent)
        G.add_edge(antecedent_str, consequent_str, weight=confidence)

    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}

    nx.draw(G, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=10, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Tree Diagram")
    plt.show()


def plot_sankey(sankey_data):
    sources = sankey_data['Source']
    targets = sankey_data['Target']
    confidences = sankey_data['Confidence']

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(1, 1, 1, xticks=[], yticks=[])

    sankey = Sankey(ax=ax, scale=0.01)
    flows = [1] * len(sources)
    sankey.add(flows=flows, labels=sources + targets, orientations=[0] * len(sources) + [1] * len(targets),
               facecolor='skyblue', edgecolor='black')

    sankey.finish()

    plt.title("Sankey Diagram")
    plt.show()


def visualize(dataset_name):
    df = pd.read_csv(f'results/{dataset_name}.csv')
    #tree_data, sankey_data, _ = preparation(df)
    # plot_tree(tree_data)
    # plot_sankey(sankey_data)
    sankey_data = prepare_sankey_data(df)
    plot_sankey_like_plotly(sankey_data)
