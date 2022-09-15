import csv
import pandas as pd
def to_csv(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "static_poly_123.csv"
  with open(path, 'a+', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols)
    if f.tell() == 0:
        wr.writeheader()
    wr.writerows(data)

def to_csv_obr(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "static_poly_obr.csv"
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
    data['static_obr'] = []
    d = {}
    d_obr = {}
    sred_ver = 0
    col_ver = 0
    sred_ver_obr = 0
    col_ver_obr = 0
    for  i in range(1,df_manual.shape[0]): #цикл по файлу с ручным вводом
      if df_manual.loc[i]['ID'] != nebrat:
        for j in range(0,dt.shape[0]): #цик по файлу с авто вводом

          if df_manual.loc[i]['ID'] == dt.loc[j]['ID']:
            d['ID'] = df_manual.loc[i]['ID']
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
              col = 0
              sim = 0
              col_obr = 0
              sim_obr = 0
              pol = ''.join(pol)
              pol_m = ''.join(pol_m)
              pol = str(pol).replace(' ', '')
              pol = str(pol).replace('.', '')
              pol = str(pol).replace('-', '')
              pol_m = str(pol_m).replace(' ', '')
              pol_m = str(pol_m).replace('.', '')
              pol_m = str(pol_m).replace('-', '')
              print(pol,len(pol),pol_m,len(pol_m))
              for x, y in zip(pol, pol_m):
                  col +=1
                  if x.upper() == y.upper():
                      sim +=1
              if col == 0:
                  ver = 0
              else:
                  ver = round(sim/col*100,2)
              # sred_ver += ver
              # col_ver +=1


              pol = pol[::-1]
              pol_m = pol_m[::-1]
              for x, y in zip(pol, pol_m):
                  col_obr += 1
                  if x == y.upper():
                      sim_obr += 1
              if col == 0:
                  ver_obr = 0
              else:
                  ver_obr = round(sim_obr/col_obr*100,2)
              sred_ver += max(ver,ver_obr)
              col_ver +=1
              d[pole] = max(ver,ver_obr)

              # if pol == pol_m:
              #       d[pole] = 100.0
              # else:
              #       d[pole] = 0.0
            # print(d)
            data['static'].append(d)
            # data['static_obr'].append(d_obr)

            d = {}
            # d_obr={}

            continue
          continue
    to_csv(data['static'])
    # to_csv(data['static_obr'])
    print('Точность распознания: ', round(sred_ver/col_ver,2))
    # print('Точность распознания obr: ', )
dt = pd.read_csv('data_many18.csv')
print(dt)
df_manual = pd.read_csv('data_manual.csv')
print(df_manual)
dt=dt.fillna('FALSE')
df_manual=df_manual.fillna('FALSE')
static_manual(df_manual,dt)
