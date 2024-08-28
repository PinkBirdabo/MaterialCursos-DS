import pandas as pd # download library to read data into dataframe
import numpy as np  # import numpy library
import re           # import library for regular expression
import random       # library for random number generation
pd.set_option('display.max_columns', None)

# Initial load
recipes = pd.read_csv('recipes4.csv')
print("Data read into dataframe!")  # takes about 30 seconds
print(recipes.iloc[:5, :7])
print("\nINFO OF CSV")
print(recipes.shape)

# START OF FIXING
# Fix name of column
column_names = recipes.columns.values
column_names[0] = "cuisine"     # column[0] because its the location of the "Country" column
recipes.columns = column_names
print("\n COLUMN NAMES FIXED!")

# Change cuisine names to all lowercase
recipes["cuisine"] = recipes["cuisine"].str.lower()
print(" FIXED ALL CUISINES NAMES TO LOWERCASE!")

# Make cuisine names consistent
recipes.loc[recipes["cuisine"] == "austria", "cuisine"] = "austrian"    # pd.loc[row, column] in this case
recipes.loc[recipes["cuisine"] == "belgium", "cuisine"] = "belgian"
recipes.loc[recipes["cuisine"] == "china", "cuisine"] = "chinese"
recipes.loc[recipes["cuisine"] == "canada", "cuisine"] = "canadian"
recipes.loc[recipes["cuisine"] == "netherlands", "cuisine"] = "dutch"
recipes.loc[recipes["cuisine"] == "france", "cuisine"] = "french"
recipes.loc[recipes["cuisine"] == "germany", "cuisine"] = "german"
recipes.loc[recipes["cuisine"] == "india", "cuisine"] = "indian"
recipes.loc[recipes["cuisine"] == "indonesia", "cuisine"] = "indonesian"
recipes.loc[recipes["cuisine"] == "iran", "cuisine"] = "iranian"
recipes.loc[recipes["cuisine"] == "italy", "cuisine"] = "italian"
recipes.loc[recipes["cuisine"] == "japan", "cuisine"] = "japanese"
recipes.loc[recipes["cuisine"] == "israel", "cuisine"] = "israeli"
recipes.loc[recipes["cuisine"] == "korea", "cuisine"] = "korean"
recipes.loc[recipes["cuisine"] == "lebanon", "cuisine"] = "lebanese"
recipes.loc[recipes["cuisine"] == "malaysia", "cuisine"] = "malaysian"
recipes.loc[recipes["cuisine"] == "mexico", "cuisine"] = "mexican"
recipes.loc[recipes["cuisine"] == "pakistan", "cuisine"] = "pakistani"
recipes.loc[recipes["cuisine"] == "philippines", "cuisine"] = "philippine"
recipes.loc[recipes["cuisine"] == "scandinavia", "cuisine"] = "scandinavian"
recipes.loc[recipes["cuisine"] == "spain", "cuisine"] = "spanish_portuguese"
recipes.loc[recipes["cuisine"] == "portugal", "cuisine"] = "spanish_portuguese"
recipes.loc[recipes["cuisine"] == "switzerland", "cuisine"] = "swiss"
recipes.loc[recipes["cuisine"] == "thailand", "cuisine"] = "thai"
recipes.loc[recipes["cuisine"] == "turkey", "cuisine"] = "turkish"
recipes.loc[recipes["cuisine"] == "vietnam", "cuisine"] = "vietnamese"
recipes.loc[recipes["cuisine"] == "uk-and-ireland", "cuisine"] = "uk-and-irish"
recipes.loc[recipes["cuisine"] == "irish", "cuisine"] = "uk-and-irish"
print(" FIXED CUISINES DUPLICATED VARIATIONS!")

# Remove cuisines with < 50 recipes
recipes_counts = recipes["cuisine"].value_counts()  # returns number of recipes of each cuisine
cuisine_indexes = recipes_counts > 50               # returns True/False of cuisines with > 50 recipes
cuisines_to_keep = list(np.array(recipes_counts.index.values)[np.array(cuisine_indexes)])   # returns list of the names of cuisines with > 50 recipes

rows_before = recipes.shape[0]  # number of rows of original dataframe
print("\n Number of rows of original dataframe is {}.".format(rows_before))

recipes = recipes.loc[recipes['cuisine'].isin(cuisines_to_keep)]    # code to remove cuisines of < 50 recipes in the original dataframe
rows_after = recipes.shape[0]   # number of rows of processed dataframe
print(" Number of rows of processed dataframe is {}.".format(rows_after))
print(" {} rows removed!".format(rows_before - rows_after))

print(" REMOVED CUISINES WITH < 50 RECIPES!\n")
print(recipes.iloc[:10, :7])

# Convert Yes/No to 1/0
recipes = recipes.replace(to_replace="Yes", value=1)
recipes = recipes.replace(to_replace="No", value=0)
print(" FIXED ALL YES/NO TO BINARY!\n")
#FINISH OF FIXING

# DATA MODELING
# Mucho pedo el graphviz, toca pura teoría

