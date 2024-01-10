import utils

curves = []
averageVal = 10

def getLaneCurve(image, display = 2):
    # display option:
    # 0 - display nothing
    # 1 - display result
    # 2 - display whole pipeline

    tempImg = image.copy()
    resImg = image.copy()
    # apply thresholding to image
    imageThres = utils.thresholding(image)
    
    # warp the input image
    height, width, channel = image.shape
    points = utils.getTrackbarsVals()
    imageWarped = utils.imageWarping(imageThres, points, width, height)
    imageWarpedPoint = utils.drawingPoints(tempImg, points)

    # finding curve using histogram for pixel summation
    middlePoint, imageHistogram = utils.getInputHistogram(imageWarped, display=True, region=4)
    curveAveragePoint, imageHistogram = utils.getInputHistogram(imageWarped, display=True, minPercentage=0.9)
    curveRaw = curveAveragePoint - middlePoint

    # averaging curve value
    curves.append(curveRaw)
    if len(curves) > averageVal:
        curves.pop(0)
    curve = int(sum(curves)/len(curves))

    # display
    if display != 0:
       imgInvWarp = utils.imageWarping(imageWarped, points, width, height, inverse=True)
       imgInvWarp = utils.cv2.cvtColor(imgInvWarp,utils.cv2.COLOR_GRAY2BGR)
       imgInvWarp[0:height//3,0:width] = 0,0,0
       imgLaneColor = utils.np.zeros_like(image)
       imgLaneColor[:] = 0, 255, 0
       imgLaneColor = utils.cv2.bitwise_and(imgInvWarp, imgLaneColor)
       imgResult = utils.cv2.addWeighted(resImg,1,imgLaneColor,1,0)
       midY = 450
       utils.cv2.putText(imgResult,str(curve),(width//2-80,85),utils.cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
       utils.cv2.line(imgResult,(width//2,midY),(width//2+(curve*3),midY),(255,0,255),5)
       utils.cv2.line(imgResult, ((width // 2 + (curve * 3)), midY-25), (width // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
       for x in range(-30, 30):
           w = width // 20
           utils.cv2.line(imgResult, (w * x + int(curve//50 ), midY-10),
                    (w * x + int(curve//50 ), midY+10), (0, 0, 255), 2)
    #    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    #    cv2.putText(imgResult, 'FPS '+str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230,50,50), 3);
    if display == 2:
       imgStacked = utils.stackImages(0.7,([image,imageWarpedPoint,imageWarped],
                                         [imageHistogram,imgLaneColor,imgResult]))
       utils.cv2.imshow('ImageStack',imgStacked)
    elif display == 1:
       utils.cv2.imshow('Resutlt',imgResult)

    # normalization
    curve = curve/100
    if curve > 1: curve == 1
    if curve < -1: curve == -1

    return curve

if __name__ == '__main__':
    cam = utils.cv2.VideoCapture('testtrack.mp4')

    utils.initializeTrackbars([28, 303, 0, 480])

    frameCounter = 0
    while True:

        # video loop
        frameCounter += 1
        if cam.get(utils.cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cam.set(utils.cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0

        _, image = cam.read()
        image = utils.cv2.resize(image, (640, 480))
        curve = getLaneCurve(image, display=2)
        print(curve)
        # utils.cv2.imshow('Source', image)
        utils.cv2.waitKey(1)


