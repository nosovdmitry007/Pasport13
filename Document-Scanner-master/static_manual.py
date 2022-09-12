import csv
import pandas as pd
def to_csv(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "static_poly1.csv"
  with open(path, 'a+', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols)
    if f.tell() == 0:
        wr.writeheader()
    wr.writerows(data)


def static_manual(df_manual, dt):


    spis_m = ['issued_by_whom',	'date_of_issue',	'unit_code',	'series_and_number_1',	'surname',	'first_name',	'patronymic',	'gender',	'date_of_birth',	'place_of_birth']
    spis = ['issued_by_whom',	'date_of_issue',	'unit_code',	'series_and_number',	'surname',	'first_name',	'patronymic',	'gender',	'date_of_birth',	'place_of_birth']
    nebrat = '10167 10191 10188 10125 10134 10148'
    toch_s=0
    kol=0
    data = {}
    data['static'] = []
    d = {}
    for  i in range(1,df_manual.shape[0]): #цикл по файлу с ручным вводом
      if df_manual.loc[i]['ID'] != nebrat:
        for j in range(0,dt.shape[0]): #цик по файлу с авто вводом

          if df_manual.loc[i]['ID'] == dt.loc[j]['ID']:

            #разбиваем посимвольно каждую ячейку
            for pole in spis:

              if dt.loc[j][pole] == 'FALSE':
                pol=''
                l_pol = 0
              else:

                pol = list(dt.loc[j][pole])
                l_pol = len(pol)

              if pole == 'series_and_number':

                if df_manual.loc[i]['series_and_number_1'] =='FALSE':
                  pol=''
                  l_pol_m = 0
                else:
                  pol_m = list(df_manual.loc[i]['series_and_number_1'].upper())
                  l_pol_m = len(pol_m)
              else:
                if df_manual.loc[i][pole] == '':
                  pol_m=''
                  l_pol_m = 0
                else:
                  pol_m = list(df_manual.loc[i][pole].upper())
                  l_pol_m = len(pol_m)

              if pol == pole:
                d[pole] = 1
              else:
                d[pole] = 0
            print(d)
            data['static'].append(d)
            to_csv(data['static'])

              # t=0
              # l=0
              # #проверяем длину каждого списка и выбираем минимальный
              #
              # l=min(l_pol,l_pol_m)
              # #проверям соответствие символов по порядку
              # for k in range(0,l):
              #
              #   if pol[k] == pol_m[k]:
              #     t+=1
              # #считаем точность
              # if l_pol_m == 0:
              #   if l_pol_m == l_pol:
              #     toch = 1
              #   else:
              #     toch = 0
              # else:
              #   toch = t/l_pol_m
              #   kol+=1
              #
              # toch_s+=toch

            # continue

    print('Точность распознания: ')

dt = pd.read_csv('data_many3.csv')
print(dt)
df_manual = pd.read_csv('data_manual.csv')
print(df_manual)
dt=dt.fillna('FALSE')
df_manual=df_manual.fillna('FALSE')
static_manual(df_manual,dt)
