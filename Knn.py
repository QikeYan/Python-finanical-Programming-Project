import numpy as np
import pandas as pd
import csv

def DESeq_normalization(counts):
    counts = counts[np.alltrue(counts, axis=1)]
    counts=counts.values
    logcounts = np.log(counts)
    loggeommeans = np.mean(logcounts, axis=1).reshape(len(logcounts), 1)
    sf = np.exp(np.median(logcounts - loggeommeans, axis=0))
    nor_counts = np.divide(counts, sf)
    return nor_counts

counts=pd.read_csv('NeuralStemCellData.tab',delimiter='\t',encoding='utf-8')
del counts['Gene']
print(counts)
df2=counts[np.alltrue(counts, axis=1)]
print("Before DESeq normalization:\n")
print(df2)
print("After DESeq normalization:\n")
print(pd.DataFrame(DESeq_normalization(df2),columns=['GliNS1','G144','G166','G179','CB541','CB660']))

# user_info=pd.read_csv('fly_RNA_counts.tsv',delimiter='\t',encoding='utf-8')
#
# print(list(user_info.columns.values)) #file header
# print("read tsv file to get dataset:\n")
# print(user_info.tail(35)) #last N rows
# df1=user_info[np.alltrue(user_info, axis=1)]
# print("Before DESeq normalization:\n")
# print(df1)
# print("After DESeq normalization:\n")
# print(pd.DataFrame(DESeq_normalization(df1),columns=['A1', 'A2', 'B1','B2']))


