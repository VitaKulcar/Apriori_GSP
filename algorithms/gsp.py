def generate_candidates(previous_level, items, sequence_list, min_support):
    candidates = set()
    # Generate one-item sequence candidates (initial level)
    if not previous_level:
        for item in items:
            candidate = ((item,),)
            if calc_support(candidate, sequence_list) >= min_support:
                candidates.add(candidate)
    else:
        for seq in previous_level:
            last_itemset = seq[-1]
            for item in items:
                # Ensure the item is larger to maintain lexicographical order
                if item > max(last_itemset):
                    # i-extension: Add item to the last itemset of the sequence
                    new_seq = seq[:-1] + (last_itemset + (item,),)
                    if calc_support(new_seq, sequence_list) >= min_support:
                        candidates.add(new_seq)
                # s-extension: Add item as a new itemset to the sequence
                new_seq = seq + ((item,),)
                if calc_support(new_seq, sequence_list) >= min_support:
                    candidates.add(new_seq)
    return candidates


def calc_support(candidate_sequence, sequence_list):
    return sum(1 for seq in sequence_list if is_subsequence(candidate_sequence, seq))


def is_subsequence(candidate, sequence):
    it = iter(sequence)
    return all(any(set(subseq).issubset(itemset) for itemset in it) for subseq in candidate)


def get_unique_items(sequences):
    return sorted(set(item for sequence in sequences for itemset in sequence for item in itemset))


class GeneralizedSequentialPatternMining:
    def __init__(self, sequences, min_supp, min_conf):
        self.dataset = sequences
        self.min_support_count = min_supp * len(self.dataset)
        self.min_confidence = min_conf
        self.unique_items = get_unique_items(self.dataset)

    def mine_frequent_sequences(self):
        current_level = set()
        frequent_sequences = {}
        k = 1
        while True:
            candidates = generate_candidates(current_level, self.unique_items, self.dataset, self.min_support_count)
            current_level = set()
            for candidate in candidates:
                support = calc_support(candidate, self.dataset)
                if support >= self.min_support_count:
                    current_level.add(candidate)
                    frequent_sequences[candidate] = support
            if not current_level:
                break
            k += 1
        return frequent_sequences

    def generate_association_rules(self, frequent_sequences):
        association_rules = {}
        for sequence, support in frequent_sequences.items():
            if len(sequence) > 1:
                for i in range(len(sequence) - 1):
                    antecedent = sequence[:i + 1]
                    consequent = sequence[i + 1:]
                    confidence = support / calc_support(antecedent, self.dataset)
                    if confidence >= self.min_confidence:
                        association_rules[(antecedent, consequent)] = confidence
        return association_rules
