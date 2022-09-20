import csv
import pandas as pd
from jiwer import wer
from tqdm import tqdm
def to_csv(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "static_poly_baza_8.csv"
  with open(path, 'a+', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols)
    if f.tell() == 0:
        wr.writeheader()
    wr.writerows(data)

def static_manual(df_manual, dt):
    spis = ['issued_by_whom',	'date_of_issue',	'unit_code',	'series_and_number',	'surname',	'first_name',	'patronymic',	'gender',	'date_of_birth',	'place_of_birth']
    nebrat = '0'
    kol=0
    data = {}
    data['static'] = []
    data['static_obr'] = []
    d = {}
    sred_ver = 0
    col_ver = 0
    for  i in tqdm(range(1,df_manual.shape[0])): #цикл по файлу с ручным вводом
      if df_manual.loc[i]['ID'] != nebrat:
        # print(df_manual.loc[i]['ID'])
        for j in range(0,dt.shape[0]): #цик по файлу с авто вводом

          if df_manual.loc[i]['ID'] == dt.loc[j]['ID']:
            kol+=1
            d['ID'] = df_manual.loc[i]['ID']
            #разбиваем посимвольно каждую ячейку
            for pole in spis:

              pol = list(dt.loc[j][pole])


              if pole == 'series_and_number':

                if df_manual.loc[i]['series_and_number_1'] =='FALSE':
                  pol=''

                else:
                  pol_m = list(df_manual.loc[i]['series_and_number_1'].upper())

              else:
                if len(df_manual.loc[i][pole])== 0:
                  pol_m=''

                else:
                  pol_m = list(df_manual.loc[i][pole].upper())

              pol = ''.join(pol)
              pol_m = ''.join(pol_m)

              if len(pol) <= 1:
                  pol = 'jhubvg'
              elif len(pol_m) <= 1:

                  pol_m = 'tufyvb'

              pol = str(pol).replace('.', '').replace('-', ' ').replace('–', ' ').replace('  ', ' ')

              pol_m = str(pol_m).replace('.', '').replace('-', ' ').replace('–', ' ').replace('  ', ' ')

              ver = wer(pol.upper(),pol_m.upper())

              sred_ver +=ver
              col_ver +=1
              d[pole] = ver

            data['static'].append(d)

            d = {}

            continue
          continue
    to_csv(data['static'])
    # to_csv(data['static_obr'])
    print(f'Точность распознания на {kol} фотографиях: ', round(sred_ver/col_ver,4))
    # print('Точность распознания obr: ', )
dt = pd.read_csv('data_auto_baza_8.csv')

df_manual = pd.read_csv('data_manual.csv')

dt=dt.fillna('FALSE')
df_manual=df_manual.fillna('FALSE')
static_manual(df_manual, dt)
