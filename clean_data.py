import pandas as pd
import numpy as np

years = range(1880,2015)

print("Reading data")

def read_one_year(year):
    path = 'data/yob%d.txt' % year
    one_year_data = pd.read_csv(path, names=['Name','Gender','Births'])
    one_year_data['Year'] = year
    return one_year_data

names_data = pd.concat([read_one_year(year) for year in years])

print(names_data.head())
names_data.to_csv('data/names_cleaned.csv', index=False)

# Get the 19x0s, 2000s, 2010s dataframe
print("Generating summary by decade")

def convert_year_to_decade(year):
    return '%i0' % np.floor(year/10)

names_data['Decade'] = names_data['Year'].apply(convert_year_to_decade)

names_by_decade = names_data.groupby(['Name', 'Gender', 'Decade'])['Births'].sum().reset_index()
names_by_decade['Rank'] = names_by_decade.groupby(['Gender','Decade'])['Births'].rank(method='first',
                                                                                      ascending=False)
names_by_decade.to_csv('data/names_by_decade.csv', index=False)