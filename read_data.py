import pandas as pd

df = pd.read_csv('data/myntra.csv', header=None, sep=',')

# create a new csv file with only first 50000 entries

df = df.head()

# Iterate over the dataframa and print specific columns

for index, row in df[1:].iterrows():
    print(row[1], row[4], row[5], row[6], row[7], row[8], row[9], row[10])