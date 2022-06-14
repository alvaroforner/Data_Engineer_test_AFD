import pandas as pd
import os
import requests

#Declaration of functions

def check_localdb(localdb):
  #Check if the DB exists, if not a new DB called Airlines_DB is created.
  try:
    df_db = pd.read_csv(localdb, sep=";")
    print("Database read successfully. You can proceed with the following steps")
  except:
    print("Database not found. A new database is generated.")
    df_db = database_generator(api)
    save_database(df_db, localdb)
    print("Database successfully generated. Name: Airlines_DB")
  return df_db 

#Function that generates the DB in case it is not found.
def database_generator(api):
  response = requests.get(api)
  response.json()["results"]
  airlines_db = pd.DataFrame(response.json()['results'])[['id', 'title',\
            'overview', 'popularity', 'release_date', 'vote_average', 'vote_count' ]]
  return airlines_db

#Function that saves in .CSV the last version of the DB.
def save_database(airlines_db, localdb):
  airlines_db.to_csv(localdb, sep=';', index = False, encoding='utf-8')

#Function that looks for the input parameter (ID) in API. In case that it does not exist restart the loop.
def buscador_id(api, input_parameter):
  response = requests.get(api)
  response.json()["results"]
  airlines_tmp = pd.DataFrame(response.json()['results'])[['id', 'title',\
            'overview', 'popularity', 'release_date', 'vote_average', 'vote_count' ]]
  fcond1 = airlines_tmp['id'] == input_parameter #checks if the id exists in the API.
  airlines_search = airlines_tmp[fcond1]
  if airlines_search.shape[0] != 0: #if it exists in the API the number of rows will be modistinct than 0
    print("Record found on the API")
    flag = True
    return airlines_search, flag
  else: 
    print("Idnetifier not located on the API")
    flag = False
    return airlines_search, flag

# Check if the register found on the API exists in local database, in case that it exists generates the mark "T", if not, generates the mark "F" in order to be able to update
#the attributes afterwards or add a new register.
def check_airline(df_db, input_parameter, airlines_search):
  def check_id(x, input_parameter):
    if x['id'] == input_parameter: #in case that the id already exists in the local DB, a mark is generated with "T" value
      res = "T"
    else:
      res = "F" # in case that the id does not exists in the local DB, a mark is generated with "F" value
    return res
  df_db['check'] = df_db.apply(lambda x: check_id(x, input_parameter), axis = 'columns')  
  fcond = df_db['check'] == "T"
  fcond2 = df_db['check'] == "F"
  
  if df_db[fcond].shape[0] != 0:
    print("[1] Identifier located in the Local Database")
    df_db = df_db[fcond2].copy()
    df_db.drop(['check'], axis=1, inplace = True)
    df_db = pd.concat([df_db, airline_search])
    print("[2] The register has been updated. ID: ", input_parameter)
    df_db.reset_index(drop =True, inplace = True)
  else: 
    print("[1] Identifier not found in the database")
    print("[2] New record is inserted in the local database. ID: ", input_parameter)
    df_db.drop(['check'], axis=1, inplace = True)
    df_db = pd.concat([df_db, airline_search])
    df_db.reset_index(drop =True, inplace = True)
  save_database(df_db, localdb)
  # Global variables
api =  "https://api.themoviedb.org/3/movie/top_rated?api_key=d73d7e5e4c1dda40808ef100a89f97c1&language=en-US&page=1"
localdb = 'airlines_db.txt'
flag_success = False
# ***************
# Step I 
# ***************
# The Check_Localdb function is called, which checks if the DB exists locally, if it does, an ID is requested, if it does not exist, it creates the DB and requests an ID.
df_db = check_localdb(localdb)
while (flag_success == False):
  input_parameter = input("Enter an Airline ID: ")
  input_parameter = int(input_parameter)
# ***************
# Step II
# ***************
# The function buscador_id is called, which will search in the API the ID previously entered and will return 2 things: all the attributes associated with that ID and the flag 
# indicating if it has been able to locate it or not.

  buscador = buscador_id(api, input_parameter)
  airline_search = buscador[0]
  flag_search = buscador[1]
# ***************
# Step III 
# ***************

  if flag_search == True:
    check_airline(df_db, input_parameter, airline_search)
    flag_success = True
  else: pass
