import pprint

import easyocr
import json
import os
import cv2
reader = easyocr.Reader(['ru', 'en'], gpu=False)

data = {}
data['pasport'] = []

path = os.listdir('oblosty')
issued_by_whom = ''
series_and_number = ''
place_of_birth = ''
ver=0
for i in path:
    put = 'oblosty/' + i
    image = cv2.imread(put)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    if 'date' in i or 'code' in i or 'series' in i:
        result = reader.readtext(image, allowlist='0123456789')
    result = reader.readtext(image)
    pole = ''
    # print(k.split('_', 3)[0])
    for k in range(len(result)):
        pole = pole + ' ' + str(result[k][1])
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
        # print(i.split('.', 1)[0], pole, str(result[k][2]))
        pole = pole.replace(' . ', '.')
        pole = pole.replace('  ', ' ')
        pole = pole.replace(' ', '.')

        data['pasport'].append({
            i.split('.', 1)[0]: pole
        })

    else:
        # print(i.split('.', 1)[0], pole, str(result[k][2]))
        data['pasport'].append({
            i.split('.', 1)[0]: pole.replace('  ', ' ')
        })

# print('issued_by_whom', issued_by_whom)
# print('place_of_birth', place_of_birth)
# print('series_and_number', series_and_number)
place_of_birth = place_of_birth.replace(' . ', '.')
place_of_birth = place_of_birth.replace('  ', ' ')
issued_by_whom = issued_by_whom.replace(' . ', '.')
issued_by_whom = issued_by_whom.replace('  ', ' ')
series_and_number = series_and_number.replace('  ', ' ')
data['pasport'].append({
    'issued_by_whom': issued_by_whom
    })
data['pasport'].append({
       'place_of_birth': place_of_birth
})
data['pasport'].append({
     'series_and_number': series_and_number
})

with open('data.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(data, ensure_ascii=False))
pprint.pprint(data)