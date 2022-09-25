from recognition_slovar_yolo_4 import recognition_slovar
import cv2
import time
import math


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
def zero( n ):
    return n * ( n > 0 )
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
        ob = ''
        #обрезаем области и сохраняем их в словарь, добавляем к областе пиксели для увеличения области распознавания
        if ('signature' in cat) or ('photograph' in cat):
            pass #поля подпись и фотографию не распознаем, поэтому с ними ничего не делаем
        else:
            if 'issued_by_whom' in cat:
                ob = cat + '_' + str(iss)
                iss += 1
            elif 'place_of_birth' in cat:
                ob = cat + '_' + str(plac)
                plac += 1
            elif 'series' not in cat:
                ob = cat
            if ob:
                oblasty[ob] = image[zero(y - math.ceil(h * 0.03)):y + math.ceil(h * 1.03), zero(x - math.ceil(w * 0.1)):x + math.ceil(w * 1.1)]
            if 'series' in cat:
                ob = cat
                cropped = image[zero(y - math.ceil(h*0.1)):y + math.ceil(h*1.1), zero(x - math.ceil(w*0.03)):x + math.ceil(w*1.03)]
                oblasty[ob] = rotate_image(cropped, 90)
#Передаем словарь с областями на распознание
    print("--- %s seconds oblasty---" % (time.time() - start_time_ob))
    recognition_slovar(put, oblasty)
