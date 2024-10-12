import os
from os import path
import pandas as pd
from visualization.weighted_graph import prepare_weighted_graph, plot_weighted_graph
from visualization.sankey import prepare_sankey_data, plot_sankey
from flask import Flask, send_from_directory, jsonify, request, render_template

app = Flask(__name__, static_folder='static')


@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/graphs')
def graphs():
    return render_template('graphs.html')


@app.route('/attributes')
def attributes():
    return render_template('attributes.html')

@app.route('/get_attributes', methods=['GET'])
def get_attributes():
    dataset_name = request.args.get('dataset')
    try:
        data = pd.read_csv(f'datasets/attributes/{dataset_name}.csv', header=None)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found for the given date, type, and dataset"}), 404
    feature = data[0].tolist()
    attr = data[1].tolist()
    return jsonify({
        'feature': feature,
        'attr': attr
    })


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


@app.route('/get-csv-dates', methods=['GET'])
def get_csv_dates():
    dataset_name = request.args.get('dataset')
    base_dir = path.join('results', f'cleaned_data_{dataset_name}')
    apriori_dir = path.join(base_dir, 'APRIORI')
    gsp_dir = path.join(base_dir, 'GSP')

    def get_csv_files(dir_path):
        if not os.path.exists(dir_path):
            return []
        return [
            f"{file.split('_')[0]}_{file.split('_')[1]}"
            for file in os.listdir(dir_path)
            if file.endswith('.csv')
        ]

    apriori_dates = get_csv_files(apriori_dir)
    gsp_dates = get_csv_files(gsp_dir)
    all_dates = list(set(apriori_dates + gsp_dates))
    all_dates.sort()
    return jsonify({
        'dates': all_dates,
    })
