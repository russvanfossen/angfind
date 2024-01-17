import cv2
import numpy as np
import math
from argparse import ArgumentParser

points = []


def drawcircle(event, x, y, flags, params):
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(img, (int(x), int(y)), 6, (255, 0, 0), -1)
        if len(points) == 1:
            cv2.line(img, tuple(points[0]), (x, y), (255, 0, 0), 3)
        if len(points) == 3:
            cv2.line(img, tuple(points[2]), (x, y), (255, 0, 0), 3)
        points.append([x, y])
        cv2.imshow('image', img)
        print(points)
        if len(points) == 4:
            degrees = find_angle()
            print(degrees)
        if len(points) > 4:
            exit()


def find_angle():
    a = points[0]
    b = points[1]
    c = points[2]
    d = points[3]
    m1 = slope(a, b)
    m2 = slope(c, d)
    angle = math.atan((m2 - m1) / 1 + m1 * m2)
    angle = round(math.degrees(angle))
    if angle < 0:
        angle = 180 + angle
    cv2.putText(img, str(angle), (int(img.shape[1]/2), int(img.shape[0]/2)), cv2.FONT_HERSHEY_DUPLEX, 5, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.imshow('image', img)
    return angle


def slope(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def main():
    img_path = input("File Path to Image:")
    global img
    img = cv2.imread(img_path)
    while True:
        cv2.putText(img, 'Press Q to quit, R to reset.', (10, 10), cv2.FONT_HERSHEY_DUPLEX, .5,
                    (0, 0, 255), 1, cv2.LINE_AA)
        cv2.imshow('image', img)
        cv2.setMouseCallback('image', drawcircle)
        if cv2.waitKey() & 0xff == ord('r'):
            cv2.putText(img, 'Press Q to quit, R to reset.', (10, 10), cv2.FONT_HERSHEY_DUPLEX, .5,
                        (0, 0, 255), 1, cv2.LINE_AA)
            img = cv2.imread(img_path)
            global points
            points = []
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', drawcircle)
        if cv2.waitKey() & 0xff == ord('q'):
            break


if __name__ == '__main__':
    main()