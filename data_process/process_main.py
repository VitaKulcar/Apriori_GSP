import os
from concurrent.futures import ProcessPoolExecutor
from data_process.data_preparation import data_cleaning, generate_sequences, group_data
from data_process.process_algorithms import process_algorithms
from data_process.data_csv_save import attributes


def clean_data():
    datasets = [
        ('oddelki', ['ZAVSIFMAT', 'ZAVSIF', 'OBD_SIF', 'KAT_MAT', 'KATEGORIJA', 'DOG_SIF', 'VZROK_SIF']),
        ('ucenci', ['ZAVSIFMAT', 'ZAVSIF', 'OBD_SIF', 'KAT_MAT', 'KATEGORIJA', 'VZROK_SIF']),
        ('zaposleni', ['ZAVSIFMAT', 'ZAVSIF', 'KAT_MAT', 'KATEGORIJA', 'VZROK_SIF', 'DEL_MES_SIF'])
    ]
    for dataset_name, columns_drop in datasets:
        data_cleaning(dataset_name, columns_drop)


def process_month(dataset_name, dataset_month, dataset_data, min_sup, min_conf, lenght):
    processor = process_algorithms(dataset_name, dataset_month, dataset_data, min_sup, min_conf, lenght)
    processor.process()


def process_file(name, filename):
    if filename.endswith('.csv'):
        group_name = filename.split('.')[0]
        sequences = generate_sequences(name, group_name)
        process_month(name, group_name, sequences, 0.9, 0.9, len(sequences))


def process_sequential():
    clean_data()

    dataset_names = {
        'oddelki': ['REGIJA', 'OBDOBJE', 'STEV_UCENCEV', 'VZROK', 'TRAJANJE'],
        'ucenci': ['REGIJA', 'OBDOBJE', 'VZROK', 'TRAJANJE'],
        'zaposleni': ['REGIJA', 'DELOVNO_MESTO', 'VZROK', 'TRAJANJE']
    }

    for name, columns in dataset_names.items():
        attributes(name, columns)
        group_data(name, columns)

        directory_path = f'datasets/cleaned_data/{name}'
        files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
        for filename in files:
            process_file(name, filename)

    print("All datasets processed sequentially.")


"""def process_concurrent():
    clean_data()

    dataset_names = {
        'oddelki': ['REGIJA', 'OBDOBJE', 'STEV_UCENCEV', 'VZROK', 'TRAJANJE'],
        'ucenci': ['REGIJA', 'OBDOBJE', 'VZROK', 'TRAJANJE'],
        'zaposleni': ['REGIJA', 'DELOVNO_MESTO', 'VZROK', 'TRAJANJE']
    }

    for name, columns in dataset_names.items():
        attributes(name, columns)
        group_data(name, columns)

    # Using ProcessPoolExecutor to process files concurrently
    with ProcessPoolExecutor() as executor:
        futures = []

        for name in dataset_names.keys():
            directory_path = f'datasets/cleaned_data/{name}'
            if not os.path.exists(directory_path):
                print(f"Directory {directory_path} does not exist.")
                continue

            files = [f for f in os.listdir(directory_path) if f.endswith('.csv')]
            for filename in files:
                futures.append(executor.submit(process_file, name, filename))

        # Ensure all processes are completed
        for future in futures:
            future.result()

    print("All datasets processed concurrently.")
"""


def process():
    process_sequential()
    # process_concurrent()
    print("All datasets processed.")
