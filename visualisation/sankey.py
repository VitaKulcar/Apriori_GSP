import plotly.graph_objects as go
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
            continue

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
    return fig
