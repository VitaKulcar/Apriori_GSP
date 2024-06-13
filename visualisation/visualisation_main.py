import pandas as pd
from visualisation.weighted_graph import prepare_weighted_graph, plot_weighted_graph
from visualisation.sankey import prepare_sankey_data, plot_sankey
import plotly.io as pio
import webbrowser


def visual():
    data = pd.read_csv('results/cleaned_data_oddelki/GSP/2020-11_rules.csv', header=None)
    rules_ = data[0].tolist()
    conf_ = data[1].tolist()

    nodes, links = prepare_sankey_data(rules_)
    sankey_fig = plot_sankey(nodes, links)

    nodes, edges = prepare_weighted_graph(rules_, conf_)
    weighted_graph_fig = plot_weighted_graph(nodes, edges)

    generate_html(sankey_fig, weighted_graph_fig)

    webbrowser.open('combined_graphs.html')


def generate_html(sankey_fig, weighted_graph_fig):
    # Save figures to HTML strings
    sankey_html = pio.to_html(sankey_fig, full_html=False)
    weighted_graph_html = pio.to_html(weighted_graph_fig, full_html=False)

    # Combine both HTML strings
    combined_html = f"""
    <html>
    <head>
        <title>Combined Graphs</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <h1>Sankey Diagram</h1>
        {sankey_html}
        <h1>Weighted Graph Treemap</h1>
        {weighted_graph_html}
    </body>
    </html>
    """

    # Save the combined HTML to a file
    with open('combined_graphs.html', 'w', encoding='utf-8') as f:
        f.write(combined_html)
