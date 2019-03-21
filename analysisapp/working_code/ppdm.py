import pandas as pd
import numpy as np
import sqlite3

print("Opening Database")
conn = sqlite3.connect('insurance.db')
print("Reading data ...")
df = pd.read_sql_query("SELECT * FROM Claims", conn, coerce_float=True, parse_dates=["Date_Of_Birth", "Policy_Start",
                                                                                     "Policy_End", "Date_Of_Loss",
                                                                                     "Date_Of_Claim"])
#
# print("\n\n\nPreserve Name ")
# df['Name'] = '*'
#
# print("\n\n\nPreserve Surname ")
# df['Surname'] = '*'
#
# print("\n\n\nPreserve Party Name")
# df['Party_Name'] = '*'
#
# print("\n\n\nPreserve Party Surname")
# df['Party_Surname'] = '*'
#
# print("\n\n\nPreserve Policy_Holder_City")
# df['Policy_Holder_City'] = '*'
#
# print("\n\n\nPreserve Policy_Holder_Street")
# df['Policy_Holder_Street'] = '*'
#
# print("\n\n\nPreserve Policy_Holder_Area")
# df['Policy_Holder_Area'] = '*'
#
# print("\n\n\nPreserve Province")
# df['Province'] = '*'

print("\n\n\nPreserve Area")
df['Area'] = '*'

print("\n\n\nPreserve Age")
df['Age'] = df['Age'].astype(str).str[:-3].astype(str) + "*"

print("\n\n\nPreserve Date OF Birth")
df['Date_Of_Birth'].fillna(value='0', inplace=True)
tmp = df['Date_Of_Birth'].astype(str).str.replace('-', '')
df['Date_Of_Birth'] = tmp.astype(str).str[:-11].astype(np.int64)

print("\n\n\nPreserve Marital Status")
df['Marital_Status'] = df['Marital_Status'].astype(str).str[0:2].astype(str)

print("\n\n\nPreserve Gender, Insure_ID, Kind_Of_Loss")
for index, row in df.iterrows():
    prev = ''
    prevIn = ''
    if index == 0:
        prev = row['Gender']
    if prev == row['Gender']:
        df.loc[index, 'Gender'] = '*'
    prev = row['Gender']

    if index == 0:
        prevIn = row['Insured_ID']
    if prevIn == row['Insured_ID']:
        df.loc[index, 'Insured_ID'] = '*'
    prevIn = row['Insured_ID']

    prevK = ''
    if index == 0:
        prevK = row['Kind_Of_Loss']
    if prevK == row['Kind_Of_Loss']:
        df.loc[index, 'Kind_Of_Loss'] = '*'
    prevK = row['Kind_Of_Loss']
    print("\rComplete: " + str((index / 100000.0) * 100) + "%", end="")

print(df.sample(5))

print("\n\n\nPreserve Fraud Claim Indicator")
df['Fraudulent_Claim'] = df['Fraudulent_Claim'].astype(str).str.replace('T', '*').astype(str).str.replace('F', '')

print("\n\n\nPreserve Broker ID")
df['Broker_ID'] = df['Broker_ID'].astype(str).str[3:].astype(np.int64)

print("\n\n\nPreserve Policy_Holder_Postal")
df['Policy_Holder_Postal'] = df['Policy_Holder_Postal'].astype(str).str[:-2].astype(str) + "**"
df['Claim_ID'] = df['Claim_ID'].astype(int)
print(df.sample(5))

#Write data from df to database
print("\n\n\nWriting Data to Database")
df.to_sql("Claims", conn, if_exists="replace", index=False)
