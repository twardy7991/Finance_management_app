import pandas as pd
from connection import Connection

class DataProcessor:
    
    def __init__(self):
        pass
    
    def process_file(path):
        operations = pd.read_csv(path, skiprows=25, delimiter=';')
        
        operations["#Data operacji"] = pd.to_datetime(operations["#Data operacji"])
        
        operations.drop(columns=operations.columns[[2,5,6]], inplace=True)
        
        operations[['Kwota', 'Waluta']] = operations['#Kwota'].str.extract(r'([-\d,\.]+)\s*(\D+)')
        
        operations.drop(columns=["#Kwota"], inplace=True)
        
        operations["#Kategoria"] = operations["#Kategoria"].apply(lambda x: str(x))
        
        operations.loc[
            operations["#Opis operacji"].str.contains(r'\bBLIK P2P\b', regex=True), "#Kategoria"
        ] = "BLIK"

        operations.loc[
            operations["#Opis operacji"].str.contains(r'\b\bPRZELEW|przelew\b\b', regex=True), "#Kategoria"
        ] = "PRZELEW"
        
        operations["#Opis operacji"] = operations["#Opis operacji"].str.strip()
        
        categories = operations["#Kategoria"].unique().tolist()
        
        conn = Connection()
        
        for index in operations.index[operations["#Kategoria"] == "Bez kategorii"]:
            response = conn.category_definition_gemini(operations.at[index, "#Opis operacji"], categories=categories)
            operations.at[index, "#Kategoria"] = response

        operations["Kwota"] = operations["Kwota"].str.replace(',','.')
        
        operations["Kwota"] = operations["Kwota"].astype('float')
        
        
        
        