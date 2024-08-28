import pandas as pd # download library to read data into dataframe
recipes = pd.read_csv('recipes.csv')

# Printing stuff
print("\n Data read into dataframe!\n\n FIRST 5 ROWS") # takes about 30 seconds
print(recipes.head())   # First 5 rows of the dataframe
print("\nINFO OF CSV")
print(recipes.shape)    # Dimensions of the dataframe