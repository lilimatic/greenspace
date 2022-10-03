import pandas as pd 
import os


# descriptive table creator 
def table_creator(df,x,book):
    var = df[x].value_counts(normalize=True).mul(100).round(1)
    var1 = df[x].value_counts()
    var_table = pd.concat([var1,var], axis=1,keys=('count','%'))
    var_table.to_excel(f'/Users/lilimatic/greenspace/tables/{book}/'+x+'.xlsx') 
    return var_table