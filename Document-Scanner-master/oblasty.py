import shutil
from recognition import recognition
from recognition_slovar import recognition_slovar
import cv2
import os


def rotate_image(mat, angle):
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """

    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    # rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

    return cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

def oblasty(txt,jpg):

    #для вывода областей
    if os.path.exists('oblosty'):
        shutil.rmtree('oblosty')
    os.mkdir('oblosty')
#
    oblasty={}
    f = open(txt, 'r')
    lines = f.readlines()
    koord = 0
    iss = 0
    plac = 0
    image = cv2.imread(jpg, cv2.IMREAD_GRAYSCALE)
    spiss = []
    acc_obl = 0
    col_obl = 0
    for line in lines[14:]:
        z = line.replace('   ', ' ')
        u = z.replace(':  ', ' ')
        y = u.replace('\t', ' ')
        t = y.replace(')\n', '')
        data = t.split(' ')
        # print(data)
        acc_obl += int(data[1][:-1])
        col_obl += 1
        cat = data[0].replace(':', '')
        y = int(data[5])
        x = int(data[3])
        h = int(data[9])
        w = int(data[7])
        spis = [cat, x, y, w, h]
        spiss.append(spis)
    # def custom_key(spiss):
    #     return spiss[2]
    spissok = sorted(spiss, reverse=True, key=lambda x: x[1])#spiss.sort(key=custom_key)
    # print(spiss)
    # print(spissok)
    for l in spissok:
        # print(l)
        cat = l[0]
        y = int(l[2])
        x = int(l[1])
        h = int(l[4])
        w = int(l[3])
        if ('signature' in cat) or ('photograph' in cat):
            pass
        else:
            if 'issued_by_whom' in cat:
                nam = 'oblosty/' + cat + '_' + str(iss) + '.jpg'
                ob = cat + '_' + str(iss)
                iss += 1
                yy = y - 5
                xx = x - 30
                if yy < 0:
                    yy = 0
                if xx < 0:
                    xx = 0
                cropped = image[yy:y + h + 5, xx:x + w + 30]
                # cv2.imwrite(nam, cropped)
                oblasty[ob] = cropped
            elif 'place_of_birth' in cat:
                nam = 'oblosty/' + cat + '_' + str(plac) + '.jpg'
                ob = cat + '_' + str(plac)
                plac += 1
                yy = y - 5
                xx = x - 30
                if yy < 0:
                    yy = 0
                if xx < 0:
                    xx = 0
                cropped = image[yy:y + h, xx:x + w + 30]
                # cv2.imwrite(nam, cropped)
                oblasty[ob] = cropped
            elif 'series' in cat:
                nam = 'oblosty/' + cat + '.jpg'
                ob = cat
                cropped = image[y - 10:y + h + 10, x - 3:x + w + 3]
                oblasty[ob] = rotate_image(cropped, 90)
            else:
                nam = 'oblosty/' + cat + '.jpg'
                ob = cat
                cropped = image[y:y + h, x:x + w]
                # cv2.imwrite(nam, cropped)
                oblasty[ob] = cropped

    accr_obl = round(acc_obl / col_obl, 2)
    # print('Точность определения областей: ', accr_obl)
    # recognition(jpg, accr_obl)
    recognition_slovar(jpg, oblasty, accr_obl)
