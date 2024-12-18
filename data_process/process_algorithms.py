import os
import time
import csv
from algorithms.apriori import Apriori
from algorithms.gsp import GeneralizedSequentialPatternMining
from data_process.data_csv_save import save_results, save_rules


class process_algorithms:
    def __init__(self, dataset_name, dataset_month, seq, min_supp, min_conf):
        self.dataset_name = dataset_name
        self.dataset_month = dataset_month
        self.seq = seq
        self.transactions = sequences_to_transactions(seq)
        self.min_support = min_supp
        self.min_confidence = min_conf

    def process(self):
        elapsed_time_apriori = self.process_apriori()
        elapsed_time_gsp = self.process_gsp()

        output_dir = 'results'
        output_file = f'{output_dir}/timings.csv'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        with open(output_file, 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([self.dataset_name, self.dataset_month, 'GSP', elapsed_time_gsp])
            csvwriter.writerow([self.dataset_name, self.dataset_month, 'APRIORI', elapsed_time_apriori])

        print(
            f"processed {self.dataset_name} {self.dataset_month}: "
            f"GSP in {elapsed_time_gsp:.2f} seconds, APRIORI in {elapsed_time_apriori:.2f} seconds")

    def process_apriori(self):
        start_time_apriori = time.time()
        APRIORI = Apriori(self.transactions, self.min_support, self.min_confidence)
        APRIORI_frequent_sequences = APRIORI.mine_frequent_itemsets()
        APRIORI_rules = APRIORI.generate_association_rules(APRIORI_frequent_sequences)
        save_results(self.dataset_name, 'APRIORI', self.dataset_month, APRIORI_frequent_sequences, len(self.transactions))
        save_rules(self.dataset_name, 'APRIORI', self.dataset_month, APRIORI_rules)
        end_time_apriori = time.time()
        elapsed_time_apriori = end_time_apriori - start_time_apriori
        return elapsed_time_apriori

    def process_gsp(self):
        start_time_gsp = time.time()
        GSP = GeneralizedSequentialPatternMining(self.seq, self.min_support, self.min_confidence)
        GSP_frequent_sequences = GSP.mine_frequent_sequences()
        GSP_rules = GSP.generate_association_rules(GSP_frequent_sequences)
        save_results(self.dataset_name, 'GSP', self.dataset_month, GSP_frequent_sequences, len(self.seq))
        save_rules(self.dataset_name, 'GSP', self.dataset_month, GSP_rules)
        end_time_gsp = time.time()
        elapsed_time_gsp = end_time_gsp - start_time_gsp
        return elapsed_time_gsp


def sequences_to_transactions(sequences):
    transactions = []
    for sequence in sequences:
        for _, items in sequence:
            transactions.append([items])
    return transactions
