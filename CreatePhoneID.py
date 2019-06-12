"""
Create a phone ID column to allow merging of dataframes.  Names don't work for this purpose becaues they are spelled inconsistently.
Takes .xlsx or .csv files.  Phone numbers can be in any format and with or without the country code (+1 for US)
"""

import pandas as pd
import numpy as np
import sys

f=str(sys.argv[1])
xlflag=input(""" Type '1' if xlsx, or '0' for csv:  """)
if xlflag==1:
    dfa=pd.read_excel(f)
else:
    dfa=pd.read_csv(f)
print(dfa.columns.to_list())
colname=input('What is the name of the column with the phone numbers?  ')

dfa[colname]=dfa[colname].astype(str)
dfa2=dfa.copy()
dfa2=dfa2[dfa2[colname].apply(lambda x: (len(x) >= 10))]

print('Removing numbers that are too short or blank...')
print('Dimensions changed from',dfa.shape,'to',dfa2.shape)

lista=[]
for phone_no in dfa2[colname]:
    contactphone=phone_no.replace('-','').replace(' ','')[-10:] #get final 10 digits to exclude leading 1's
    lista.append(str(contactphone))
    
arra=np.array(lista)
dfa2['PhoneID']=arra
for i in dfa2.index:
    if not dfa2.loc[i,'PhoneID'].isnumeric():
        dfa2.loc[i,'PhoneID']='null'
        
del(lista,arra)
dfa2=dfa2[dfa2['PhoneID']!='null']
newfilename='PhoneID'+f[2:]
dfa2.to_csv(newfilename,index=False)
print('Done!')
