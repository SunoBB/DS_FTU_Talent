import os
import cv2
import numpy as np




def detect(file):
    video = cv2.VideoCapture(file)
    font = cv2.FONT_HERSHEY_SIMPLEX
    vid = cv2.VideoCapture(file)
    while True:
        ret, img = vid.read()

        try:

            roi = img[70:200,450:700]

            if ret != None:


                img_hsv=cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

                # lower mask (0-10)
                lower_red = np.array([0,50,50])
                upper_red = np.array([10,255,255])
                mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

                # upper mask (170-180)
                lower_red = np.array([170,50,50])
                upper_red = np.array([180,255,255])
                mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

                # join my masks
                maskr = cv2.add(mask0, mask1)

                size = img.shape

                r_circles = cv2.HoughCircles(maskr, cv2.HOUGH_GRADIENT, 1, 80,
                                                param1=50, param2=10, minRadius=0, maxRadius=30)

                r = 5
                bound = 4.0 / 10
                if r_circles is not None:
                    r_circles = np.uint16(np.around(r_circles))

                    for i in r_circles[0, :]:
                        if i[0] > size[1] or i[1] > size[0] or i[1] > size[0] * bound:
                            continue

                        h, s = 0.0, 0.0
                        for m in range(-r, r):
                            for n in range(-r, r):

                                if (i[1] + m) >= size[0] or (i[0] + n) >= size[1]:
                                    continue
                                h += maskr[i[1] + m, i[0] + n]
                                s += 1
                        if h / s > 50:
                            cv2.circle(roi, (i[0], i[1]), i[2] + 10, (0, 255, 0), 2)
                            cv2.circle(maskr, (i[0], i[1]), i[2] + 30, (255, 255, 255), 2)
                            cv2.putText(roi, 'RED', (i[0], i[1]), font, 1, (255, 0, 0), 2, cv2.LINE_AA)
                            cv2.imshow(",",img)
                            cv2.imshow('detected results', roi)
        except TypeError as e:
            print(e)
            break


        # cv2.imshow('roi', roi)
        # cv2.imshow('img', img)

        if cv2.waitKey(1) & 0xFF == ord('q'): #type q to quit/exit
            break

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect('~/Check_traffic_light/DetectTrafic/main.mp4')