import pandas as pd 
import os
import numpy as np
import matplotlib.pyplot as plt

from functions.data import df

# descriptive table creator 
def table_creator(df,x,book):
    var = df[x].value_counts(normalize=True).mul(100).round(1)
    var1 = df[x].value_counts()
    var_table = pd.concat([var1,var], axis=1,keys=('count','%'))
    var_table.to_excel(f'/Users/lilimatic/greenspace/tables/{book}/'+x+'.xlsx') 
    return var_table

def stats(col):
    features = list(set(', '.join(map(str, df[col].to_numpy())).split(', ')))
    stats = pd.DataFrame(np.array([[int(feature in str(item)) for item in df[col].to_numpy()] for feature in features]).T, columns=features)
    return stats

def freqcount(question,tres,book,part):
    data_location_m = stats(question)
    output = np.sum(data_location_m)
    output = output.drop('nan')
    others = output[output < tres]
    output = output[output >= tres]
    output['Others'] = np.sum(others)
    outputdf = pd.DataFrame(output)
    outputdf['%'] = np.round(output*100 /np.sum(output),1) 
    outputdf.columns = ['counts','%']
    outputdf.to_excel(f'/Users/lilimatic/greenspace/tables/remainder/'+part+'.xlsx')
    plt.bar(output.index, output)
    plt.xticks(rotation=90)
    #plt.savefig('f'/Users/lilimatic/greenspace/images/remainder/'+part+'.xlsx')
    #plt.savefig('images/activity/' + question+'.png')
    return outputdf
    