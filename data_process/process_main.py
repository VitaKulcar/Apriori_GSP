import pandas as pd
from data_process.data_preparation import data_cleaning, attributes, generate_sequences
from algorithms.apriori import Apriori
from algorithms.gsp import GeneralizedSequentialPatternMining
from concurrent.futures import ProcessPoolExecutor


def clean_data():
    datasets = [
        ('oddelki', ['ZAVSIFMAT', 'ZAVSIF', 'OBD_SIF', 'KAT_MAT', 'KATEGORIJA', 'DOG_SIF', 'VZROK_SIF']),
        ('ucenci', ['ZAVSIFMAT', 'ZAVSIF', 'OBD_SIF', 'KAT_MAT', 'KATEGORIJA', 'VZROK_SIF']),
        ('zaposleni', ['ZAVSIFMAT', 'ZAVSIF', 'KAT_MAT', 'KATEGORIJA', 'VZROK_SIF', 'DEL_MES_SIF'])
    ]
    for dataset_name, columns_drop in datasets:
        data_cleaning(dataset_name, columns_drop)


def write_attributes():
    dataset_name = ['oddelki', 'ucenci', 'zaposleni']
    for dataset in dataset_name:
        attributes(dataset)


def sequence_to_string(s):
    set_notation = ", ".join(["{" + ", ".join(item) + "}" for item in s])
    return f"{set_notation}"


def save_results(dataset_name, algorithm, dataset_month, frequent_sequences, length):
    dataset_data = {
        'Sequence': [sequence_to_string(k) for k in frequent_sequences.keys()],
        'Support': list(frequent_sequences.values()),
        'Relative Frequency': [support / length for support in frequent_sequences.values()]
    }
    df_freq_sequences = pd.DataFrame(dataset_data)
    df_freq_sequences.to_csv(f"results/cleaned_data_{dataset_name}/{algorithm}/{dataset_month}_frequent_sequences.csv",
                             index=False)


def rule_to_string(rule):
    antecedent, consequent = rule
    antecedent_str = ", ".join(["{" + ", ".join(item) + "}" for item in antecedent])
    consequent_str = ", ".join(["{" + ", ".join(item) + "}" for item in consequent])
    return f"{antecedent_str} => {consequent_str}"


def save_rules(dataset_name, algorithm, dataset_month, rules):
    dataset_data = {
        'Rule': [rule_to_string(k) for k in rules.keys()],
        'Confidence': list(rules.values())
    }
    df_rules = pd.DataFrame(dataset_data)
    df_rules.to_csv(f"results/cleaned_data_{dataset_name}/{algorithm}/{dataset_month}_rules.csv", index=False)


def process_month(dataset_name, dataset_month, dataset_data, min_support, min_confidence, length):
    GSP = GeneralizedSequentialPatternMining(dataset_data, min_support, min_confidence)
    GSP_frequent_sequences = GSP.mine_frequent_sequences()
    GSP_rules = GSP.generate_association_rules(GSP_frequent_sequences)
    save_results(dataset_name, 'GSP', dataset_month, GSP_frequent_sequences, length)
    save_rules(dataset_name, 'GSP', dataset_month, GSP_rules)

    APRIORI = Apriori(dataset_data, min_support, min_confidence)
    APRIORI_frequent_sequences = APRIORI.mine_frequent_itemsets()
    APRIORI_rules = APRIORI.generate_association_rules(APRIORI_frequent_sequences)
    save_results(dataset_name, 'APRIORI', dataset_month, APRIORI_frequent_sequences, length)
    save_rules(dataset_name, 'APRIORI', dataset_month, APRIORI_rules)

    print(f"procesed {dataset_name} {dataset_month}")


def process():
    if __name__ == '__process_main__':
        clean_data()
        write_attributes()

        dataset_names = {
            'oddelki': ['REGIJA', 'OBDOBJE', 'STEV_UCENCEV', 'VZROK', 'TRAJANJE'],
            'ucenci': ['REGIJA', 'OBDOBJE', 'VZROK', 'TRAJANJE'],
            'zaposleni': ['REGIJA', 'DELOVNO_MESTO', 'VZROK', 'TRAJANJE']
        }

        with ProcessPoolExecutor() as executor:
            futures = []
            for name, columns in dataset_names.items():
                sequences = generate_sequences(name, columns)
                for month, data in sequences.items():
                    futures.append(executor.submit(process_month, name, month, data, 0.5, 0.5, len(data)))

        print("All datasets processed.")
