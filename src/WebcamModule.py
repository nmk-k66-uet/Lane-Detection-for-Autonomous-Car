import cv2

cam = cv2.VideoCapture(0)


def getImage(display = False, size = [480, 480]):
    _, image = cam.read()
    image = cv2.resize(image, (size[0], size[1]))
    if display:
        cv2.imshow('IMG', image)
    return image

if __name__ == '__main__':
    while True:
        image = getImage(True)