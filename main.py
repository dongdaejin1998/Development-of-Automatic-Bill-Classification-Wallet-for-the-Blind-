import cv2
import numpy as np
import auto_scan_image,tesseract_test,ocr_preprocessing,shadow
#import serial
#import arduino
import time,math

"""
cap=cv2.VideoCapture('http://192.168.142.230:8080/video')


b = serial.Serial('/dev/ttyACM0', 9600)


while True:

    ret,frame=cap.read()


    frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
    a = b.readline().decode("utf-8")
    a = str(a)
    #print(a)
    ard1 = str(a[0:4])
    #start = time.time()
    if ard1=='capt':
        break


#cv2.imwrite("original.jpg",frame)
cv2.imshow("result", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


frame=cv2.imread("test1.jpg")
frame=cv2.resize(frame,dsize=(0,0),fx=2,fy=2)
start = time.time()
image=shadow.shadow_remove2(frame)
#cv2.imwrite("remove_shadow.jpg",image)
cv2.imshow("result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("!")
image=auto_scan_image.auto_scan_image(image)
#cv2.imwrite("perspective.jpg",image)
cv2.imshow("result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
print("2")



image=ocr_preprocessing.preprocessing(image)
print("3")
cv2.imshow("result", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#cv2.imwrite("preprocessing.jpg",image)
string_array=tesseract_test.ocr(image)
print("4")
math.factorial(100000)
end=time.time()
print(f"{end - start:.5f}sec")
#gg=arduino.send_data(string_array)
#if gg==False:
#    print("종료되었습니다.")






