# такой скрипт нужно отправить ответом!!! В нём не нужно учить модельку.
# моделька поставляется вместе со скриптом, и загружается через pickle
# важно!!!! не подаётся колонка с фильмами!!!
# разрешено numpy, pandas, sklearn (мне влом ставить либы)
import pandas as pd
import argparse
import pickle


parser = argparse.ArgumentParser()
parser.add_argument("in_file")
parser.add_argument("out_file")
args = parser.parse_args()

data = pd.read_csv(args.in_file, parse_dates=["Отметка времени"]) #отчистка данных
data.rename(columns=dict(zip(data.columns.tolist(), ['time', 'sex', 'child_offence', 'vegan', 'dvach', 'gender', 'rest', 'games', 'series', 'books', 'antisemetism', 'subject', 'crimea', 'putin', 'english', 'old_days', 'films'])),inplace = True)
data.loc[data.sex != "Девочка", ["sex"]] = "0"
data.loc[data.sex == "Девочка", ["sex"]] = "1"
data.sex = data.sex.astype("int")
temp = pd.get_dummies(data.child_offence)
temp.rename(columns={"Не били": "child_offence_no", "Разве что по делу": "child_offence_infrequently", "Часто": "child_offence_often"}, inplace= True)
data = data.join(temp)
data = data.drop("child_offence", axis=1)
temp = pd.get_dummies(data.dvach)
temp.rename(columns={"Не знаю": "dvach_doesn't_know", "Ненавижу Абу": "dvach_hate_abu", "Паблик в вк": "dvach_vk_pub", "Лучшая борда рунета": "dvach_best_bord"}, inplace= True)
data = data.join(temp)
data = data.drop("dvach", axis=1)
temp = pd.get_dummies(data.gender)
temp.rename(columns={"Гетеро": "gender_hetero", "Би": "gender_bi", "Альтернативная": "gender_other"}, inplace= True)
data = data.join(temp)
data = data.drop("gender", axis=1)
data.loc[data.sex != "Гулять", ["rest"]] = "0"
data.loc[data.sex == "Гулять", ["rest"]] = "1"
data.rest = data.rest.astype("int")
data.antisemetism.unique()
temp = pd.get_dummies(data.antisemetism)
temp.rename(columns={"Нет": "antisemetism_no", "Я просто боюсь евреев": "antisemetism_afraid", "Да": "antisemetism_yes"}, inplace= True)
data = data.join(temp)
data = data.drop("antisemetism", axis=1)
temp = pd.get_dummies(data.subject)
temp.rename(columns=dict(zip(temp.columns.tolist(), ['subject_literature', 'subject_math', 'subject_IT', 'subject_history', 'subject_foreign_languages', 'subject_physics', 'subject_biology', 'subject_chemistry'])), inplace= True)
data = data.join(temp)
data = data.drop("subject", axis=1)
temp = pd.get_dummies(data.crimea)
temp.rename(columns={"Положительно": "crimea_yes", "Мне всё равно": "crimea_neutral", "Отрицательно": "crimea_no"}, inplace= True)
data = data.join(temp)
data = data.drop("crimea", axis=1)
data.loc[data.english == "Оригатоё гайзаймас", ["english"]] = "0"
data.loc[data.english == "Чуть лучше, чем ничего", ["english"]] = "1"
data.loc[data.english == "Нормально", ["english"]] = "2"
data.loc[data.english == "Хорошо", ["english"]] = "3"
data.loc[data.english == "Отлично", ["english"]] = "4"
data.loc[data.english == "НЭЙТИВ ИНГЛИШ СПИКЕР", ["english"]] = "5"
data.english = data.english.astype("int")
data.loc[data.old_days != "Нет", ["old_days"]] = "1"
data.loc[data.old_days == "Нет", ["old_days"]] = "0"
data.old_days = data.old_days.astype("int")
temp_borec = data.putin == "Политик, лидер и боец"
temp_molodec = data.putin == "Молодец"
data["putin_good"] = [0] * len(data.index)
data.loc[temp_borec | temp_molodec, ["putin_good"]] = 1
data["rebel"] = [0] * len(data.index)
data.loc[data.putin_good != 1, ["rebel"]] = 1
data = data.drop("putin", axis=1)
new_cols = ["films_action", "films_detective", "films_anime", "films_drama", "films_comedy", "films_melodrama", "films_historical", "films_tragedy", "films_horror", "films_fantasy"]
old_cols = ['Боевик', 'Детектив', 'Аниме', 'Драма', 'Комедия', 'Мелодрама', 'Историческийфильм', 'Трагедия', 'Фильмужасов', 'Фантастика']
for col in old_cols:
    data[col] = 0
for pers in data.index:
    temp = data.films[pers].split(",")
    for i in temp:
        data[i.replace(" ", "")][pers] = 1
data.rename(columns=dict(zip(old_cols, new_cols)),inplace = True)
data = data.drop("films", axis=1) #данные готовы

tree = pickle.load(open("tree.nn", "rb"))
result = tree.predict(data)

result.to_csv(args.out_file)

