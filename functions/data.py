import pandas as pd

df = pd.read_csv(f'data/data.csv')

#Clean data set and read

df = df.loc[:, df.columns!='Timestamp']
df = df[df['Gender'] != 'Apache attack helicopter']
df = df[df['If your identity was not revealed, would you want to provide your phone’s location (see question 10)?'] != 'Yes']


    