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


def filter_unique_candidates(candidates):
    unique_candidates = set()
    filtered_candidates = []

    for candidate in candidates:
        # Convert candidate to a frozenset to ignore order and ensure uniqueness
        candidate_set = frozenset(candidate)

        # Check if this candidate has already been seen
        if candidate_set not in unique_candidates:
            unique_candidates.add(candidate_set)
            filtered_candidates.append(candidate)

    return filtered_candidates


def filter_candidates(candidates, sequence_list, min_support):
    # First filter candidates for uniqueness
    unique_candidates = filter_unique_candidates(candidates)

    valid_candidates = {}
    for candidate in unique_candidates:
        support = calc_support(candidate, sequence_list)
        if support >= min_support:
            valid_candidates[candidate] = support

    return valid_candidates


def calc_support(candidate_sequence, sequence_list):
    count = 0
    for seq in sequence_list:
        if is_subsequence(candidate_sequence, seq):
            count += 1
    return count


def is_subsequence(candidate, sequence):
    it = iter(sequence)
    for subseq in candidate:
        found = False
        for itemset in it:
            if set(subseq).issubset(set(itemset[-1])):
                found = True
                break
        if not found:
            return False
    return True


def get_unique_items(sequences):
    return sorted(set(item for sequence in sequences for _, itemset in sequence for item in itemset))


class GeneralizedSequentialPatternMining:
    def __init__(self, sequences, min_supp, min_conf):
        self.dataset = sequences
        self.min_support_count = min_supp * len(self.dataset)
        self.min_confidence = min_conf
        self.unique_items = get_unique_items(self.dataset)

    def mine_frequent_sequences(self):
        current_level = set()
        frequent_sequences = {}
        while True:
            candidates = generate_candidates(current_level, self.unique_items, self.dataset, self.min_support_count)
            candidates = filter_unique_candidates(candidates)
            current_level = set()
            for candidate in candidates:
                support = calc_support(candidate, self.dataset)
                if support >= self.min_support_count:
                    current_level.add(candidate)
                    frequent_sequences[candidate] = support
            if not current_level:
                break
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
