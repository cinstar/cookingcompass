import pandas as pd

ingredient_bank = ['tomato', 'tofu', 'garlic', 'onion', 'potato']

print("Select the ingredient you have:")
for idx, item in enumerate(ingredient_bank):
    print(f"{idx}: {item}")
input_idx = int(input())

df = pd.read_csv('recipes.csv')

print("You select this ingredient:", ingredient_bank[input_idx])

recipe_count = 0
recipe_list = []

for row in df:
    # if row['ingredients']
    pass

print("Here are recipes with that ingredient:")