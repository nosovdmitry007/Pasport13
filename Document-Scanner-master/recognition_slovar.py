import pprint
import easyocr
import json
import os
import cv2
import csv
#запускается 1 раз для скачивания библиотек
# reader = easyocr.Reader(['ru'], gpu=False)


reader = easyocr.Reader(['ru'], recog_network='custom_example', gpu=False)

def to_csv(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "data_many17.csv"
  with open(path, 'a+', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols)
    if f.tell() == 0:
        wr.writeheader()
    wr.writerows(data)

def recognition_slovar(jpg,oblasty, accr_obl):
    data = {}
    data['pasport'] = []
    d = {}
    obl = dict(sorted(oblasty.items()))
    # print(oblasty.items())
    # pug = os.listdir('oblosty')
    # path = sorted(pug)
    issued_by_whom = ''
    series_and_number = ''
    place_of_birth = ''
    ver = 0
    acc_ocr = 0
    col_ocr = 0
    d['ID'] = (jpg.split('.')[0]).split('/')[-1]
    for i,v in obl.items():
        # print(i)
        # put = 'oblosty/' + i
        # image = cv2.imread(v)
        image = cv2.cvtColor(v, cv2.COLOR_BGR2RGB)
        if 'date' in i or 'code' in i or 'series' in i:
            result = reader.readtext(image, allowlist='0123456789-. ')
        elif 'surname' in i or 'name' in i or 'patronymic' in i:
            result = reader.readtext(image,
                                     allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя-')
        elif 'gender' in i:
            result = reader.readtext(image, allowlist='.МУЖЕНмужен')
        else:
            result = reader.readtext(image,
                                     allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя-"№ .')
        pole = ''
        for k in range(len(result)):
            if result[k][2] * 100 >= 32:
                pole = pole + ' ' + str(result[k][1])
                acc_ocr += result[k][2] * 100
                # print(str(result[k][1]), ': ',result[k][2] * 100)
                col_ocr += 1
        if pole:
            pole = pole.strip()
            if 'issued_by_whom' in i:
                issued_by_whom = issued_by_whom + pole + ' '
            if 'place_of_birth' in i:
                place_of_birth = place_of_birth + pole + ' '
            if 'series_and_number' in i:
                if ver < result[k][2]:
                    series_and_number = pole

            if 'issued_by_whom' in i or 'place_of_birth' in i or 'series_and_number' in i:
                pass
            elif 'date' in i:
                pole = pole.replace(' . ', '.')
                pole = pole.replace('  ', ' ')
                pole = pole.replace(' ', '.')
                pole = pole.replace('..', '.')
                d[i.split('.', 1)[0]] = pole.upper().strip()
            else:
                d[i.split('.', 1)[0]] = pole.replace('  ', ' ').upper().strip()

    place_of_birth = place_of_birth.replace(' . ', '.')
    place_of_birth = place_of_birth.replace('  ', ' ')
    place_of_birth = place_of_birth.replace('..', '.')
    issued_by_whom = issued_by_whom.replace(' . ', '.')
    issued_by_whom = issued_by_whom.replace('..', '.')
    issued_by_whom = issued_by_whom.replace('  ', ' ')
    series_and_number = series_and_number.replace('  ', ' ')

    d['issued_by_whom'] = issued_by_whom.upper().strip()

    d['place_of_birth'] = place_of_birth.upper().strip()

    d['series_and_number'] = series_and_number.strip()

    accr_ocr = round(acc_ocr / col_ocr, 2)
    d['accr_ocr'] = accr_ocr
    d['accr_obl'] = accr_obl
    data['pasport'].append(d)
    # d['accr_ocr'] = accr_ocr
    # d['accr_obl'] = accr_obl
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
    print('Точность определения областей: ', accr_obl)
    print('Точность распознания текстов: ', accr_ocr)
    pprint.pprint(data['pasport'])
    to_csv(data['pasport'])
