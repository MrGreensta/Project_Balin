import pandas as pd


def hrs_to_mins(time: str) -> int:

    '''Данная функция принимает строку, содержащую информацию о времени
    в различных форматах (количество часов или количество минут) и,
    если это необходимо, переводит значение в количество минут'''

    if len(time) == 0: # Т.к. в базе есть 4 одинаковых записи без указания времени.
        return None
    time_list = time.split()
    if time_list[1] == "mins":
        mins = int(time_list[0])
    else:
        mins = int(time_list[0]) * 60
        mins += int(time_list[2])
    return mins


assert hrs_to_mins("") == None
assert hrs_to_mins("0 mins") == 0
assert hrs_to_mins("10 mins") == 10
assert hrs_to_mins("1 hrs 5 mins") == 65


df = pd.read_csv('recipes_100.csv')

