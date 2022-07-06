import cv2
import numpy as np

win_name = "scanning"
cap = cv2.VideoCapture('http://192.168.1.103:8080/video')

pts_cnt = 0
pts = np.zeros((4, 2), dtype=np.float32)

def onMouse(event, x, y, flags, param):
    global pts_cnt
    if event == cv2.EVENT_LBUTTONDOWN:
        # 좌표에 초록색 동그라미 표시
        cv2.circle(frame, (x, y), 10, (0, 255, 0), -1)
        cv2.imshow(win_name, frame)

        # 마우스 좌표 저장
        pts[pts_cnt] = [x, y]
        print(pts)
        pts_cnt += 1
        if pts_cnt == 4:
            # 좌표 4개 중 상하좌우 찾기
            sm = pts.sum(axis=1)  # 4쌍의 좌표 각각 x+y 계산
            diff = np.diff(pts, axis=1)  # 4쌍의 좌표 각각 x-y 계산

            topLeft = pts[np.argmin(sm)]  # x+y가 가장 값이 좌상단 좌표
            bottomRight = pts[np.argmax(sm)]  # x+y가 가장 큰 값이 우하단 좌표
            topRight = pts[np.argmin(diff)]  # x-y가 가장 작은 것이 우상단 좌표
            bottomLeft = pts[np.argmax(diff)]  # x-y가 가장 큰 값이 좌하단 좌표

            # 변환 전 4개 좌표
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
            mtrx = cv2.getPerspectiveTransform(pts1, pts2)

            # 원근 변환 적용
            np.savez("camera_coordinate",mtrx=mtrx,width=width,height=height)
            print(mtrx,width,height)

            result = cv2.warpPerspective(frame, mtrx, (width, height))
            cv2.imshow('scanned', result)


while True:
    ret, frame = cap.read()
    frame=cv2.resize(frame,dsize=(0,0),fx=0.9,fy=0.9)
    frame=cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imshow(win_name, frame)
    cv2.setMouseCallback(win_name, onMouse)
    rows, cols = frame.shape[:2]
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break







