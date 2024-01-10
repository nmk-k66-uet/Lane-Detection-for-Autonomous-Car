import pandas as pd
import os
import cv2
from datetime import datetime

global imageList, steeringList
folderCounter = 0
count = 0
imageList = []
steeringList = []

# get current directory path
myDir = os.path.join(os.getcwd(), '')
# print(myDir)

# create a new folder based on the previous folder counter
while os.path.exists(os.path.join(myDir, f'IMG{str(folderCounter)}')):
    folderCounter += 1
newPath = myDir + "/IMG" + str(folderCounter)
os.makedirs(newPath)

# save images in the newly created folder
def saveImages(image, steering):
    global imageList, steeringList
    curr = datetime.now()
    timestamp = str(datetime.timestamp(curr)).replace('.', '')
    # print("timestamp = ", timestamp)
    fileName = os.path.join(newPath, f'Image_{timestamp}.jpg')
    cv2.imwrite(fileName, image)
    imageList.append(fileName)
    steeringList.append(steering)

# save log file when session ended
def saveLog():
    global imageList, steeringList
    rawData = {'Image': imageList,
               'Steering': steeringList}
    dataFrame = pd.DataFrame(rawData)
    dataFrame.to_csv(os.path.join(myDir, f'log_{str(folderCounter)}.csv'), index=False, header=False)
    print('Log Saved!')
    print('Total numbers of Images: ', len(imageList))

if __name__ == '__main__':
    cam = cv2.VideoCapture(1)
    for x in range (10):
        _, img = cam.read()
        saveImages(img, 0.5)
        cv2.waitKey(1)
        cv2.imshow("Image", img)
    saveLog()