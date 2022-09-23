from recognition_slovar_yolo_4 import recognition_slovar
import cv2
import time
import numpy as np


def rotate_image(mat, angle):
    """
   Функция для поворота изображений (серийный номер)
    """

    height, width = mat.shape[:2] # форма изображения имеет 3 измерения
    image_center = (width/2, height/2) # getRotationMatrix2D нужны координаты в обратном порядке (ширина, высота) по сравнению с формой

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # вращение вычисляет cos и sin, принимая их абсолютные значения.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # найдите новые границы ширины и высоты
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    #вычтите старый центр изображения (возвращая изображение в исходное состояние) и добавьте новые координаты центра изображения.
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # поверните изображение с новыми границами и преобразованной матрицей поворота
    return cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

#вырезаем области после детекции YOLO4

def oblasty_yolo_4(put,image,box):

    start_time_ob = time.time()
    oblasty={}
    iss = 0
    plac = 0
#Сортируем список по у для того чтобы области шли по порядку сверху вниз
    spissok = sorted(box, reverse=False, key=lambda x: x[2])#spiss.sort(key=custom_key)
    for l in spissok:
        cat = l[0]
        y = int(l[2])
        x = int(l[1])
        h = int(l[4])
        w = int(l[3])
        #обрезаем области и сохраняем их в словарь, добавляем к областе пиксели для увеличения области распознавания
        if ('signature' in cat) or ('photograph' in cat):
            pass #поля подпись и фотографию не распознаем, поэтому с ними ничего не делаем
        else:
            if 'issued_by_whom' in cat:
                ob = cat + '_' + str(iss)
                iss += 1
                yy = y - 5
                xx = x - 30
                if yy < 0:
                    yy = 0
                if xx < 0:
                    xx = 0
                cropped = image[yy:y + h + 5, xx:x + w + 30]
                oblasty[ob] = cropped
            elif 'place_of_birth' in cat:
                ob = cat + '_' + str(plac)
                plac += 1
                yy = y - 5
                xx = x - 30
                if yy < 0:
                    yy = 0
                if xx < 0:
                    xx = 0
                cropped = image[yy:y + h, xx:x + w + 30]
                oblasty[ob] = cropped
            elif 'series' in cat:
                ob = cat
                cropped = image[y - 10:y + h + 10, x - 3:x + w + 3]
                oblasty[ob] = rotate_image(cropped, 90)
            else:
                ob = cat
                cropped = image[y:y + h, x:x + w]
                oblasty[ob] = cropped

#Передаем словарь с областями на распознание
    print("--- %s seconds oblasty---" % (time.time() - start_time_ob))
    recognition_slovar(put, oblasty)
