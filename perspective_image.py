import cv2 as cv
import numpy as np

frame=cv.imread("capture.jpg")
a=np.load("camera_coordinate.npy")

def image_wraping(a):

    sm=a.sum(axis=1)
    diff=np.diff(a,axis=1)

    topLeft = a[np.argmin(sm)]  # x+y가 가장 작은 값이 좌상단 좌표
    bottomRight = a[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
    topRight = a[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
    bottomLeft = a[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표

    pts1 = np.float32([topLeft, topRight, bottomRight, bottomLeft])

    # 변환 후 영상에 사용할 서류의 폭과 높이 계산
    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(topRight[0] - topLeft[0])
    h1 = abs(topRight[1] - bottomRight[1])
    h2 = abs(topLeft[1] - bottomLeft[1])
    width = max([int(w1), int(w2)])  # 두 좌우 거리간의 최대값이 서류의 폭
    height = max([int(h1), int(h2)])  # 두 상하 거리간의 최대값이 서류의 높이

    # 변환 후 4개 좌표
    pts2 = np.float32([[0, 0], [width - 1, 0],
                       [width - 1, height - 1], [0, height - 1]])

    # 변환 행렬 계산

    mtrx = cv.getPerspectiveTransform(pts1, pts2)


    return mtrx,width,height

mtrx,width,height=image_wraping(a)
# 원근 변환 적용
frame = cv.warpPerspective(frame, mtrx, (width, height))

cv.imshow('image', frame)
cv.waitKey(0)
cv.destroyAllWindows()
