import pandas as pd # download library to read data into dataframe
import numpy as np  # import numpy library
import re           # import library for regular expression
pd.set_option('display.max_columns', None)

# Initial load
recipes = pd.read_csv('recipes3.csv')
print("Data read into dataframe!")  # takes about 30 seconds
print(recipes.head())
print("\nINFO OF CSV")
print(recipes.shape)

# DATA UNDERSTANDING

# Check if Rice, Soy Sauce, Wasabi, Seaweed exists in dataframe
ingredients = list(recipes.columns.values)
print("\n CHECK IF JAPANESE INGREDIENTS EXIST IN DATAFRAME")
print([match.group(0) for ingredient in ingredients for match in [(re.compile(".*(rice).*")).search(ingredient)] if match])
print([match.group(0) for ingredient in ingredients for match in [(re.compile(".*(wasabi).*")).search(ingredient)] if match])
print([match.group(0) for ingredient in ingredients for match in [(re.compile(".*(soy).*")).search(ingredient)] if match])
print([match.group(0) for ingredient in ingredients for match in [(re.compile(".*(seaweed).*")).search(ingredient)] if match])

# DATA PREPARATION

# Check if data needs cleaning
print(recipes["country"].value_counts())    # frequency table
# As we can see: 
# 1) the label of Country is inaccurate and should be Cuisine 
# 2) the starting letter of the cuisine names are not consistent (uppercase/lowercase) 
# 3) some cuisines have duplicated variations (ex. Vietnam and Vietnamese) 
# 4) some cuisines have few recipes

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
# FINISH OF FIXING

# Now, we check if the recipes that contain (Rice, Soy, Wasabi, Seaweed) are Japanese
check_recipes = recipes.loc[
    (recipes["rice"] == 1) &
    (recipes["soy_sauce"] == 1) &
    (recipes["wasabi"] == 1) &
    (recipes["seaweed"] == 1)
]
print(check_recipes.iloc[:, :7])
# As we can see, using these parameters, it tell us that there are only 5 Japanese recipes which is false, as well as taking to account Asian and East Asian recipes.

# Lets count the ingredients across all recipes
print("\n COUNT INGREDIENTS ACROSS ALL RECIPES")
ing = recipes.iloc[:, 1:].sum(axis=0)   # sum each column
# define each column as a pandas series
ingredient = pd.Series(ing.index.values, index = np.arange(len(ing)))
count = pd.Series(list(ing), index = np.arange(len(ing)))
# create the dataframe
ing_df = pd.DataFrame(dict(ingredient = ingredient, count = count))
ing_df = ing_df[["ingredient", "count"]]
# sort in descending order
ing_df.sort_values(["count"], ascending=False, inplace=True)
ing_df.reset_index(inplace=True, drop=True)
print(ing_df)
# As we can see, there are a lot of western ingredients due to the abundance of American recipes (~40,000), creating a bias.

# Lets check the mean of each ingredient
cuisines_mean = recipes.groupby("cuisine").mean()
print("\n LIST OF THE MEAN OF INGREDIENTS PER CUISINE")
print(cuisines_mean.iloc[:,:5])

# Display top ingredients of each cuisine
num_ingredients = 5
# define a function that prints the top ingredients for each cuisine
def print_top_ingredients(row):
    print(row.name.upper())
    row_sorted = row.sort_values(ascending=False)*100
    top_ingredients = list(row_sorted.index.values)[0:num_ingredients]
    row_sorted = list(row_sorted)[0:num_ingredients]

    print("\n LIST OF TOP INGREDIENTS PER CUISINE")
    for ind, ingredient in enumerate(top_ingredients):
        print("%s (%d%%)" % (ingredient, row_sorted[ind]), end=' ')
    print("\n")

# apply function to cuisines dataframe
create_cuisines_profiles = cuisines_mean.apply(print_top_ingredients, axis=1)