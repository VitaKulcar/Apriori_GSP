from algorithms.gsp import GeneralizedSequentialPatternMining
from algorithms.apriori import Apriori
from data_process.data_csv_save import rule_to_string
from data_process.process_algorithms import sequences_to_transactions


def process_GSP(data, min_support, min_confidence):
    GSP = GeneralizedSequentialPatternMining(data, min_support, min_confidence)
    frequent_sequences = GSP.mine_frequent_sequences()
    rules = GSP.generate_association_rules(frequent_sequences)
    return frequent_sequences, rules


def process_Apriori(data, min_support, min_confidence):
    apriori = Apriori(data, min_support, min_confidence)
    frequent_sequences = apriori.mine_frequent_itemsets()
    rules = apriori.generate_association_rules(frequent_sequences)
    return frequent_sequences, rules


def sequence_to_string(s):
    set_notation = ", ".join(["{" + ", ".join(item) + "}" for item in s])
    return f"{set_notation}"


def print_results(frequent_items, rules):
    print(f"\nFrequent items:")
    for seq, supp in frequent_items.items():
        s = sequence_to_string(seq)
        print(f"Sequence: {s}, Support: {supp}")

    print(f"\nAssociation rules:")
    for rule, conf in rules.items():
        r = rule_to_string(rule)
        print(f"Rule: {r}, Confidence: {conf}")


"""
# test GSP algoritma po viru: https://simpledatamining.blogspot.com/2015/03/generalized-sequential-pattern-gsp.html
sequences = [
    [("2022-01-01", ('a')),
     ("2022-01-01", ('b')),
     ("2022-01-01", ('f', 'g'),),
     ("2022-01-01", ('c')),
     ("2022-01-01", ('d'))],
    [("2022-01-02", ('b')),
     ("2022-01-02", ('g')),
     ("2022-01-02", ('d'))],
    [("2022-01-03", ('b')),
     ("2022-01-03", ('f')),
     ("2022-01-03", ('g')),
     ("2022-01-03", ('a', 'b'))],
    [("2022-01-04", ('f')),
     ("2022-01-04", ('a', 'b')),
     ("2022-01-04", ('c')),
     ("2022-01-04", ('d'))],
    [("2022-01-05", ('a')),
     ("2022-01-05", ('b', 'c')),
     ("2022-01-05", ('g')),
     ("2022-01-05", ('f')),
     ("2022-01-05", ('d', 'e'))]
]
GSP_frequent_sequences, GSP_rules = process_GSP(sequences, 0.25, 0.5)
print_results(GSP_frequent_sequences, GSP_rules)

# test GSP algoritma po viru: https://www.philippe-fournier-viger.com/dspr-paper5.pdf
sequences_a = [
    [("a", "b"), ("c"), ("f", "g"), ("g"), ("e")],
    [("a", "d"), ("c"), ("b"), ("a", "b", "e", "f")],
    [("a"), ("b"), ("f", "g"), ("e")],
    [("b"), ("f", "g")]
]
GSP_frequent_sequences_a, GSP_rules_a = process_GSP(sequences_a, 0.5, 0.5)
print_results(GSP_frequent_sequences_a, GSP_rules_a)

# test Apriori algoritma po viru: https://codinginfinite.com/apriori-algorithm-numerical-example/
transactions = [
    ['1', '3', '4'],
    ['2', '3', '5', '6'],
    ['1', '2', '3', '5'],
    ['2', '5'],
    ['1', '3', '5']
]
apriori_frequent_sequences, apriori_rules = process_Apriori(transactions, 0.25, 0.5)
print_results(apriori_frequent_sequences, apriori_rules)

# test Apriori algoritma po viru: https://medium.com/image-processing-with-python/apriori-algorithm-in-associate-rule-mining-dc9404caffd1
transactions_a = [
    ['a', 'b', 'c'],
    ['b', 'e'],
    ['c', 'd', 'e'],
    ['a', 'd'],
    ['b', 'c', 'd'],
    ['a', 'e', 'g'],
    ['a', 'b', 'd', 'f'],
    ['c', 'e', 'f'],
    ['a', 'c', 'd', 'e'],
    ['b', 'd']
]
apriori_frequent_sequences_a, apriori_rules_a = process_Apriori(transactions_a, 0.2, 0.5)
print_results(apriori_frequent_sequences_a, apriori_rules_a)
"""
"""
sequences_b = [
    [("2022-01-01", ("Mleko", "Kruh", "Jajca"))],
    [("2022-01-02", ("Mleko", "Jabolka", "Banana", "Pomaranča"))],
    [("2022-01-01", ("Mleko", "Kruh", "Maslo", "Jabolka"))],
    [("2022-01-02", ("Jabolka", "Banana", "Mleko"))],
    [("2022-01-01", ("Kruh", "Mleko", "Jajca"))],
    [("2022-01-01", ("Mleko", "Jabolka", "Banana", "Kruh"))],
    [("2022-01-01", ("Kruh", "Maslo"))],
    [("2022-01-02", ("Kruh", "Jabolka"))],
    [("2022-01-02", ("Mleko", "Kruh", "Pomaranča"))],
    [("2022-01-02", ("Jabolka", "Kruh", "Banana"))]
]"""

sequences_b = [
    [("2022-01-01", ("Mleko", "Kruh", "Jajca")),
     ("2022-01-01", ("Mleko", "Kruh", "Maslo", "Jabolka")),
     ("2022-01-01", ("Kruh", "Mleko", "Jajca"))],
    [("2022-01-02", ("Mleko", "Jabolka", "Banana", "Kruh")),
     ("2022-01-02", ("Kruh", "Maslo"))],
    [("2022-01-03", ("Mleko", "Jabolka", "Banana", "Pomaranča")),
     ("2022-01-03", ("Jabolka", "Banana", "Mleko")),
     ("2022-01-03", ("Kruh", "Jabolka"))],
    [("2022-01-04", ("Mleko", "Kruh", "Pomaranča")),
     ("2022-01-04", ("Jabolka", "Kruh", "Banana"))]
]

apriori_frequent_sequences_b, apriori_rules_b = process_Apriori(sequences_to_transactions(sequences_b), 0.5, 0.5)
print_results(apriori_frequent_sequences_b, apriori_rules_b)
GSP_frequent_sequences_b, GSP_rules_b = process_GSP(sequences_b, 0.5, 0.5)
print_results(GSP_frequent_sequences_b, GSP_rules_b)

