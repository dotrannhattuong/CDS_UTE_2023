import cv2 
import numpy as np
#read image (BGR)
image_bgr = cv2.imread('D:\Desktop\Visual Code Studio\Python\car_yellow_173.0.jpg')
#image_bgr = cv2.resize(image_bgr, (image_bgr.shape[1]//2, image_bgr.shape[0]//2))

#Convert to HSV
image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

#Convert to GRAY 
image_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

#Convert to BIN
ret, image_bin = cv2.threshold(image_gray, 127, 255, cv2.THRESH_BINARY)

#erosion & dilation
kernel =np.ones((5,5), np.uint8)
image_erosion = cv2.erode(image_gray, kernel, iterations=1)
image_dilation = cv2.dilate(image_gray, kernel, iterations=1)

#Gray -> Blur -> canny 
image_blur = cv2.blur(image_gray, (3,3))
sobel_x = cv2.Sobel(image_blur, cv2.CV_64F, 0, 1, ksize=5)
sobey_y = cv2.Sobel(image_blur, cv2.CV_64F, 1, 0, ksize=5)
canny = cv2.Canny(image_blur, 50, 100)

#houghline
img_houghline = cv2.imread('D:\Desktop\Visual Code Studio\Python\car_yellow_173.0.jpg')
img_houghline = cv2.resize(img_houghline, (img_houghline.shape[1]//2, img_houghline.shape[0]//2))
img_houghline_gray = cv2.cvtColor(img_houghline, cv2.COLOR_BGR2GRAY)
img_houghline_blur = cv2.blur(img_houghline_gray, (3,3))
img_houghline_canny = cv2.Canny(img_houghline_blur, 50, 100)
lines = cv2.HoughLines(img_houghline_canny, 1, np.pi/180, 150, None, 0 ,0)
if lines is not None:
    for i in range(0, len(lines)):
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0= b*rho
        pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
        pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
        cv2.line(img_houghline, pt1, pt2, (0,0,255), 1, cv2.LINE_AA)
#houghlineP
img_houghline_P = np.copy(img_houghline)
linesP = cv2.HoughLinesP(img_houghline_canny, 1, np.pi/180, 50, None, 50, 10)
if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv2.line(img_houghline_P, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv2.LINE_AA)

#contour
img_contours = cv2.imread('D:\Desktop\Visual Code Studio\Python\pngtree-round-bubble-decoration-illustration-png-image_4535061.jpg')
img_contours_gray = cv2.cvtColor(img_contours, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(img_contours_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img_contours, contours, -1, (0, 255, 0), 2)

#lane detection with hough transform
img_hough = cv2.imread('D:\Desktop\Visual Code Studio\Python\car_yellow_173.0.jpg')
img_hough = img_hough[130:,:]
gray_img_hough = cv2.cvtColor(img_hough, cv2.COLOR_BGR2GRAY)
blur_img_hough = cv2.GaussianBlur(gray_img_hough, (3,3), 0)
canny = cv2.Canny(blur_img_hough, 150, 255)

_img_bgr = np.copy(img_hough)
linesP = cv2.HoughLinesP(canny, 1, np.pi/180, 50, None, 50, 10)
if linesP is not None:
    for i in range(0, len(linesP)):
        l = linesP[i][0]
        cv2.line(_img_bgr, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv2.LINE_AA)

#lane detection with contour
img_contour = cv2.imread('D:\Desktop\Visual Code Studio\Python\car_yellow_173.0.jpg')
img_contour = img_contour[130:,:]
lower_green = np.array([95, 0, 0], dtype="uint8")
upper_green = np.array([255, 255, 255], dtype="uint8")
mask = cv2.inRange(img_contour, lower_green, upper_green)
lane = cv2.bitwise_and(img_contour, img_contour, mask= mask)
lane_gray = cv2.cvtColor(lane, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(lane_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
area = []
for i, contour in enumerate(contours):
    area.append(cv2.contourArea(contour))
max_area = np.max(area)
idx = area.index(max_area)
cnt = contours[idx]
cv2.drawContours(lane, [cnt], 0, [255,0,255],1)

#Display image
#cv2.imshow("image", image_bgr)
#cv2.imshow("image_hsv", image_hsv)
#cv2.imshow("image_gray", image_gray)
#cv2.imshow("image_bin", image_bin)
#cv2.imshow("image_erosion", image_erosion)
#cv2.imshow("image_dilation", image_dilation)
#cv2.imshow("image_blur", image_blur)
#cv2.imshow("sobel_x", sobel_x)
#cv2.imshow("sobey_y", sobey_y)
#cv2.imshow("canny", canny)
#cv2.imshow("img_houghline", img_houghline)
#cv2.imshow("img_houghline_P", img_houghline_P)
#cv2.imshow("img_contours", img_contours)
#cv2.imshow("lane detection with hough transform", _img_bgr)
#cv2.imshow("lane detection with contour gray", lane_gray)
#cv2.imshow("lane detection with contour binary", thresh)
#cv2.imshow("lane detection with contour", lane)
cv2.waitKey()