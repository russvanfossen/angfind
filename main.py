import cv2
import math
import PySimpleGUI as sg

points = []
degrees_list = []
img = ''


def drawcircle(event, x, y, flags, params):
    # global img
    global points
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
            degrees_list.append(degrees)
            print(degrees_list)
            cv2.destroyAllWindows()
            points = []


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
    return angle


def slope(p1, p2):
    return (p2[1] - p1[1]) / (p2[0] - p1[0])


def main():
    sg.theme('Light Blue 2')

    layout1 = [[sg.Text('Enter 2 Images')],
               [sg.Text('File 1', size=(8, 1)), sg.Input(), sg.FileBrowse()],
               [sg.Text('File 2', size=(8, 1)), sg.Input(), sg.FileBrowse()],
               [sg.Submit(), sg.Cancel()]]

    window = sg.Window('Angle Finder', layout1)

    event, values = window.read()
    window.close()
    print(f'You clicked {event}')
    print(f'You chose filenames {values[0]} and {values[1]}')
    print(values)

    if event == "Submit":
        if not len(values[0]) or not len(values[1]):
            sg.popup('Please enter 2 files to compare')
        else:
            global img
            global points
            points = []
            # img_path_1 = input("File Path to Image 1:")
            img_path_1 = values[0]
            img = cv2.imread(img_path_1)
            cv2.putText(img, 'Press Q to quit', (10, 10), cv2.FONT_HERSHEY_DUPLEX, .5,
                        (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', drawcircle)
            k = cv2.waitKey(0)
            if k == ord('q'):
                cv2.destroyAllWindows()

            # img_path_2 = input("File Path to Image 2:")
            img_path_2 = values[1]
            img = cv2.imread(img_path_2)
            cv2.putText(img, 'Press Q to quit', (10, 10), cv2.FONT_HERSHEY_DUPLEX, .5,
                        (0, 0, 255), 1, cv2.LINE_AA)
            cv2.imshow('image', img)
            cv2.setMouseCallback('image', drawcircle)
            k = cv2.waitKey(0)
            if k == ord('q'):
                cv2.destroyAllWindows()
            diff_result = abs(degrees_list[1] - degrees_list[0])
            sg.popup(f'The angle difference is {diff_result}°')


if __name__ == '__main__':
    main()
