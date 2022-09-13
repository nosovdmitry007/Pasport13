import cv2
import numpy as np
import utlis

from yolo import yolo
#Программа по автоматичекому выравниванию паспорта, если есть фон, без фона работает не корректно
def auto_rotait(photo,out):
  ########################################################################
  webCamFeed = False

  cap = cv2.VideoCapture(1)
  cap.set(10,160)
  heightImg = 985
  widthImg = 700
  ########################################################################

  ph = photo.split('/')[-1]
  pathImage = photo
  if webCamFeed:success, img = cap.read()
  else:img = cv2.imread(pathImage)
      # print(pathImage)
  img = cv2.resize(img, (widthImg, heightImg)) # ИЗМЕНЕНИЕ РАЗМЕРА ИЗОБРАЖЕНИЯ

  imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # ПРЕОБРАЗОВАНИЕ ИЗОБРАЖЕНИЯ В ОТТЕНКИ СЕРОГО
  imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ДОБАВИТЬ РАЗМЫТИЕ ПО ГАУССУ
  imgThreshold = cv2.Canny(imgBlur,20,20)#thres[0],thres[1]) # ПРИМЕНИТЕ ХИТРОЕ РАЗМЫТИЕ
  kernel = np.ones((5, 5))
  imgDial = cv2.dilate(imgThreshold, kernel, iterations=2) # ПРИМЕНИТЕ РАСШИРЕНИЕ
  imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # НАНЕСИТЕ ЭРОЗИЮ

  ## ## НАЙТИ ВСЕ КОНТУРЫ
  imgContours = img.copy() # КОПИРОВАНИЕ ИЗОБРАЖЕНИЯ ДЛЯ ОТОБРАЖЕНИЯ
  imgBigContour = img.copy() # КОПИРОВАНИЕ ИЗОБРАЖЕНИЯ ДЛЯ ОТОБРАЖЕНИЯ
  contours, hierarchy = cv2.findContours(imgThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # НАЙТИ ВСЕ КОНТУРЫ
  cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # НАРИСУЙТЕ ВСЕ ОБНАРУЖЕННЫЕ КОНТУРЫ


  # # НАЙДИТЕ САМЫЙ БОЛЬШОЙ КОНТУР
  biggest, maxArea = utlis.biggestContour(contours) # НАЙДИТЕ САМЫЙ БОЛЬШОЙ КОНТУР
  if biggest.size != 0:
      biggest=utlis.reorder(biggest)
      cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # НАРИСУЙТЕ САМЫЙ БОЛЬШОЙ КОНТУР
      pts1 = np.float32(biggest) # ПОДГОТОВЬТЕ ТОЧКИ ДЛЯ ДЕФОРМАЦИИ
      pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # ПОДГОТОВЬТЕ ТОЧКИ ДЛЯ ДЕФОРМАЦИИ
      matrix = cv2.getPerspectiveTransform(pts1, pts2)
      imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg))

      #УДАЛИТЕ ПО 20 ПИКСЕЛЕЙ С КАЖДОЙ СТОРОНЫ
      imgWarpColored = cv2.resize(imgWarpColored,(widthImg,heightImg))

      # ПРИМЕНИТЬ АДАПТИВНЫЙ ПОРОГ
      imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)
      imgAdaptiveThre= cv2.adaptiveThreshold(imgWarpGray, 255, 1, 1, 7, 2)
      imgAdaptiveThre = cv2.bitwise_not(imgAdaptiveThre)

  else:
    print('некоректная фотография, необходимо сфотографировать паспорт на однородгом фоне')

  cv2.imwrite(ph, imgWarpColored)
  # count += 1
  print(pathImage)
  yolo(ph,out)
