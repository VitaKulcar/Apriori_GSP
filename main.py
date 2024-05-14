import pandas as pd
import data_preparation
from data_preparation import data_cleaning, attributes, generate_sequences
from apriori import Apriori
from gsp import GeneralizedSequentialPatternMining
from visualisation import visualize

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


"""
sequences = data_preparation.generate_sequences('oddelki', ['ZAVMATNAZ', 'OBDOBJE',
                                                            'STEV_UCENCEV', 'DOGODEK', 'VZROK', 'TRAJANJE'])
# za vsak mesec izvedi algoritem
for month in sequences:
    data = sequences[month]
    GSP = GeneralizedSequentialPatternMining(data, 0.5, 0.5)
    GSP_frequent_sequences = GSP.mine_frequent_sequences()
    GSP_rules = GSP.generate_association_rules(GSP_frequent_sequences)
    save_results(month, GSP_frequent_sequences)
    save_rules(month, GSP_rules)
    visualize('test/GSP_rules')
"""
sequences = [
    [("a", "b"), ("c"), ("f", "g"), ("g"), ("e")],
    [("a", "d"), ("c"), ("b"), ("a", "b", "e", "f")],
    [("a"), ("b"), ("f", "g"), ("e")],
    [("b"), ("f", "g")]
]
"""
sequences_tt = {
    '2020/09': [('Nova Gorica', 'OŠ', 'Okužba s Covid-19 pri vzgojitelju', '3. razred', '3 days'),
                ('Ljubljana', 'Vrtec', 'Okužba s Covid-19 pri vzgojitelju', 'Skupina A', '12 days'),
                ('Kočevje', 'Srednja', 'Okužba s Covid-19 pri učencu', '5. razred', '10 days'),
                ('Ljubljana', 'Glasbena', 'Okužba s Covid-19 pri otroku', 'Klavir', '5 days')],
    '2020/10': [('Kočevje', 'SŠ', 'Okužba s Covid-19 pri vzgojitelju', '2. razred', '9 days'),
                ('Nova Gorica', 'SŠ', 'Okužba s Covid-19 pri učitelju', '1. razred', '12 days'),
                ('Kranj', 'Srednja', 'Okužba s Covid-19 pri otroku', 'Skupina B', '5 days'),
                ('Kočevje', 'Gimnazija', 'Okužba s Covid-19 pri učitelju', '5. razred', '10 days')],
    '2020/11': [('Cerklje na Gorenjskem', 'OŠ', 'Okužba s Covid-19 pri otroku', '1. razred', '9 days'),
                ('Kočevje', 'Vrtec', 'Okužba s Covid-19 pri učencu', '5. razred', '7 days'),
                ('Maribor', 'Srednja', 'Okužba s Covid-19 pri učitelju', '4. razred', '12 days'),
                ('Ptuj', 'Srednja', 'Okužba s Covid-19 pri učencu', 'Skupina B', '9 days')],
    '2020/12': [('Celje', 'OŠ', 'Okužba s Covid-19 pri otroku', '5. razred', '10 days'),
                ('Kranj', 'Glasbena', 'Okužba s Covid-19 pri učitelju', '3. razred', '12 days'),
                ('Ptuj', 'Gimnazija', 'Okužba s Covid-19 pri vzgojitelju', '4. razred', '7 days'),
                ('Cerklje na Gorenjskem', 'SŠ', 'Okužba s Covid-19 pri učitelju', 'Kitara', '12 days')]
}
"""

GSP = GeneralizedSequentialPatternMining(sequences, 0.5, 0.5)
GSP_frequent_sequences = GSP.mine_frequent_sequences()
GSP_rules = GSP.generate_association_rules(GSP_frequent_sequences)
save_results('GSP_test', GSP_frequent_sequences)
save_rules('GSP_test', GSP_rules)
# visualize('test/GSP_rules')

"""
def generate_transactions(data_file):
    df = pd.read_csv(data_file)
    _transactions = {}
    for _, row in df.iterrows():
        regija = row['REGIJA']
        leto_mesec = row['LETO_MESEC_VNOSA']
        vzrok = row['VZROK']
        transaction_key = (leto_mesec, regija)
        if transaction_key not in _transactions:
            _transactions[transaction_key] = set()
        _transactions[transaction_key].add(vzrok)
    return _transactions
    
    
transactions = generate_transactions('datasets/cleaned_oddelki.csv')
print("transactions")
APRIORI = Apriori(transactions, 0.5)
APRIORI_frequent_sequences = APRIORI.run()
print("APRIORI")
save_results('APRIORI', APRIORI_frequent_sequences)
"""
