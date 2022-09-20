import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('oblosty/series_and_number_1.jpg',0)
#cropped
cropped = cv2.threshold(img,abs(np.mean(img)-15),255,cv2.THRESH_BINARY)[1]#переводим в бинарное изображение с порогом 150 для лучшего распознаания
cv2.imwrite('oblosty/' + '78' + '.jpg', cropped)
