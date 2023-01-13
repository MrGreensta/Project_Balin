import pandas as pd
import json


# Заметил, что записи дублируются по 3-4 раза, доказательства ниже :)
df = pd.read_csv('recipes_100.csv')
# Убрал все дубликаты для каждого 'recipe_name' по колонке 'directions'.
unique_dict = df.drop_duplicates().set_index('recipe_name')['directions'].to_dict()

unique_list = list(unique_dict.keys())
unique_list.append(f'Total Unique Values: {len(unique_dict.keys())}')

with open('unique_recipes.json', 'w') as f:
    json.dump(unique_list, f, indent=4, sort_keys=True)
