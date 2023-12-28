import pandas as pd
import numpy as np

import os
directory = f'/Users/lilimatic/greenspace'
os.chdir(directory)

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

oldcolumns = df.columns

df = df.reset_index(drop=True)

ages = {'7-14': 12.4, '15-24': 19.5, '25-40': 32.5, '41-64': 52.5}
df['age'] = df['age'].apply(lambda x: ages[x])

minutes = {
    'Not at all': 0,
    'Up to 15 minutes': 0.25,
    'From 15 to 30 minutes': 0.5,
    'From 30 minutes to one hour': 0.75,
    'More than one hour': 1.0,
}

df['time'] = df['time'].apply(lambda x: minutes[x])

df['safety'] = df.loc[:, 'physicalsafety']

df.safety[df[df.physicalsafety != df.covidsafety].index] = 0

df.safety= df.safety.apply(lambda x: 1 if x== 'Yes' else 0 )

hotone = ['gender','distancing', 'precovid','frequency','location'] #'physicalsafety','covidsafety', ,'interest','location'

df = pd.get_dummies(df,columns=hotone)

list_municipalities = stats('municipality')
list_activities = stats('activity')
list_socializing = stats('socializing')

df = pd.concat([df,stats('municipality'),stats('activity'),stats('socializing')],axis=1)

df = df.drop(columns=['municipality', 'activity','socializing','physicalsafety','covidsafety','interest']) #'location',

df = df.drop(columns=['Rakovica','Voždovac','Savski Venac','Čukarica','Barajevo', 'Grocka','Surčin', 'Palilula', 'Lazarevac', 'Sopot', 'Obrenovac', 'Mladenovac'])
