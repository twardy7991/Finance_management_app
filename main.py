import os
import pandas as pd

# Path to this script (main.py)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up to reach "Kalkulator finansowy"
PARENT_DIR = os.path.dirname(SCRIPT_DIR)

# Full path to the CSV file
csv_path = os.path.join(PARENT_DIR, "data", "lista_operacji.csv")

# Load the file
operations = pd.read_csv(csv_path, skiprows=25, delimiter=';')

