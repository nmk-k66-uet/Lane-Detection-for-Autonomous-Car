import cv2
import numpy as np

# Using color detection to find the path
def thresholding(image):
    
    # converting image to HSV color space
    imageHSV = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # How to find value of minWhite and maxWhite? => Color Picker
    minWhite = np.array([48, 0, 90])
    maxWhite = np.array([179, 218, 255])
    
    # create mask layer
    maskedWhite= cv2.inRange(imageHSV, minWhite,maxWhite)

    return maskedWhite

# warp the input image to get a bird-eyes view of the track
def imageWarping(image, points, width, height, inverse = False):
    
    # point1 & point2 are input from user
    point1 = np.float32(points)
    point2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])

    # Transformation matrix
    if inverse:
        matrix = cv2.getPerspectiveTransform(point2, point1)
    else:    
        matrix = cv2.getPerspectiveTransform(point1, point2)
    imageWarped = cv2.warpPerspective(image, matrix, (width, height))

    return imageWarped

# placeholder function to be called when there is a change in Warping Trackbars
def placeholder(a):
    pass

# initialize Warping Trackbars
def initializeTrackbars(initialTracbarVals, widthTarget = 640, heightTarget = 480):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", initialTracbarVals[0], widthTarget//2, placeholder)
    cv2.createTrackbar("Height Top", "Trackbars", initialTracbarVals[1], heightTarget, placeholder)
    cv2.createTrackbar("Width Bottom", "Trackbars", initialTracbarVals[2], widthTarget//2, placeholder)
    cv2.createTrackbar("Height Bottom", "Trackbars", initialTracbarVals[3], heightTarget, placeholder)

# convert Warping Trackbars values into reference point for imageWarping function
def getTrackbarsVals(widthTarget = 640, heightTarget = 480):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(widthTop, heightTop), (widthTarget - widthTop, heightTop),
                      (widthBottom , heightBottom ), (widthTarget - widthBottom, heightBottom)])
    return points

# draw reference points into warped image
def drawingPoints(image, points):
    for point in points:
        cv2.circle(image, (int(point[0]), int(point[1])), 15, (0, 0, 255), cv2.FILLED)
    return image

# get input image histogram for finding curve using pixel summation
def getInputHistogram(image, minPercentage = 0.75, display = False, region = 1):
    
    if region == 1:
        histogramVal = np.sum(image, axis = 0)
    else:
        histogramVal = np.sum(image[image.shape[0]//region:,:], axis=0)
    # print(histogramVal)
    maxVal = np.max(histogramVal)
    # print(max)
    # minimum threshold to filter out noises in input image
    minVal = minPercentage * maxVal 
    
    indexArray = np.where(histogramVal >= minVal)
    basePoint = int(np.average(indexArray))
    # print(basePoint)

    # plot histogram and pixel summation
    if display:
        imageHistogram = np.zeros((image.shape[0], image.shape[1], 3), np.uint8)
        for x,intensity in enumerate(histogramVal):
            cv2.line(imageHistogram, (x, image.shape[0]), (x, int(image.shape[0] - (intensity//255//region))), (255, 0, 255), 1)
            cv2.circle(imageHistogram, (basePoint, image.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return basePoint, imageHistogram
    
    return basePoint

# stacking multiple output into 1 single frame
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver