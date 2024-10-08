from algorithms.gsp import GeneralizedSequentialPatternMining
from algorithms.apriori import Apriori
from data_process.data_csv_save import rule_to_string


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


# test GSP algoritma po viru: https://simpledatamining.blogspot.com/2015/03/generalized-sequential-pattern-gsp.html
sequences = [
    [('a'), ('b'), ('f', 'g'), ('c'), ('d')],
    [('b'), ('g'), ('d')],
    [('b'), ('f'), ('g'), ('a', 'b')],
    [('f'), ('a', 'b'), ('c'), ('d')],
    [('a'), ('b', 'c'), ('g'), ('f'), ('d', 'e')]
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
