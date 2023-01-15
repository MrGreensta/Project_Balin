import pandas as pd
import json
from typing import List, Dict
import matplotlib.pyplot as plt


def hrs_to_mins(time: str) -> int:
    '''Данная функция принимает строку, содержащую информацию о времени
    в различных форматах (количество часов или количество минут) и,
    если это необходимо, переводит значение в количество минут.
    При этом одна запись без указания total_time. Поэтому сказал, что для нее total_time = 0'''
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
    '''Данная функция удаляет дублирующиеся данные а также переводит столбец
    total_time в тип string, т.к. одна ячейка там пустая и имеет тип float (NaN)'''
    df = pd.read_csv('recipes_100.csv')
    df = df.iloc[0:31]
    df['total_time'] = df['total_time'].astype(str)
    return df


def find_ingredient(ings: str) -> Dict:
    '''Данная функция принимает строку с названием ингредиента и ищет совпадения
    в базе рецептов в колонке "ingredients" и возвращает словарь для записи в json файл'''
    if isinstance(ings, str) == False:
        return None
    recipes = only_unique()
    recipes = recipes[recipes["ingredients"].str.contains(f"{ings}")]["recipe_name"]
    if len(recipes) == 0 or len(ings) == 0:
        return None
    recipes_dict : Dict = {}
    recipes_dict[f'All recipes with {ings}'] = []
    recipes_dict[f'All recipes with {ings}'].append(list(recipes))
    return recipes_dict


assert find_ingredient(3) == None
assert find_ingredient("") == None


def large_time(num : int) -> Dict:
    '''Данная функция принимает значение (целое) количества рецептов, которое нужно 
    найти по условию - наибольшее время приготовления и возвращает словарь для записи в json'''
    if (isinstance(num, int) == False) or (num < 1 or num > 31):
        return None
    time_df = only_unique()
    time_df = time_df[['recipe_name','total_time']]
    for i in range(0, len(time_df)):
        time_df.loc[i, 'total_time'] = hrs_to_mins(time_df.loc[i, 'total_time'])
    time_df['total_time'] = time_df['total_time'].astype(int)
    top_time_df = time_df.nlargest(num, 'total_time')
    top_time_dict : Dict = {}
    top_time_dict = top_time_df.to_dict()
    return top_time_dict


assert large_time("3") == None
assert large_time(32) == None
assert large_time(0) == None
assert large_time(-5) == None
assert large_time(3.5) == None


def servings_or_rating(coloumn : str) -> Dict:
    '''Данная функция принимает строку с названием столбца: либо ""servings",
     либо "rating". Возвращает словарь, в котором для каждого значения выбранного 
     столбца (являются ключами) указаны названия блюд.'''
    if ((coloumn != 'servings') and (coloumn != 'rating')) or isinstance(coloumn, str) == False:
        return None
    s_r_df = only_unique()
    s_r_df = s_r_df.sort_values(by=coloumn, ascending=True)
    s_r_list : List = s_r_df[coloumn].unique()
    s_r_dict : Dict = {}
    for s_r in s_r_list:
        s_r_find_df = s_r_df[s_r_df[coloumn] == s_r]['recipe_name']
        if coloumn == 'servings':
            s_r_dict[f'{s_r} persons'] = []
            s_r_dict[f'{s_r} persons'].append(list(s_r_find_df))
        else:
            s_r_dict[f'rating {s_r}'] = []
            s_r_dict[f'rating {s_r}'].append(list(s_r_find_df))
    return s_r_dict


assert servings_or_rating('hi') == None
assert servings_or_rating(0) == None


with open('answers.json', 'w') as f:
    json.dump(find_ingredient("chicken"), f, indent=2)
    json.dump(large_time(3), f, indent=2)
    json.dump(servings_or_rating("servings"), f, indent=2)

hist_df = only_unique()
hist1 = hist_df['rating']
plt.hist(hist1, bins=32, edgecolor='black', label = 'Rating')
plt.xlabel('Rating of recipes')
plt.ylabel('Quantity of recipes')
plt.legend()
plt.savefig('hist.png')