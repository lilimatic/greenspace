import pandas as pd
import numpy as np

def stats(col):
    features = list(set(', '.join(map(str, df[col].to_numpy())).split(', ')))
    stats = pd.DataFrame(np.array([[int(feature in str(item)) for item in df[col].to_numpy()] for feature in features]).T, columns=features,
                        index=df.index)
    return stats

df = pd.read_csv(f'data/data.csv',index_col=0)

#Clean data set and read

df = df.loc[:, df.columns!='Timestamp']
df = df[df['Gender'] != 'Apache attack helicopter']
df = df[df['If your identity was not revealed, would you want to provide your phone’s location (see question 10)?'] != 'Yes']

df = df.dropna()

#Dictionary to understand what is where 
rename = pd.Series(list(df.columns),index=['age','gender','municipality','precovid', 'freqency','time', 'activity','socializing','distancing',
'physicalsafety','covidsafety', 'interest','location']).to_dict()

df.columns = ['age','gender','municipality','precovid', 'frequency','time', 'activity','socializing','distancing',
'physicalsafety','covidsafety', 'interest','location']

# Data preprocessing 

df.gender= df.gender.apply(lambda x: 1 if x== 'Female' else 0 )

binary = ['distancing','physicalsafety','covidsafety', 'interest']

for x in binary:
    df[x]= df[x].apply(lambda x: 1 if x== 'Yes' else 0 )
    
ages = {'7-14': 0, '15-24': 1, '25-40': 2, '41-64': 3}
df['age'] = df['age'].apply(lambda x: ages[x])

precov = {
    'Not at all': 0,
    'Rarely, a couple of times per year': 1,
    'Sometimes, a couple of times per month': 2,
    'Often, a couple of times per week': 3,
    'Always, almost every day': 4,
}

df['precovid'] = df['precovid'].apply(lambda x: precov[x])

freq = {
    'Not at all': 0,
    'Less frequently': 1,
    'As frequently': 2,
    'More frequently': 3,
}

df['frequency'] = df['frequency'].apply(lambda x: freq[x])

minutes = {
    'Not at all': 0,
    'Up to 15 minutes': 1,
    'From 15 to 30 minutes': 2,
    'From 30 minutes to one hour': 3,
    'More than one hour': 4,
}

df['time'] = df['time'].apply(lambda x: minutes[x])

loc = {
    'Yes, at all time':0,
    'Yes, while using the app': 1,
    'No, not at all':2,  
}

df['location'] = df['location'].apply(lambda x: loc[x])

df = df.reset_index(drop=True)

#Hot one encoding for entries, where people were allowed to make multiple choices

df = pd.concat([df,stats('municipality'),stats('activity'),stats('socializing')],axis=1)
df = df.drop(columns=['municipality', 'activity','socializing'])