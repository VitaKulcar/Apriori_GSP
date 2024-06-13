import plotly.express as px
import pandas as pd
import numpy as np
from plotly.io import to_json


def parse_rule(rule_str):
    antecedent, consequent = rule_str.split('=>')
    antecedent = [item.strip('{} ') for item in antecedent.split(',')]
    consequent = [item.strip('{} ') for item in consequent.split(',')]
    return antecedent, consequent


def prepare_weighted_graph(rules, confidences):
    nodes = []
    edges = []
    node_index = {}

    for rule, confidence in zip(rules, confidences):
        try:
            rule_str = rule.strip()
            confidence = float(confidence)  # Ensure confidence is a float

            antecedent, consequent = parse_rule(rule_str)
            items = antecedent + consequent

            # Update nodes and node_index
            for item in items:
                if item not in node_index:
                    node_index[item] = len(nodes)
                    nodes.append(item)

            # Add edges with weights (confidence values)
            for ant in antecedent:
                for cons in consequent:
                    source_idx = node_index[ant]
                    target_idx = node_index[cons]
                    edges.append((source_idx, target_idx, confidence))
        except ValueError:
            continue

    return nodes, edges


def plot_weighted_graph(nodes, edges):
    names = []
    parents = []
    values = []

    for source_idx, target_idx, confidence in edges:
        source_name = nodes[source_idx]
        target_name = nodes[target_idx]

        names.append(target_name)
        parents.append(source_name)
        values.append(confidence)

    # Ensure all nodes are included as root nodes where necessary
    for node in nodes:
        if node not in names and node not in parents:
            names.append(node)
            parents.append("")
            values.append(0)

        # Create a DataFrame for the treemap
    df = pd.DataFrame({
        'names': names,
        'parents': parents,
        'values': values
    })

    # Plot the treemap
    fig = px.treemap(df, path=['parents', 'names'], values='values', color='values',
                     color_continuous_scale='RdBu',
                     color_continuous_midpoint=np.average(df['values'], weights=df['values']))
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return to_json(fig)
