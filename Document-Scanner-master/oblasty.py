import shutil
from recognition import recognition
import cv2
import os


def rotate_image(mat, angle, nam):
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
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

    cv2.imwrite(nam, rotated_mat)



def oblasty(txt,jpg):
    if os.path.exists('oblosty'):
        shutil.rmtree('oblosty')
    os.mkdir('oblosty')

    f = open(txt, 'r')
    lines = f.readlines()
    koord = 0
    iss = 1
    plac = 1
    image = cv2.imread(jpg)
    spiss=[]
    for line in lines:

        if '/' in line:
            print(line)
            koord = 1
            continue

        if koord == 1:
            z = line.replace('   ', ' ')
            u = z.replace(':  ', ' ')
            y = u.replace('\t', ' ')
            t = y.replace(')\n', '')
            data = t.split(' ')
            print(data)

            cat = data[0].replace(':', '')
            y = int(data[5])
            x = int(data[3])
            h = int(data[9])
            w = int(data[7])
            spis = [cat, x, y, w, h]
            spiss.append(spis)

    def custom_key(spiss):
        return spiss[2]
    spissok = spiss.sort(key=custom_key)
    print(spiss)
    # print(spissok)
    for l in spiss:
        print(l)
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
                iss += 1
                cropped = image[y-5:y + h+5, x-20:x + w+20]
                cv2.imwrite(nam, cropped)
            elif 'place_of_birth' in cat:
                nam = 'oblosty/' + cat + '_' + str(plac) + '.jpg'
                plac += 1
                cropped = image[y-5:y + h+5, x-20:x + w+20]
                cv2.imwrite(nam, cropped)
            elif 'series' in cat:
                nam = 'oblosty/' + cat + '.jpg'
                cropped = image[y:y + h, x:x + w]
                rotate_image(cropped, 90, nam)
            elif 'issued_by_whom' in cat or 'place_of_birth' in cat:
                nam = 'oblosty/' + cat + '.jpg'
                yy = y-5
                xx = x -20
                if yy<0:
                    yy=0
                if xx<0:
                    xx=0
                cropped = image[yy:y + h+5, xx:x + w+20]
                cv2.imwrite(nam, cropped)
            else:
                nam = 'oblosty/' + cat + '.jpg'
                cropped = image[y:y + h, x:x + w]
                cv2.imwrite(nam, cropped)

    recognition()
