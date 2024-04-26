
import pandas as pd
import csv

def get_data_train_nhan_tsv(filename):
  data_nhan = []
  data_file = pd.read_csv(filename, sep='\t')
  data_nhan = data_file['Values']
  return data_nhan

def get_data_train_vecto_csv(filename):
    vectors = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            vector = [float(x) for x in row]
            vectors.append(vector)
    return vectors