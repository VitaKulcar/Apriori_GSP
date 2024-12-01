from collections import defaultdict

import plotly.express as px
import pandas as pd
import numpy as np
from plotly.io import to_json


def parse_rule(rule_str):
    antecedent, consequent = rule_str.split('=>')
    antecedent = [item.strip('{} ') for item in antecedent.split(',')]
    consequent = [item.strip('{} ') for item in consequent.split(',')]
    return antecedent, consequent


def prepare_weighted_graph(rules):
    nodes = []
    links = {"source": [], "target": [], "value": []}
    node_index = {}
    link_counts = defaultdict(int)
    for rule in rules:
        try:
            rule_str = rule.strip()
            antecedent, consequent = parse_rule(rule_str)
            items = antecedent + consequent
            for item in items:
                if item not in node_index:
                    node_index[item] = len(nodes)
                    nodes.append(item)
            for ant in antecedent:
                for cons in consequent:
                    source_idx = node_index[ant]
                    target_idx = node_index[cons]
                    link_counts[(source_idx, target_idx)] += 1
        except ValueError:
            continue

    # aggregated links
    for (source_idx, target_idx), count in link_counts.items():
        links["source"].append(source_idx)
        links["target"].append(target_idx)
        links["value"].append(count)

    return nodes, links


def plot_weighted_graph(nodes, links):
    # Convert Sankey links data into treemap format
    names = []
    parents = []
    values = []

    # Prepare the treemap data using links
    for source_idx, target_idx, count in zip(links["source"], links["target"], links["value"]):
        source_name = nodes[source_idx]
        target_name = nodes[target_idx]

        names.append(target_name)
        parents.append(source_name)
        values.append(count)

    # Add standalone nodes
    for node in nodes:
        if node not in names and node not in parents:
            names.append(node)
            parents.append("")
            values.append(0)

    # Create a dataframe for the treemap
    df = pd.DataFrame({
        'names': names,
        'parents': parents,
        'values': values
    })

    # Define color midpoint for better scaling
    color_continuous_midpoint = (
        np.mean([v for v in df['values'] if v > 0]) if df['values'].sum() > 0 else 0
    )

    # Plot the treemap
    fig = px.treemap(
        df,
        path=['parents', 'names'],
        values='values',
        color='values',
        color_continuous_scale='Blues',
        color_continuous_midpoint=color_continuous_midpoint
    )

    # Enhance the treemap appearance
    fig.update_traces(marker=dict(
        colorscale='Blues',
        colorbar=dict(
            title="Connections",
            ticks="outside",
            len=0.8
        )
    ))
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    return to_json(fig)

