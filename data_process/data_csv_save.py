import pandas as pd


def attributes(dataset_name, columns):
    df = pd.read_csv(f'datasets/cleaned_data/{dataset_name}.csv')

    attributes_list = []
    # v vsakem stolpcu poiščemo unikatne vrednosti
    for column in columns:
        if column in df.columns:
            unique_values = df[column].unique()
            unique_values_str = ', '.join(map(str, unique_values))
            attributes_list.append({'Feature': column, 'Attributes': unique_values_str})

    attributes_df = pd.DataFrame(attributes_list)
    attributes_df.to_csv(f'datasets/attributes/{dataset_name}.csv', index=False)


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