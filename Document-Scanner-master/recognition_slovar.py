import pprint
import easyocr
import json
import cv2
import csv
import time
from memory_profiler import profile
#запускается 1 раз для скачивания библиотек
# reader = easyocr.Reader(['ru'], gpu=False) #распознание из коробки
reader = easyocr.Reader(['ru'], recog_network='custom_example', gpu=False) #распознание с дообучением
#сохранение в csv
def to_csv(data):
  cols = ['ID','issued_by_whom','first_name','date_of_issue','unit_code','series_and_number','surname','patronymic','gender','date_of_birth','place_of_birth','accr_obl','accr_ocr']
  path = "data_auto_baza_8.csv"
  with open(path, 'a+', encoding='utf-8') as f:
    wr = csv.DictWriter(f, fieldnames = cols)
    if f.tell() == 0:
        wr.writeheader()
    wr.writerows(data)

#распознание текста
# @profile()
def recognition_slovar(jpg,oblasty, accr_obl):
    start_time_r = time.time() #засекаем время выполнеия функции
#__________________________________________________________________
    #задаем начальные значения
    data = {}
    data['pasport'] = []
    d = {}
    issued_by_whom = ''
    series_and_number = ''
    place_of_birth = ''
    ver = 0
    acc_ocr = 0
    col_ocr = 0
#________________________________________________________
    d['ID'] = (jpg.split('.')[0]).split('/')[-1] #записываем номер фотографии (берем имя файла

    for i,v in oblasty.items(): #цикл по всем найденым полям с их распределения по классам
        image = cv2.cvtColor(v, cv2.COLOR_BGR2RGB) #переводим области в серый цвет
        #Для каждого класса устанавливаем свои ограничения на распознания классов
        if 'date' in i or 'code' in i or 'series' in i:
            result = reader.readtext(image, allowlist='0123456789-. ')
            # print(result)
        elif 'surname' in i or 'name' in i or 'patronymic' in i:
            result = reader.readtext(image,
                                     allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-')
        elif 'gender' in i:
            result = reader.readtext(image, allowlist='.МУЖЕНмужен')
        else:
            result = reader.readtext(image,
                                     allowlist='АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ-"№ .1234567890')
        pole = ''
        # Сцепляем распознаные поля в одной области и подсчитыаем среднию увереность
        for k in range(len(result)):
            if result[k][2] * 100 >= 35:
                pole = pole + ' ' + str(result[k][1])
                acc_ocr += result[k][2] * 100
                col_ocr += 1
        #ели поле не пустое то записываем результат распознавания (json +csv)
        if pole:
            pole = pole.strip()#удаляем пробелы вконце и в неачале
            #сцепляем 
            if 'issued_by_whom' in i:
                issued_by_whom = issued_by_whom + pole + ' '
            if 'place_of_birth' in i:
                place_of_birth = place_of_birth + pole + ' '
            if 'series_and_number' in i:
                # print(pole)
                if len(pole) >= 10:
                    if ver < result[k][2]:
                        series_and_number = pole
#Убираем лишние знаки в распознание текста, если такие находятся и приводим к формату
            if 'issued_by_whom' in i or 'place_of_birth' in i or 'series_and_number' in i:
                pass
            elif 'date' in i:
                pole = pole.replace('.', '').replace(' ', '').replace('-', '')
                pole = pole[:2] + '.' + pole[2:4] + '.' + pole[4:]
                d[i.split('.', 1)[0]] = pole.upper().strip()
            elif 'cod' in i:
                pole = pole.replace(' . ', '').replace(' ', '').replace('-', '')
                pole = pole[:3] + '-' + pole[3:]
                d[i.split('.', 1)[0]] = pole.upper().strip()
                #заменяем пол
            elif 'gender' in i:
                if 'Е' in pole.upper() or 'Н' in pole.upper():
                    pole = 'ЖЕН.'
                elif 'У' in pole.upper() or 'М' in pole.upper():
                    pole = 'МУЖ.'
                d[i.split('.', 1)[0]] = pole.upper().strip()
            else:
                d[i.split('.', 1)[0]] = pole.replace('  ', ' ').upper().strip()
    #пост обработка текста, подводим под формат паспорта
    place_of_birth = place_of_birth.upper()
    issued_by_whom = issued_by_whom.upper()
    place_of_birth = place_of_birth.replace('ГОР ', 'ГОР. ').replace('Г ', 'Г. ').replace('ОБЛ ', 'ОБЛ. ').replace('ПОС ', 'ПОС. ').replace(' . ', '. ').replace(' .', '.').replace('  ', ' ').replace('..', '.')
    issued_by_whom = issued_by_whom.replace('ГОР ', 'ГОР. ').replace('Г ', 'Г. ').replace('ОБЛ ', 'ОБЛ. ').replace('ПОС ', 'ПОС. ').replace(' . ', '. ').replace(' .', '.').replace('  ', ' ').replace('..', '.')
    if series_and_number:
        series_and_number = series_and_number.replace(' ', '')
        if len(series_and_number) == 10:
            series_and_number = series_and_number[:2]+' ' + series_and_number[2:4] + ' ' + series_and_number[4:]
        else:
            series_and_number = 'поле распознано не полностью' + series_and_number
    else:
        series_and_number = 'поле не распознано'
# Создаем файлы json and csv
    d['issued_by_whom'] = issued_by_whom.strip()
    d['place_of_birth'] = place_of_birth.strip()
    d['series_and_number'] = series_and_number.strip()
    if col_ocr == 0:
        accr_ocr = 0
    else:
        accr_ocr = round(acc_ocr / col_ocr, 2)
    d['accr_ocr'] = accr_ocr
    d['accr_obl'] = accr_obl
    data['pasport'].append(d)
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))
    pprint.pprint(data['pasport'])
    to_csv(data['pasport'])#зписываем json в csv
    print("--- %s seconds_records ocr---" % (time.time() - start_time_r))
