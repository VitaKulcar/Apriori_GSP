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
            last_item = seq[-1][-1]
            for item in items:
                if item > last_item:
                    new_seq = seq + ((item,),)
                    if calc_support(new_seq, sequence_list) >= min_support:
                        candidates.add(new_seq)
    return candidates


def filter_candidates(candidates,  sequence_list, min_support):
    valid_candidates = {}
    for candidate in candidates:
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
    return all(any(set(subseq).issubset(itemset) for itemset in it) for subseq in candidate)


def get_unique_items(sequences):
    unique_items = set(item for sequence in sequences for itemset in sequence for item in itemset)
    return sorted(unique_items)


class Apriori:
    def __init__(self, sequences, min_support):
        self.dataset = sequences
        self.min_support_count = min_support * len(self.dataset)
        self.unique_items = get_unique_items(self.dataset)

    def run(self):
        current_level = set()
        frequent_sequences = {}
        k = 1
        # 1-item sequences
        candidates = generate_candidates(current_level, self.unique_items, self.dataset, self.min_support_count)
        while candidates:
            valid_candidates = filter_candidates(candidates, self.dataset, self.min_support_count)
            frequent_sequences.update(valid_candidates)
            k += 1
            current_level = set(valid_candidates.keys())
            candidates = generate_candidates(current_level, self.unique_items, self.dataset, self.min_support_count)

        return frequent_sequences
