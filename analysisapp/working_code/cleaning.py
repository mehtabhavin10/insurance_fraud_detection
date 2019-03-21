import pandas as pd
import numpy as np
import sqlite3


def clean_data():

    print(    "Opening Database"    )
    conn = sqlite3.connect('insurance.db')
    print(        "Reading data ..."    )
    df = pd.read_sql_query("SELECT * FROM Claims", conn, coerce_float=True, parse_dates=["Date_Of_Birth", "Policy_Start",
                                                                                         "Policy_End", "Date_Of_Loss",
                                                                                         "Date_Of_Claim"])

    print(    "\n\n\nDirty Data"    )
    df.loc[2, "Claim_ID"] = np.nan
    df.loc[30, "Postal_Code"] = ''
    df.loc[40, "Broker_ID"] = np.nan
    df.loc[22, "Date_Of_Claim"] = None
    df.loc[23, "Date_Of_Loss"] = None
    df.loc[44, "Sum_Insured"] = -5000.01
    df.loc[50, "Date_Of_Loss"] = pd.Timestamp("2018-03-01 00:00:00", tz=None)
    df.loc[200, "Policy_Start"] = pd.Timestamp("2018-03-01 00:00:00", tz=None)
    df.loc[500, "Policies_Revenue"] = None
    df.loc[100, "Policies_Revenue"] = None
    df.loc[520, "Policies_Revenue"] = None
    df.loc[1, "Policies_Revenue"] = None

    ####### Write data from df to database
    # print(    "\n\n\nWriting Data to Database"    )
    # df.to_sql("Claims", conn, if_exists="replace", index=False)

    # print(    "Opening Database"   )
    # conn = sqlite3.connect('insurance.db')
    # print(       "Reading data ..."   )
    # df = pd.read_sql_query("SELECT * FROM Claims",conn,  coerce_float=True, parse_dates=["Date_Of_Birth", "Policy_Start",
    #                                                  "Policy_End", "Date_Of_Loss", "Date_Of_Claim"])

    if 'Name' in df.columns:
        print(    "\n\n\nRemove Name"    )
        del df['Name']

    if 'Surname' in df.columns:
        print(    "\n\n\nRemove Surname"    )
        del df['Surname']

    if 'Party_Name' in df.columns:
        print(    "\n\n\nRemove Party_Name"    )
        del df['Party_Name']

    if 'Party_Surname' in df.columns:
        print(    "\n\n\nRemove Party_Surname"    )
        del df['Party_Surname']

    if 'Policy_Holder_Street' in df.columns:
        print(    "\n\n\nRemove Policy_Holder_Street"    )
        del df['Policy_Holder_Street']

    if 'Policy_Holder_Area' in df.columns:
        print(    "\n\n\nRemove Policy_Holder_Area"    )
        del df['Policy_Holder_Area']

    if 'Province' in df.columns:
        print(    "\n\n\nRemove Province"    )
        del df['Province']

    if 'Area' in df.columns:
        print(    "\n\n\nRemove Area"    )
        del df['Area']

    if 'Policy_Holder_City' in df.columns:
        print(    "\n\n\nRemove Policy_Holder_City"    )
        del df['Policy_Holder_City']

    if 'index' in df.columns:
        del df['index']

    print(    "\n\n\nHandle Policy Start and end Date"    )
    df = df[(df['Policy_End'] >= df['Policy_Start'])]

    print(    "\n\n\nHandle Date of loss and claim"    )
    df = df[(df['Date_Of_Claim'] >= df['Date_Of_Loss'])]

    print(    "\n\n\nHandle Claim_ID"    )
    df['Claim_ID'].dropna(how='any', inplace=True)
    df['Claim_ID'] = df['Claim_ID'].astype(int)

    print(    "\n\n\nHandle Postal_Code"    )
    df['Postal_Code'].dropna(how='any', inplace=True)

    print(    "\n\n\nHandle Broker_ID"    )
    df['Broker_ID'].dropna(how='any', inplace=True)

    print(    "\n\n\nHandle Date_Of_Claim"    )
    df['Date_Of_Claim'].dropna(how='any', inplace=True)

    print(    "\n\n\nHandle Date_Of_Loss"    )
    df['Date_Of_Loss'].dropna(how='any', inplace=True)

    print(    "\n\n\nHandle Broker_ID"    )
    df['Broker_ID'].dropna(how='any', inplace=True)

    print(    "\n\n\nHandle Sum_Insured"    )
    df['Sum_Insured'].dropna(how='any', inplace=True)
    df = df[df['Sum_Insured'] > -0.0]

    print(    "\n\n\nHandle Policies_Revenue"    )
    df['Policies_Revenue'].fillna(value=df['Policies_Revenue'].mean(), inplace=True)

    #    ;; ; ; ;; ; ;
    # df.interpolate()91377 91417
    #  ' ' ' ' ' ' ' ''
    print(df.head())
    df.dropna(how='any', inplace=True)
    print(df.isnull().sum())
    ####### Write data from df to database
    print(    "\n\n\nWriting Data to Database"    )
    df.to_sql("Claims", conn, if_exists="replace", index=False)
