import pandas as pd
from app.services.connection import Connection
from typing import BinaryIO
import io

class DataProcessor:
    
    def __init__(self, operations : pd.DataFrame):
        
        self.operations : pd.DataFrame = operations
    
    def _preprocess_file(self):
    
        self._correct_datatypes()
        self._extract_currency()
        self._delete_unused_columns()

    def _correct_datatypes(self):
        
        self.operations["#Data operacji"] = pd.to_datetime(self.operations["#Data operacji"])
        
        self.operations["#Kategoria"] = self.operations["#Kategoria"].apply(lambda x: str(x))
        
    def _extract_currency(self):
        
        self.operations[['Kwota', 'Waluta']] = self.operations['#Kwota'].str.extract(r'([-\d,\.]+)\s*(\D+)')
        
        self.operations["Kwota"] = self.operations["Kwota"].str.replace(',','.').astype('float')

    def _delete_unused_columns(self):
        
        self.operations.drop(columns=self.operations.columns[[2,4,5,6]], inplace=True)
        
    def _correct_categories(self):
        
        self._extract_correct_categories()
        self._fill_missing_categories()

    def _extract_correct_categories(self):
        
        self.operations.loc[
            self.operations["#Opis operacji"].str.contains(r'\bBLIK P2P\b', regex=True), "#Kategoria"
        ] = "BLIK"

        self.operations.loc[
            self.operations["#Opis operacji"].str.contains(r'\b\bPRZELEW|przelew\b\b', regex=True), "#Kategoria"
        ] = "PRZELEW"
    
        self.operations["#Opis operacji"] = self.operations["#Opis operacji"].str.strip()
    
    def _fill_missing_categories(self):
        
        # categories = self.operations["#Kategoria"].unique().tolist()
        
        # conn = Connection()
        
        # for index in self.operations.index[self.operations["#Kategoria"] == "Bez kategorii"]:
        #     response = conn.category_definition_gemini(self.operations.at[index, "#Opis operacji"], categories=categories)
        #     self.operations.at[index, "#Kategoria"] = response
        
        return self
    
def process_file(operations : BinaryIO):
        
    processor = DataProcessor(pd.read_csv(operations, skiprows=25, sep=";"))
    processor._preprocess_file()
    print(processor.operations)
    processor._correct_categories()
    print(processor.operations)
    return processor.operations
        
def get_unsaved_operations(saved_operations : pd.DataFrame, new_operations : pd.DataFrame) -> pd.DataFrame:
    
    operations_to_add = new_operations[~new_operations.apply(tuple, 1).isin(pd.DataFrame(saved_operations).apply(tuple, 1))].reset_index(drop=True)
    
    return operations_to_add
        