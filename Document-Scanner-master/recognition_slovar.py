import pprint
import easyocr
import json
import os
import cv2
import csv
import time
#запускается 1 раз для скачивания библиотек
# reader = easyocr.Reader(['ru'], gpu=False)


reader = easyocr.Reader(['ru'], recog_network='custom_example', gpu=False)

#сохранение в csv
def to_csv(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "data_many18.csv"
  with open(path, 'a+', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols)
    if f.tell() == 0:
        wr.writeheader()
    wr.writerows(data)

#распознание текста
def recognition_slovar(jpg,oblasty, accr_obl):
    start_time_r = time.time()
    data = {}
    data['pasport'] = []
    d = {}
    obl = dict(sorted(oblasty.items()))
    issued_by_whom = ''
    series_and_number = ''
    place_of_birth = ''
    ver = 0
    acc_ocr = 0
    col_ocr = 0
    d['ID'] = (jpg.split('.')[0]).split('/')[-1] #записываем номер фотографии
    for i,v in obl.items(): #цикл по всем найденым полям с их распределения по классам
        image = cv2.cvtColor(v, cv2.COLOR_BGR2RGB) #переводим области в серый цвет
        #Для каждого класса устанавливаем свои ограничения на распознания классов
        if 'date' in i or 'code' in i or 'series' in i:
            result = reader.readtext(image, allowlist='0123456789-. ')
        elif 'surname' in i or 'name' in i or 'patronymic' in i:
            result = reader.readtext(image,
                                     allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-')
        elif 'gender' in i:
            result = reader.readtext(image, allowlist='.МУЖЕНмужен')
        else:
            result = reader.readtext(image,
                                     allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-"№ .1234567890')
        pole = ''
        # Сцепляем распознаные поля в одной области и подсчитыаем среднию вероятность
        for k in range(len(result)):
            print(str(result[k][1]), result[k][2] * 100)
            if result[k][2] * 100 >= 35:
                pole = pole + ' ' + str(result[k][1])
                acc_ocr += result[k][2] * 100
                col_ocr += 1
        if pole:
            pole = pole.strip()
            if 'issued_by_whom' in i:
                issued_by_whom = issued_by_whom + pole + ' '
            if 'place_of_birth' in i:
                place_of_birth = place_of_birth + pole + ' '
            if 'series_and_number' in i:
                if len(pole) >= 10:
                    if ver < result[k][2]:
                        series_and_number = pole
#Убираем лишние знаки в распознание текста, если такие находятся и приводим к формату
            if 'issued_by_whom' in i or 'place_of_birth' in i or 'series_and_number' in i:
                pass
            elif 'date' in i:
                pole = pole.replace(' . ', '. ')
                pole = pole.replace('  ', ' ')
                pole = pole.replace(' ', '.')
                pole = pole.replace('..', '.')
                d[i.split('.', 1)[0]] = pole.upper().strip()
            else:
                d[i.split('.', 1)[0]] = pole.replace('  ', ' ').upper().strip()

    place_of_birth = place_of_birth.replace(' . ', '. ')
    place_of_birth = place_of_birth.replace(' .', '.')
    place_of_birth = place_of_birth.replace('  ', ' ')
    place_of_birth = place_of_birth.replace('..', '.')
    place_of_birth = place_of_birth.upper().replace('ГОР ', 'ГОР. ')
    place_of_birth = place_of_birth.upper().replace('Г ', 'Г. ')
    place_of_birth = place_of_birth.upper().replace('ОБЛ ', 'ОБЛ. ')
    issued_by_whom = issued_by_whom.replace(' . ', '. ')
    issued_by_whom = issued_by_whom.replace('..', '.')
    issued_by_whom = issued_by_whom.replace('  ', ' ')
    issued_by_whom = issued_by_whom.upper().replace('ГОР ', 'ГОР. ')
    issued_by_whom = issued_by_whom.upper().replace('Г ', 'Г. ')
    issued_by_whom = issued_by_whom.upper().replace('ОБЛ ', 'ОБЛ. ')
    series_and_number = series_and_number.replace('  ', ' ')

# Создаем файлы json and csv
    d['issued_by_whom'] = issued_by_whom.upper().strip()

    d['place_of_birth'] = place_of_birth.upper().strip()

    d['series_and_number'] = series_and_number.strip()

    accr_ocr = round(acc_ocr / col_ocr, 2)
    d['accr_ocr'] = accr_ocr
    d['accr_obl'] = accr_obl
    data['pasport'].append(d)
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
    print('Точность определения областей: ', accr_obl)
    print('Точность распознания текстов: ', accr_ocr)
    pprint.pprint(data['pasport'])
    to_csv(data['pasport'])
    print("--- %s seconds_records ocr---" % (time.time() - start_time_r))
