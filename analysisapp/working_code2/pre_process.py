import pandas as pd
import numpy as np
import sklearn.metrics as metrics
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn import tree
from sklearn.linear_model import LogisticRegression
from geopy.geocoders import Nominatim
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

final_pred = []
accuracy = []

def get_data():
    global final_pred
    global accuracy
    df = pd.read_csv('dataset.csv')

    print(df.tail(5))

    print(list(df))
    #print(df.info())

    string_col_list = ['policy_bind_date', 'policy_state', 'policy_csl', 'insured_sex', 'insured_education_level', 'insured_occupation', 'insured_hobbies', 'insured_relationship', 'incident_date', 'incident_type', 'collision_type', 'incident_severity', 'authorities_contacted', 'incident_state', 'incident_city', 'incident_location', 'property_damage', 'police_report_available', 'auto_make', 'auto_model', 'fraud_reported']


    print(df.groupby('fraud_reported').count())

    fraud_df = df[df['fraud_reported'] == "Y"]
    cities = list(fraud_df['incident_city'])
    cities_counts = { name : cities.count(name) for name in cities }
    print(cities_counts)

    education = list(fraud_df['insured_education_level'])
    education_counts = { name : education.count(name) for name in education }
    print(education_counts)

    location = list(fraud_df['incident_location'])
    location_counts = { name : location.count(name) for name in location }
    print(location_counts)

    #-------------------------------------//

    # Other Feature Graphs and Charts.

    #-------------------------------------//

    cols_to_delete = ["policy_number", "policy_bind_date", "insured_zip", "incident_location", "incident_date"]

    filtered_string_cols = [i for i in string_col_list if i not in cols_to_delete]

    df_series = pd.Series(filtered_string_cols)

    labels, levels = pd.factorize(df_series)

    print(labels)
    print(levels)

    for col in filtered_string_cols:
        col_series = pd.Series(list(df[col]))
        col_labels, col_levels = pd.factorize(col_series)
        df[col] = list(col_labels)

    print(df.head(5))
    print(df.tail(5))
    print(df.iloc[2])
    print(df.iloc[10])
    print(df.iloc[99])



    def load_data(feature_list):
        global final_pred
        iris = load_iris()
        print("\n\nInside load_data()")
        print("Type2: ", type(iris))
        iris.feature_names = feature_list
        iris.feature_names = [0,1]
        tmp = df['fraud_reported']
        iris.target = tmp.values
        iris.data = np.dstack((df['months_as_customer'],df['age'],df['policy_number'],df['policy_state'],df['policy_deductable'],
                               df['policy_annual_premium'],df['umbrella_limit'],df['insured_sex'],df['insured_education_level'],
                               df['insured_occupation'],df['capital-gains'],df['capital-loss'],df['incident_type'],
                               df['incident_state'],df['incident_city'],df['injury_claim']))[0]

        return iris


    features_list = ['months_as_customer', 'age', 'policy_number', 'policy_state',
                     'policy_deductable', 'policy_annual_premium', 'umbrella_limit' 'insured_sex',
                     'insured_education_level', 'insured_occupation',
                     'capital-gains', 'capital-loss', 'incident_type', 'incident_state', 'incident_city', 'injury_claim']

    iris = load_data(features_list)

    print("Type: ", type(iris))

    train_data, test_data, train_target, test_target = train_test_split(iris.data, iris.target, test_size=0.2, random_state=3)

    clf = tree.DecisionTreeClassifier()
    clf.fit(train_data, train_target)

    lr = LogisticRegression()
    lr.fit(train_data, train_target)

    rfc = RandomForestClassifier()
    rfc.fit(train_data, train_target)

    mlp = MLPClassifier()
    mlp.fit(train_data, train_target)

    print("Training set: " + str(len(train_target)))
    print("Testing set: " + str(len(test_target)))
    print(clf.predict(test_data))
    pred = clf.predict(test_data)

    pred2 = lr.predict(test_data)

    pred3 = rfc.predict(test_data)

    pred4 = mlp.predict(test_data)

    score = metrics.accuracy_score(test_target, pred)
    score2 = metrics.accuracy_score(test_target, pred2)
    score3 = metrics.accuracy_score(test_target, pred3)
    score4 = metrics.accuracy_score(test_target, pred4)
    print("Accuracy: " + str(score*100.0))
    print("Accuracy2: " + str(score2*100.0))
    print("\n\nType: ",list(pred2))
    final_pred = list(pred3)
    accuracy = [str(score*100.0), str(score2*100.0), str(score3*100.0), str(score4*100.0)]
    print("\n\nFinal: ", accuracy)

def occupation():
    df=pd.read_csv("dataset.csv")
    occupationList=[]
    occupationListCount=[]
    occupationListCount=df.groupby("insured_occupation")["insured_occupation"].count().tolist()
    occupationList=df["insured_occupation"].unique().tolist()
    return occupationListCount,occupationList
occupation()

def education():
    df=pd.read_csv("dataset.csv")
    educationList=[]
    educationListCount=[]
    educationListCount=df.groupby("insured_education_level")["insured_education_level"].count().tolist()
    educationList=df["insured_education_level"].unique().tolist()
    return educationListCount,educationList
education()


def sex():
    df=pd.read_csv("dataset.csv")
    sexList=[]
    sexListCount=[]
    sexListCount=df.groupby("insured_sex")["insured_sex"].count().tolist()
    sexList=df["insured_sex"].unique().tolist()
    return sexListCount,sexList
sex()


def age():
    df=pd.read_csv("dataset.csv")
    ageList=[]
    ageListCount=[]
    ageListCount=df.groupby("age")["age"].count().tolist()
    ageList=df["age"].unique().tolist()
    ageList.sort()
    sortList=ageList
    return ageListCount,sortList
def maps():
    df = pd.read_csv("dataset.csv")
    geolocator = Nominatim(user_agent="analysisapp")
    lat_long = []
    cities=df["incident_city"].unique().tolist()
    print("cities: ",cities)
    for i in cities:
        location = geolocator.geocode(i,timeout=2000)  # "California")
        latitude = location.latitude
        longitude = location.longitude
        latLong = [latitude, longitude]
        values = {
            "latLng": latLong,
            "name": i
        }

        lat_long.append(values)
        print("ddcdc",lat_long)
    return lat_long

def tableData():
    global final_pred
    df=pd.read_csv("dataset.csv")
    data=[]
    columns=[]
    columns=df.columns.tolist()
    print(columns)
    columnsToSelect=[]
    columnsToSelect.append(columns[1])
    columnsToSelect.append("policy number")
    # columnsToSelect.append(columns[9])
    columnsToSelect.append(columns[10])
    columnsToSelect.append(columns[11])
    columnsToSelect.append(columns[12])
    columnsToSelect.append(columns[22])
    columnsToSelect.append(columns[23])
    columnsToSelect.append(columns[24])
    columnsToSelect.append(columns[38])
    columnsToSelect.append('Our prediction')

    # ageList=df["age"].tail(200).tolist()
    print(columnsToSelect)
    #print(ageList)
    # policyList=df["policy number"].tail(200).tolist()
    # sexList=df["insured_sex"].tail(200).tolist()
    # education=df["insured_education_level"].tail(200).tolist()
    # occupation=df["insured_occupation"].tail(200).tolist()
    # state=df["incident_state"].tail(200).tolist()
    # city=df["incident_city"].tail(200).tolist()
    # location=df["incident_location"].tail(200).tolist()
    # fraud=df["fraud_reported"].tail(200).tolist()

    final_dict = {}
    required_cols = ["age","policy_number","insured_sex","insured_education_level","insured_occupation","incident_state","incident_city","incident_location","fraud_reported"]

    for i in required_cols:
        current_lst = list(df[i].tail(200))
        final_dict.update({i : current_lst,})
    print(final_dict)
    final_dict.update({'our_prediction': final_pred})
    print(final_dict)


    return final_dict


def analysis_chart_data():
    global final_pred
    df=pd.read_csv("dataset.csv")
    df = df.tail(200)
    fraud = len(df[df['fraud_reported'] == "Y"])
    not_fraud = 200 - fraud

    original_header = ["Fraud", "Not Fraud"]
    original_count = [fraud, not_fraud]

    print(original_count)


    not_fraud = final_pred.count(1)
    fraud = 200 - not_fraud

    predicted_count = [fraud, not_fraud]
    print(final_pred)
    print(predicted_count)

    return original_count,predicted_count


def analysis_accuracy():
    global accuracy
    accuracy_headers = ['DecisionTreeClassifier', 'LogisticRegression', 'RandomForestClassifier', 'MLPClassifier']

    return accuracy_headers, accuracy

get_data()
analysis_chart_data()
tableData()
