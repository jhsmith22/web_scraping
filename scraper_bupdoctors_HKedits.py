import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

state=['AK', 'AL', 'AR','AZ', 'CA','CO','CT','DC','DE','FL','GA','HI','IA','ID','IL','IN','KS','KY','LA','MA','MD','ME','MI','MN','MO','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VA','VT','WA','WI','WV','WY']

df = pd.DataFrame()
url = 'https://www.samhsa.gov/medication-assisted-treatment/physician-program-data/certified-physicians?field_bup_us_state_code_value='

for s in state:

    # Construct url
    website = url + s

    # Fetch website html and soupify
    page = requests.get(website)
    soup = BeautifulSoup(page.content, 'html.parser')

    #1. Waiver 30 Physician - Create a List of Doctor Counts for all Years 2002-2018
    content = soup.findAll('div', class_ = "views-field views-field-field-bup-certification-30")
    doctors = [str(j)[-18:-13] for j in content]
    doctors = ([s.strip('>' 'g' '') for s in doctors]) # remove unwanted characters
      
    #2. Identify Year     
    year = soup.find_all('span', class_ = "field-content")
    year30, k = [], 0
    while k < len(year):
        year30.append(str(year[k])[-11:-7])
        k += 2
   
    # Create dataframe (combine lists from each state)
    df["Year"]  = year30
    df[s] = doctors
    
#export csv
df.to_csv('bupdoctors.csv',index=False)
df.head()
