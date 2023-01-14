import pandas as pd
import json
from typing import List, Dict


def hrs_to_mins(time: str) -> int:
    '''Данная функция принимает строку, содержащую информацию о времени
    в различных форматах (количество часов или количество минут) и,
    если это необходимо, переводит значение в количество минут.
    При этом одна запись без указания total_time. Поэтому сказал, что для нее total_time = 0.'''
    if time == 'nan':
        mins : int = 0
    else:
        time_list : List = time.split()
        if time_list[1] == "mins":
            mins = int(time_list[0])
        else:
            mins = int(time_list[0]) * 60
            if len(time_list) == 4:
                mins += int(time_list[2])
    return mins


assert hrs_to_mins("nan") == 0
assert hrs_to_mins("0 mins") == 0
assert hrs_to_mins("10 mins") == 10
assert hrs_to_mins("1 hrs") == 60
assert hrs_to_mins("1 hrs 5 mins") == 65


def only_unique():
    '''Данная функция удаляет дублирующиеся данные'''
    df = pd.read_csv('recipes_100.csv')
    df = df.iloc[0:31]
    df['total_time'] = df['total_time'].astype(str)
    return df


def find_ingredient(ings: str) -> Dict:
    '''Данная функция принимает строку с названием ингредиента и ищет совпадения
    в базе рецептов в колонке "ingredients" и возвращает словарь для записи в json файл'''
    recipes = only_unique()
    recipes = recipes[recipes["ingredients"].str.contains(f"{ings}")]["recipe_name"]
    if len(recipes) == 0 or len(ings) == 0:
        return None
    recipes_dict : Dict = {}
    recipes_dict[f'All recipes with {ings}'] = []
    recipes_dict[f'All recipes with {ings}'].append(list(recipes))
    return recipes_dict


assert find_ingredient("") == None
assert find_ingredient("chicken") == {'All recipes with chicken': [['Mulligatawny Soup']]}


def large_time(num : int) -> Dict:
    '''Данная функция принимает значение количества рецептов, которое нужно 
    найти по условию - наибольшее время приготовления и возвращает словарь для записи в json.'''
    time_df = only_unique()
    time_df = time_df[['recipe_name','total_time']]
    for i in range(0, len(time_df)):
        time_df.loc[i, 'total_time'] = hrs_to_mins(time_df.loc[i, 'total_time'])
    time_df['total_time'] = time_df['total_time'].astype(int)
    top_time_df = time_df.nlargest(num, 'total_time')
    top_time_dict = {}
    top_time_dict : Dict = top_time_df.to_dict()
    return top_time_dict


with open('answers.json', 'w') as f:
    json.dump(find_ingredient("chicken"), f, indent=2)
    json.dump(large_time(3), f, indent=2)
