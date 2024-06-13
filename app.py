import pandas as pd
from visualization.weighted_graph import prepare_weighted_graph, plot_weighted_graph
from visualization.sankey import prepare_sankey_data, plot_sankey
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_graphs', methods=['GET'])
def get_graphs():
    date = request.args.get('date')
    data_type = request.args.get('type')
    dataset_name = request.args.get('dataset')

    if not date:
        return jsonify({"error": "Date parameter is required"}), 400

    if not data_type:
        return jsonify({"error": "Data type parameter is required"}), 400

    if not dataset_name:
        return jsonify({"error": "Dataset parameter is required"}), 400

    try:
        data = pd.read_csv(f'results/cleaned_data_{dataset_name}/{data_type}/{date}_rules.csv', header=None)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found for the given date, type, and dataset"}), 404

    rules_ = data[0].tolist()
    conf_ = data[1].tolist()

    nodes, links = prepare_sankey_data(rules_)
    sankey_fig = plot_sankey(nodes, links)

    nodes, edges = prepare_weighted_graph(rules_, conf_)
    weighted_graph_fig = plot_weighted_graph(nodes, edges)

    return jsonify({
        'sankey': sankey_fig,
        'weighted_graph': weighted_graph_fig
    })
