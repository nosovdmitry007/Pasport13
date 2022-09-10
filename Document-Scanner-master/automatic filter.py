import cv2
import numpy as np
import utlis
import os
from yolo import yolo
def auto_rotait(photo,out):
  ########################################################################
  webCamFeed = False
  # pathImage = "55.jpg"
  cap = cv2.VideoCapture(1)
  cap.set(10,160)
  heightImg = 985
  widthImg = 700
  ########################################################################

  count=0

  # file = os.listdir('pasport_photo')
  # # while True:
  # print(file)
  # for pathImage1 in file:
  ph = photo.split('/')[-1]
  pathImage =  photo
  if webCamFeed:success, img = cap.read()
  else:img = cv2.imread(pathImage)
      # print(pathImage)
  img = cv2.resize(img, (widthImg, heightImg)) # ИЗМЕНЕНИЕ РАЗМЕРА ИЗОБРАЖЕНИЯ

  imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # ПРИ НЕОБХОДИМОСТИ СОЗДАЙТЕ ПУСТОЕ ИЗОБРАЖЕНИЕ ДЛЯ ТЕСТИРОВАНИЯ ОТЛАДКИ
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
  biggest, maxArea = biggestContour(contours) # НАЙДИТЕ САМЫЙ БОЛЬШОЙ КОНТУР
  if biggest.size != 0:
      biggest=reorder(biggest)
      cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20) # НАРИСУЙТЕ САМЫЙ БОЛЬШОЙ КОНТУР
      imgBigContour = drawRectangle(imgBigContour,biggest,2)
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
      imgAdaptiveThre=cv2.medianBlur(imgAdaptiveThre,3)

      # Массив изображений для отображения
      # imageArray = ([img,imgGray,imgThreshold,imgContours],
      #               [imgBigContour,imgWarpColored, imgWarpGray,imgAdaptiveThre])

  else:
    print('некоректная фотография, необходимо сфотографировать паспорт на однородгом фоне')
      # imageArray = ([img,imgGray,imnk, imgBlank, imggThreshold,imgContours],
      #               [imgBlaBlank, imgBlank])

  # ЭТИКЕТКИ ДЛЯ ОТОБРАЖЕНИЯ
  # lables = [["Оригинал", "Серый", "Порог", "Контуры"],
  #           ["Самый большой контур", "Искаженная перспектива", "Искаженный серый", "Адаптивный порог"]]

  # stackedImage = stackImages(imageArray,0.75,lables)

  cv2.imwrite("/content/oblosty/"+str(ph), imgWarpColored)
  # count += 1
  print(pathImage)
  yolo("/content/oblosty/"+str(ph),out)
