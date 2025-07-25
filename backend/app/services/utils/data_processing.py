from app.database.models import Operation

import pandas as pd
from typing import BinaryIO, List
from datetime import date, datetime

class DataProcessor:
    
    def __init__(self, operations : pd.DataFrame):
        
        self.operations : pd.DataFrame = operations
    
    def _preprocess_file(self):
    
        self._correct_datatypes()
        self._extract_currency()
        self._delete_unused_columns()

    def _correct_datatypes(self):
        
        self.operations["#Data operacji"] = pd.to_datetime(self.operations["#Data operacji"])
        self.operations.sort_values("#Data operacji", ascending=False, inplace=True)
        
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
    
def process_file(operations : BinaryIO) -> pd.DataFrame:
        
    processor = DataProcessor(pd.read_csv(operations, skiprows=25, sep=";"))
    processor._preprocess_file()
    print(processor.operations)
    processor._correct_categories()
    print(processor.operations)
    return processor.operations
        
def get_unsaved_operations(saved_operations : List[Operation], new_operations : pd.DataFrame) -> pd.DataFrame:
    
    saved_operations : pd.DataFrame = pd.DataFrame([[o.operation_date, o.category, o.description, o.value, o.currency] for o in saved_operations], columns=["#Data operacji","#Kategoria","#Opis operacji","Kwota","Waluta"])
    saved_operations["#Data operacji"] = pd.to_datetime(saved_operations["#Data operacji"])
    saved_operations["Kwota"] = saved_operations["Kwota"].astype(float)

        
    # print(saved_operations.dtypes)
    # print(new_operations.dtypes)
    
    # print(saved_operations)
    # print(new_operations)

    merged_df = new_operations.merge(saved_operations, how='left', indicator=True)

    operations_to_add = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge'])

    # print(operations_to_add)
    return operations_to_add

def date_to_int(operations : List[Operation]):
    
        interval = 86400.0
        
        determinant = datetime.strptime(str(operations[0].operation_date), '%Y-%m-%d').timestamp()
        
        data = [[(datetime.strptime(str(o.operation_date), '%Y-%m-%d').timestamp() - determinant) / interval, float(o.value)] for o in operations]
        
        return data
    
