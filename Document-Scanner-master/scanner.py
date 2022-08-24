import numpy as np
import cv2
import os
from oblasty import oblasty

import tkinter.filedialog as fd
def fil():
    filetypes = (("Изображение", "*.jpg *.gif *.png"),
                 ("Любой", "*"))
    filename = fd.askopenfilename(title="Открыть файл", initialdir="/",
                                  filetypes=filetypes)
    if filename:
        return filename.split('/')[-1]

photo = fil()
# def normal_photo(imag_put):
imag_put = 'photo/' + photo
# txt = 'oblosty_txt/' + photo.split('.')[0] + '.txt'
# crop = 'oblosty'
DOCUMENT_HEIGHT_WIDTH_RATIO = np.sqrt(1.982464) # ISO paper size concept (A0, A1, A2, A3, ...)
#DOCUMENT_HEIGHT_WIDTH_RATIO = np.sqrt(1.982464) # паспорт
WIDTH = 700
HEIGHT = int(WIDTH * DOCUMENT_HEIGHT_WIDTH_RATIO)

# onMouse variables
drawing = False # true if mouse is pressed
closer_edge = None
EDGE_COLOR = (120, 120, 120)
CONTOUR_COLOR = (0, 255, 0)

def onMouse(event, x, y, flags, param):
    global imageCopy, approx, edges, pts_src, drawing, closer_edge

    if event == (cv2.EVENT_LBUTTONDOWN and cv2.EVENT_MOUSEMOVE):
        if drawing:
            imageCopy = img.copy()
            cv2.circle(imageCopy, (x, y), 10, EDGE_COLOR, -1)
            approx[closer_edge][0] = np.array((x, y))
            cv2.drawContours(imageCopy, [approx], -1, CONTOUR_COLOR, thickness=5) #Uncomment to draw lines conecting the edges
            cv2.drawContours(imageCopy, approx, -1, EDGE_COLOR, thickness=10) #Uncomment to draw points on edges

    elif event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        distance_from_edges = []
        for coordinates in edges:
            distance_from_edges.append(np.linalg.norm(np.array((x, y)) - coordinates))
        closer_edge = np.argmin(distance_from_edges)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        #Update edges and pts_src
        edges[closer_edge] = np.array((x, y))
        # top left corner will have the smallest sum,
        # bottom right corner will have the largest sum
        # top-right will have smallest difference
        # botton left will have largest difference
        addition = np.sum(edges, axis=1)
        pts_src[0] = edges[np.argmin(addition)]
        pts_src[2] = edges[np.argmax(addition)]
        diff = np.diff(edges, axis=1)
        pts_src[1] = edges[np.argmin(diff)]
        pts_src[3] = edges[np.argmax(diff)]


#pictures = os.listdir('pictures/1_search duplicates_2')
#pictures.sort()
#for picture in pictures

img = cv2.imread(imag_put)
#img = cv2.imread('pictures/myImage3.jpg')
#img = cv2.imread('pictures/scanned-form.jpg')
#img = cv2.imread('pictures/81.jpg')
imageCopy = img.copy()
# Converting to grayscale
imageGray = cv2.cvtColor(imageCopy, cv2.COLOR_BGR2GRAY)
imageGray = cv2.GaussianBlur(imageGray, (5, 5), 0)
imageGray = cv2.bilateralFilter(imageGray, 8, 15, 15)


# Edge detection Выделение границ
edged = cv2.Canny(imageGray, 50, 100)
kernel = np.ones((5, 5))
edged = cv2.dilate(edged, kernel, iterations=2)  # APPLY DILATION Расширение
edged = cv2.erode(edged, kernel, iterations=1)  # APPLY EROSION Эрозия

# cv2.namedWindow('edge',cv2.WINDOW_NORMAL)
# cv2.imshow("edge", edged)

# Finding all contours in the image
contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#Sorting contours from largest to smallest area
#biggest, maxArea = utlis.biggestContour(contours) # Поиск наибольших контуров
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]
#print(contours)
# loop over our contours
for contour in contours:
    # approximating the contour
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.05 * perimeter, True)
    # if the approximated contour has four points, then
    # we can assume that we have found our document.
    #print(type(approx))

    if len(approx) != 4:
        approx = np.array([[[  25,   25]], [[  25, 750]], [[500, 750]], [[500,   25]]])
    print(type(approx))
    print(approx)
    #print(approx.shape)
    if len(approx) == 4:

        cv2.drawContours(imageCopy, [approx], -1, CONTOUR_COLOR, thickness=5) #Uncomment to draw lines conecting the edges
        cv2.drawContours(imageCopy, approx, -1, EDGE_COLOR, thickness=10) #Uncomment to draw points on edges
        # print(approx)
        edges = approx.reshape(4, 2)
        # print(edges)
        break
    else:
        raise Exception('No 4-point contour was found in the picture.')

# list to hold ROI coordinates
pts_src = np.zeros((4, 2), dtype=float)

# top left corner will have the smallest sum,
# bottom right corner will have the largest sum
# top-right will have smallest difference
# botton left will have largest difference
addition = np.sum(edges, axis=1)
pts_src[0] = edges[np.argmin(addition)]
pts_src[2] = edges[np.argmax(addition)]
diff = np.diff(edges, axis=1)
pts_src[1] = edges[np.argmin(diff)]
pts_src[3] = edges[np.argmax(diff)]

# Checks which of the sides is bigger to identify possible rotation of document
# Document on the vertical axis # Проверка необходимо ли вращать документ
if np.linalg.norm(pts_src[0] - pts_src[1]) < np.linalg.norm(pts_src[0] - pts_src[3]):
    pts_dst = np.array([[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]], dtype=float)
else: # Document on the horizontal axis
    pts_dst = np.array([[0, HEIGHT], [0, 0], [WIDTH, 0], [WIDTH, HEIGHT]], dtype=float)

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.setMouseCallback('image', onMouse, img)

while cv2.getWindowProperty('image', 0) >= 0: # Stop if user closes the window with mouse
    cv2.imshow('image', imageCopy)
    cv2.putText(imageCopy, 'Press q to extract or drag the circles to correct.',
              (10,10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1)
    k = cv2.waitKey(1) & 0xFF
    if k == 27: # ESC key
        ## Необходимо добавить модуль по разметки фотографии YOLO 4


        #Вызов функции обрезания вырезания областей фотографии
        oblasty('oblosty_txt/' + photo.split('.')[0] + '.txt', 'photo/' + photo)
        cv2.destroyWindow('extraction')
        # cv2.destroyWindow('image')
        cv2.waitKey(0)
    elif k == ord('q'):

        # Calculate Homography
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Warp source image to destination based on homography
        img_out = cv2.warpPerspective(img, h, (WIDTH, HEIGHT))

        cv2.namedWindow('extraction')
        cv2.imshow('extraction', img_out)

