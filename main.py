import pandas as pd
import data_preparation
from data_preparation import data_cleaning, attributes, generate_sequences
from apriori import Apriori
from gsp import GeneralizedSequentialPatternMining
from visualisation import visualize
from concurrent.futures import ProcessPoolExecutor, as_completed

"""
# priprava podatkov
data_cleaning('oddelki', ['ZAVSIFMAT', 'ZAVSIF', 'OBD_SIF', 'KAT_MAT', 'KATEGORIJA', 'DOG_SIF', 'VZROK_SIF'])
data_cleaning('ucenci', ['ZAVSIFMAT', 'ZAVSIF', 'OBD_SIF', 'KAT_MAT', 'KATEGORIJA', 'VZROK_SIF'])
data_cleaning('zaposleni', ['ZAVSIFMAT', 'ZAVSIF', 'KAT_MAT', 'KATEGORIJA', 'VZROK_SIF', 'DEL_MES_SIF'])

# zapis atributov
attributes('oddelki')
attributes('ucenci')
attributes('zaposleni')

#imamo hierarhične podatke (regija > občina > matični zavod > zavod)
"""


def sequence_to_string(s):
    set_notation = ", ".join(["{" + ", ".join(item) + "}" for item in s])
    return f"{set_notation}"


def save_results(algorithm, frequent_sequences):
    data = {
        'Sequence': [sequence_to_string(k) for k in frequent_sequences.keys()],
        'Support': list(frequent_sequences.values()),
        'Relative Frequency': [support / len(sequences) for support in frequent_sequences.values()]
    }
    df_freq_sequences = pd.DataFrame(data)
    df_freq_sequences.to_csv(f"results/test/{algorithm}_frequent_sequences.csv", index=False)


def rule_to_string(rule):
    antecedent, consequent = rule
    antecedent_str = ", ".join(["{" + ", ".join(item) + "}" for item in antecedent])
    consequent_str = ", ".join(["{" + ", ".join(item) + "}" for item in consequent])
    return f"{antecedent_str} => {consequent_str}"


def save_rules(algorithm, rules):
    data = {
        'Rule': [rule_to_string(k) for k in rules.keys()],
        'Confidence': list(rules.values())
    }
    df_rules = pd.DataFrame(data)
    df_rules.to_csv(f"results/test/{algorithm}_rules.csv", index=False)


def process_month(month, data, min_support, min_confidence):
    GSP = GeneralizedSequentialPatternMining(data, min_support, min_confidence)
    GSP_frequent_sequences = GSP.mine_frequent_sequences()
    GSP_rules = GSP.generate_association_rules(GSP_frequent_sequences)
    save_results(month, GSP_frequent_sequences)
    save_rules(month, GSP_rules)

    APRIORI = Apriori(data, min_support, min_confidence)
    APRIORI_frequent_sequences = APRIORI.mine_frequent_itemsets()
    APRIORI_rules = APRIORI.generate_association_rules(APRIORI_frequent_sequences)
    save_results(month, APRIORI_frequent_sequences)
    save_rules(month, APRIORI_rules)

    return month, GSP_frequent_sequences, GSP_rules


def process_month_wrapper(args):
    month, data, min_support, min_confidence = args
    return process_month(month, data, min_support, min_confidence)


if __name__ == '__main__':
    sequences = data_preparation.generate_sequences('oddelki', ['ZAVMATNAZ', 'OBDOBJE',
                                                                'STEV_UCENCEV', 'DOGODEK', 'VZROK', 'TRAJANJE'])

    args_list = [(month, data, 0.5, 0.5) for month, data in sequences.items()]
    results = []
    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_month_wrapper, args): args[0] for args in args_list}
        for future in as_completed(futures):
            month = futures[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Processed {month}")
            except Exception as e:
                print(f"Error processing {month}: {e}")

    print("All months processed.")
