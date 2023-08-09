from datetime import datetime
import json



def formatting_time(result_time):
    """формотирование  время '%H:%M:%S,%f' в строку '%M:%S,%f'"""
    minut = str(result_time).split(":")[1]
    sec = str(result_time).split(":")[1]
    microsec = str(result_time).split(".")[1][:2]   
    return str(minut+':'+sec+','+microsec)


def result_sportsman(data_file):
    """Подсчитывает результат времени"""
    with open(data_file, encoding='utf-8-sig') as data:
        # распаковка файла в список
        data_sportsman = [i.split() for i in data]  
    # разбиение по спискам
    data_sportsman_2 = [[data_sportsman[i], data_sportsman[i+1]] for i in range(0, len(data_sportsman), 2)]
    sort_list_sp = list() 
    format = "%H:%M:%S,%f"
    for item in data_sportsman_2:
        result_time_sportsman = datetime.strptime(item[1][2], format) - datetime.strptime(item[0][2], format)
        item[0][2] = str(result_time_sportsman)
        sort_list_sp.append([0,item[0][0],item[0][2]])

    lenght = len(sort_list_sp) 
    count = 1
    # Сортировка времени по возростанию
    for run in range(lenght-1):
        for item in range(lenght-1):
            if sort_list_sp[item][2] > sort_list_sp[item+1][2]:
                sort_list_sp[item], sort_list_sp[item+1] = sort_list_sp[item+1], sort_list_sp[item]  
    # Форматирование время в '%M:%S,%f'      
    for i in sort_list_sp:
        result_time = formatting_time(i[2])
        i[2] = result_time
        i[0] = str(count)  # Счетчик занятого места
        count += 1
    return sort_list_sp
        
 
def forming_data_sportsmen(file_json):
    """формирование данные о спортсмене"""
    with open(file_json) as dt_json:
        data = json.load(dt_json)
    sportsman_data = list()
    sp_time = result_sportsman('results_RUN.txt')
    for item in sp_time:
        for name in data:
            if item[1] == name:
                sportsman_data.append([item[0], name, data[name]['Surname'], data[name]['Name'], item[2]])
            continue
    return sportsman_data


def output_sportsman_table(fail_json):
    """Вывод списка в виде таблицы"""
    sp_data = forming_data_sportsmen(fail_json)
    columns = ["место", "номер", "Имя", "Фамилия", "Время"]
    # расчёт максимальной длинны колонок
    max_columns = [] 
    for col in zip(*sp_data):
        len_el = []
        [len_el.append(len(el)) for el in col]
        max_columns.append(max(len_el))
    # печать таблицы с колонками максимальной длинны строки
    # печать шапки таблицы
    for column in columns:
        print(f'{column:{max(max_columns)+1}}', end='')
    print()
    # печать разделителя шапки
    print(f'{"="*max(max_columns)*5}')
    # печать тела таблицы
    for el in sp_data:
        for col in el:
            print(f'{col:{max(max_columns)+1}}', end='')
        print()

if __name__ == "__main__":
    output_sportsman_table('competitors2.json')