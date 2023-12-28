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
    
ages = {'7-14': 12.4, '15-24': 19.5, '25-40': 32.5, '41-64': 52.5}
df['age'] = df['age'].apply(lambda x: ages[x])

#PROBLEM 2
precov = {
    'Not at all': 0, 
    'Rarely, a couple of times per year': 0, #close to not at all
    'Sometimes, a couple of times per month': 1,
    'Often, a couple of times per week': 2,
    'Always, almost every day': 3,
}

#PROBLEM 2
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
    'Up to 15 minutes': 0.25,
    'From 15 to 30 minutes': 0.5,
    'From 30 minutes to one hour': 0.75,
    'More than one hour': 1.0,
}

df['time'] = df['time'].apply(lambda x: minutes[x])

loc = {
    'Yes, at all time':1,
    'Yes, while using the app': 1,
    'No, not at all':0,  
}

df['location'] = df['location'].apply(lambda x: loc[x])

#Make Activity only 0 or 1 

df.socializing= df.socializing.apply(lambda x: 0 if x== 'Alone or with pets' else 1)

df = df.reset_index(drop=True)

#Hot one encoding for entries, where people were allowed to make multiple choices

#df = pd.concat([df,stats('municipality'),stats('activity')],axis=1)

df['safety'] = df[['physicalsafety']]

#if at least one is different
df.safety[df[df.physicalsafety != df.covidsafety].index] = 0

df = pd.concat([df,stats('municipality'),stats('activity')],axis=1)
df = df.drop(columns=['location','municipality', 'activity','interest','physicalsafety','covidsafety']) #'interest','location','socializing' 

#delete raraly visited municipalities
df = df.drop(columns=['Rakovica','Voždovac','Savski Venac','Čukarica','Barajevo', 'Grocka','Surčin', 'Palilula', 'Lazarevac', 'Sopot', 'Obrenovac', 'Mladenovac'])

