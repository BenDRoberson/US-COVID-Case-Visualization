import pandas as pd
import csv
import os

dir = os.path.dirname(__file__)

def prep_data(data):
    data.columns = [x.lower() for x in data.columns]
    data = data[~data['state'].isin(['Guam', 'Virgin Islands', 'Puerto Rico', 'Northern Mariana Islands'])]
    return data

def data_overview(data):
    print(data.head())
    print(data.info())
    print("Number of Rows: " + str(data.shape[0]) + " and Number of Cols: " + str(data.shape[1]))
    return 1

################## Read in Cases File and Clean ########################
caseFile = os.path.join(dir, "Data", "us-states.txt")
caseData = pd.read_csv(caseFile, sep = ",", header = 0)
# Don't need fips
del caseData['fips']

caseData.rename(columns={'date':'case_date'}, inplace=True)

caseData = prep_data(caseData)
print(caseData.head())
print("Number of Rows: " + str(caseData.shape[0]) + " and Number of Cols: " + str(caseData.shape[1]))

print("---------------------Done Cases --------------------------")

################## Read in Reopening File and Clean ########################
reopenFile = os.path.join(dir, "Data", "NYT-State-Reopen-Data.csv")
reopenData = pd.read_csv(reopenFile, sep = ",", header = 0)

reopenData = prep_data(reopenData)
reopenData = reopenData[['state', 'state_abbreviation', 'status', 'restriction_start', 'restriction_end', 'status_details', 'external_link', 'population']]
del reopenData['restriction_start']

print(reopenData.head())
print("Number of Rows: " + str(reopenData.shape[0]) + " and Number of Cols: " + str(reopenData.shape[1]))

print("--------------------- Done Reopening --------------------------")

################## Read in Lockdown File and Clean ########################
lockdownFile = os.path.join(dir, "Data", "NYT-State-Lockdown-Data.csv")
lockdownData = pd.read_csv(lockdownFile, sep = ",", header = 0)

# Only keep the state-wide stay at home orders
lockdownData = lockdownData[lockdownData.County.isnull()]
lockdownData = prep_data(lockdownData)

lockdownData.rename(columns={'date':'lockdown_date'}, inplace=True)
# All NULL column and All US column
del lockdownData['county']
del lockdownData['country']

print(lockdownData.head())
print("Number of Rows: " + str(lockdownData.shape[0]) + " and Number of Cols: " + str(lockdownData.shape[1]))

print("-------------------- Done Lockdown ---------------------------")

################# Merge Data sets #####################
tempMergeDf = pd.merge(caseData, reopenData, on = "state")
finalDF = pd.merge(tempMergeDf, lockdownData, on = "state")

data_overview(finalDF)

finalDF = finalDF[['case_date', 'state', 'state_abbreviation', 'cases', 'deaths', 'status', 'lockdown_date', 'restriction_end', 'status_details', 'external_link', 'population', 'type']]

outputFile = os.path.join(dir, "Data", "Cleaned COVID State Data.csv")
finalDF.to_csv(outputFile, index = False)
