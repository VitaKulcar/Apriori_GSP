import pandas as pd
import plotly.graph_objects as go
import networkx as nx
from collections import defaultdict


def parse_rule(rule_str):
    antecedent, consequent = rule_str.split('=>')
    antecedent = [item.strip('{} ') for item in antecedent.split(',')]
    consequent = [item.strip('{} ') for item in consequent.split(',')]
    return antecedent, consequent


def prepare_sankey_data(rules):
    nodes = []
    links = {"source": [], "target": [], "value": []}
    node_index = {}

    # To aggregate the links by counting the number of connections
    link_counts = defaultdict(int)

    # Parse each rule
    for rule in rules:
        try:
            rule_str = rule.strip()

            antecedent, consequent = parse_rule(rule_str)
            items = antecedent + consequent

            # Update nodes and node_index
            for item in items:
                if item not in node_index:
                    node_index[item] = len(nodes)
                    nodes.append(item)

            # Count links for each pair (antecedent -> consequent)
            for ant in antecedent:
                for cons in consequent:
                    source_idx = node_index[ant]
                    target_idx = node_index[cons]
                    link_counts[(source_idx, target_idx)] += 1
        except ValueError:
            continue  # Skip rows that don't conform to the expected format

    # Prepare aggregated links
    for (source_idx, target_idx), count in link_counts.items():
        links["source"].append(source_idx)
        links["target"].append(target_idx)
        links["value"].append(count)

    return nodes, links


def plot_sankey(nodes, links):
    fig = go.Figure(data=[go.Sankey(
        arrangement='snap',
        node=dict(
            pad=15,
            thickness=20,
            label=nodes,
        ),
        link=dict(
            arrowlen=15,
            source=links["source"],
            target=links["target"],
            value=links["value"]
        )
    )])
    fig.show()


def prepare_weighted_graph(rules, confidences):
    G = nx.DiGraph()

    # Parse each rule and add edges with confidence values
    for rule, confidence in zip(rules, confidences):
        try:
            rule_str = rule.strip()
            confidence = float(confidence)

            antecedent, consequent = parse_rule(rule_str)

            # Add edges for each pair (antecedent -> consequent) with weighted values
            for ant in antecedent:
                for cons in consequent:
                    G.add_edge(ant, cons, weight=confidence)
        except ValueError:
            continue  # Skip rows that don't conform to the expected format

    return G


def plot_weighted_graph(G):
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Create nodes trace
    node_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers',
        marker=dict(
            color='blue',
            size=10
        ),
        text=list(G.nodes())
    )

    # Create edge traces
    edge_traces = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_trace = go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            mode='lines',
            line=dict(width=edge[2]['weight'] * 5, color='gray'),  # Adjust width based on weight
            hoverinfo='none'
        )
        edge_traces.append(edge_trace)

    # Create figure
    fig = go.Figure(data=edge_traces + [node_trace],
                    layout=go.Layout(
                        title='Weighted Graph',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )
    fig.show()


def plot_tree(tree_data):
    fig = go.Figure()

    def add_trace(node, parent_pos=None):
        if 'name' in node:
            fig.add_trace(go.Scatter(
                x=[parent_pos[0], node['pos'][0]] if parent_pos else [],
                y=[parent_pos[1], node['pos'][1]] if parent_pos else [],
                mode='lines+markers',
                line=dict(width=2),
                marker=dict(size=10, color='blue'),
                text=node['name'],
                hoverinfo='text'
            ))
            for child in node.get('children', []):
                add_trace(child, node['pos'])

    add_trace(tree_data)

    fig.update_layout(title='Tree Diagram', showlegend=False,
                      hovermode='closest', xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                      plot_bgcolor='white')

    fig.show()


# Your tree data (similar to Sankey and weighted graph data structure)
tree_data = {
    'name': 'Root',
    'pos': (0, 0),
    'children': [
        {'name': 'Child 1', 'pos': (-1, -1)},
        {'name': 'Child 2', 'pos': (1, -1)},
        {'name': 'Child 3', 'pos': (0, -2), 'children': [
            {'name': 'Grandchild 1', 'pos': (-1, -3)},
            {'name': 'Grandchild 2', 'pos': (1, -3)}
        ]}
    ]
}

# Plot the tree diagram
plot_tree(tree_data)

data = pd.read_csv('results/cleaned_data_oddelki/GSP/2020-11_rules.csv', header=None)
rules_ = data[0].tolist()
conf_ = data[1].tolist()

nodes, links = prepare_sankey_data(rules_)
plot_sankey(nodes, links)

G = prepare_weighted_graph(rules_, conf_)
plot_weighted_graph(G)

################################
