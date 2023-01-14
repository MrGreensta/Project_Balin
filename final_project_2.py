import pandas as pd
import json
from typing import List, Dict


def hrs_to_mins(time: str) -> int:
    '''Данная функция принимает строку, содержащую информацию о времени
    в различных форматах (количество часов или количество минут) и,
    если это необходимо, переводит значение в количество минут'''
    if len(time) == 0: # Т.к. в базе есть 4 одинаковых записи без указания времени.
        return None
    time_list : List = time.split()
    if time_list[1] == "mins":
        mins : int = int(time_list[0])
    else:
        mins = int(time_list[0]) * 60
        if len(time_list) == 4:
            mins += int(time_list[2])
    return mins


assert hrs_to_mins("") == None
assert hrs_to_mins("0 mins") == 0
assert hrs_to_mins("10 mins") == 10
assert hrs_to_mins("1 hrs") == 60
assert hrs_to_mins("1 hrs 5 mins") == 65


def find_ingredient(ings: str) -> Dict:
    '''Данная функция принимает строку с названием ингредиента и ищет совпадения
    в базе рецептов в колонке "ingredients" и возвращает словарь для записи в json файл'''
    df = pd.read_csv('recipes_100.csv')
    df = df.iloc[0:31]  # Оставил только уникальные строки
    recipes = df[df["ingredients"].str.contains(f"{ings}")]["recipe_name"]
    if len(recipes) == 0 or len(ings) == 0:
        return None
    recipes_dict : Dict = {}
    recipes_dict[f'All recipes with {ings}'] = []
    recipes_dict[f'All recipes with {ings}'].append(list(recipes))
    return recipes_dict


assert find_ingredient("") == None
assert find_ingredient("chicken") == {'All recipes with chicken': [['Mulligatawny Soup']]}


df = pd.read_csv('recipes_100.csv')
df = df.iloc[0:31] # Оставил только уникальные значения
time_df = df[['recipe_name','total_time']]
pd.options.mode.chained_assignment = None
for i in range(1, len(time_df)):
    time_df.loc[i, 'total_time'] = hrs_to_mins(time_df.loc[i, 'total_time'])
time_df['total_time'] = time_df['total_time'].astype(float)
top_time_df = time_df.nlargest(3, 'total_time')
top_time_dict : Dict = top_time_df.to_dict()

with open('answers.json', 'w') as f:
    json.dump(find_ingredient("chicken"), f, indent=2) # ,sort_keys=True
    json.dump(top_time_dict, f, indent=2)
    