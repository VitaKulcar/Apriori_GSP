import itertools


def generate_candidates(previous_level, items, sequence_list, min_support):
    candidates = set()
    # one-item sequence candidates
    if not previous_level:
        for item in items:
            candidate = ((item,),)
            if calc_support(candidate, sequence_list) >= min_support:
                candidates.add(candidate)
    else:  # new candidates from previous level
        for seq in previous_level:
            for item in items:
                if (item,) not in seq:
                    new_seq = seq + ((item,),)
                    if calc_support(new_seq, sequence_list) >= min_support:
                        candidates.add(new_seq)
    return candidates


def filter_candidates(candidates, sequence_list, min_support):
    valid_candidates = {}
    for candidate in candidates:
        normalized_candidate = tuple(sorted(candidate))
        support = calc_support(candidate, sequence_list)
        if support >= min_support:
            valid_candidates[normalized_candidate] = support
    return valid_candidates


def calc_support(candidate_sequence, sequence_list):
    count = 0
    for seq in sequence_list:
        if is_subsequence(candidate_sequence, seq):
            count += 1
    return count


def is_subsequence(candidate, sequence):
    # Flatten the sequence into a single set of items for easier searching
    sequence_items = {item for itemset in sequence for item in itemset}

    # Check if each item in the candidate is found in the sequence
    for candidate_itemset in candidate:
        for item in candidate_itemset:
            if item not in sequence_items:
                return False  # Return False if any item is not found

    return True  # All items in candidate found in the sequence


def get_unique_items(sequences):
    unique_items = set(item for sequence in sequences for itemset in sequence for item in itemset)
    return sorted(unique_items)


def get_nonempty_subsets(itemset):
    subsets = []
    itemset = list(itemset)
    for i in range(1, len(itemset)):
        subsets.extend(itertools.combinations(itemset, i))
    return subsets


class Apriori:
    def __init__(self, transactions, min_supp, min_conf):
        self.dataset = transactions
        self.min_support_count = min_supp * len(self.dataset)
        self.min_confidence = min_conf
        self.unique_items = get_unique_items(self.dataset)

    def mine_frequent_itemsets(self):
        current_level = set()
        frequent_sequences = {}

        # začetni nabor 1-element množice
        candidates = generate_candidates(current_level, self.unique_items, self.dataset, self.min_support_count)

        # ustvarjanje in filtriranje kandidatov 2,3,4,...-elementnih množic
        while candidates:
            # izkanje kandidatov, ki ustrezajo minimalni podpori
            valid_candidates = filter_candidates(candidates, self.dataset, self.min_support_count)

            # dodajanje ustreznih kanjdidatov v slovar
            frequent_sequences.update(valid_candidates)

            # izbira elementov za generiranje naslednjih kandidatatov
            current_level = set(valid_candidates.keys())

            # generiranje novih kandidatov za naslednji nivo
            candidates = generate_candidates(current_level, self.unique_items, self.dataset, self.min_support_count)

        return frequent_sequences

    def generate_association_rules(self, frequent_itemsets):
        association_rules = {}
        for itemset, support in frequent_itemsets.items():
            if len(itemset) > 1:
                subsets = get_nonempty_subsets(itemset)
                for antecedent in subsets:
                    consequent = tuple(sorted(set(itemset) - set(antecedent)))
                    if consequent:
                        antecedent_support = calc_support(antecedent, self.dataset)
                        confidence = support / antecedent_support
                        if confidence >= self.min_confidence:
                            association_rules[(antecedent, consequent)] = confidence

        return association_rules
