import cv2
import numpy as np
# import utlis

from yolo import yolo
#Программа по автоматичекому выравниванию паспорта, если есть фон, без фона работает не корректно
from memory_profiler import profile

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), dtype=np.int32)
    add = myPoints.sum(1)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] =myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]

    return myPointsNew


def biggestContour(contours):
    biggest = np.array([])
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 5000:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest = approx
                max_area = area
    return biggest,max_area

# @profile()
def auto_rotait(photo,out):
  ########################################################################

  heightImg = 640
  widthImg = 455
  ########################################################################

  ph = photo.split('/')[-1]
  pathImage = photo

  img = cv2.imread(pathImage)
  img = cv2.resize(img, (widthImg, heightImg)) # ИЗМЕНЕНИЕ РАЗМЕРА ИЗОБРАЖЕНИЯ

  imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # ПРЕОБРАЗОВАНИЕ ИЗОБРАЖЕНИЯ В ОТТЕНКИ СЕРОГО
  imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ДОБАВИТЬ РАЗМЫТИЕ ПО ГАУССУ
  imgThreshold = cv2.Canny(imgBlur,20,20)#thres[0],thres[1]) # ПРИМЕНИТЕ ХИТРОЕ РАЗМЫТИЕ
  kernel = np.ones((5, 5))
  imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # ПРИМЕНИТЕ РАСШИРЕНИЕ
  imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # НАНЕСИТЕ ЭРОЗИЮ

  ## ## НАЙТИ ВСЕ КОНТУРЫ
  contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # НАЙТИ ВСЕ КОНТУРЫ


  # # НАЙДИТЕ САМЫЙ БОЛЬШОЙ КОНТУР
  biggest, maxArea = biggestContour(contours) # НАЙДИТЕ САМЫЙ БОЛЬШОЙ КОНТУР
  if biggest.size != 0:
      biggest=reorder(biggest)
      pts1 = np.float32(biggest) # ПОДГОТОВЬТЕ ТОЧКИ ДЛЯ ДЕФОРМАЦИИ
      pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # ПОДГОТОВЬТЕ ТОЧКИ ДЛЯ ДЕФОРМАЦИИ
      matrix = cv2.getPerspectiveTransform(pts1, pts2)
      imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

  else:
    print('некоректная фотография, необходимо сфотографировать паспорт на однородном фоне')

  cv2.imwrite('oblosty/' + ph, imgWarpColored)
  # count += 1
  # print(pathImage)
  yolo(ph,out)
