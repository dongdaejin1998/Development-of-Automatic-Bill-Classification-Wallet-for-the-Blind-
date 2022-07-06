import cv2
import numpy as np

# shadow remove
def shadow_romove1(img):
    GrayImg_1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dilated_img = cv2.dilate(GrayImg_1, np.ones((7, 7), np.uint8))
    bg_img = cv2.medianBlur(dilated_img, 21)
    diff_img = 255 - cv2.absdiff(GrayImg_1, bg_img)
    norm_img = diff_img.copy()  # Needed for 3.x compatibility
    cv2.normalize(diff_img, norm_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    _, thr_img = cv2.threshold(norm_img, 230, 0, cv2.THRESH_TRUNC)
    cv2.normalize(thr_img, thr_img, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
    cv2.imwrite("./shadow/shadow1.jpg",thr_img)

def shadow_remove2(img):
    # 그림자 제거
    rgb_planes = cv2.split(img)
    result_planes = []
    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_planes.append(diff_img)
        result_norm_planes.append(norm_img)
    remove_shadow_img = cv2.merge(result_planes)
    remove_shadow_img_norm = cv2.merge(result_norm_planes)
    cv2.imwrite("./shadow/shadow2.jpg", remove_shadow_img_norm)
    cv2.imwrite("./shadow/shadow3.jpg", remove_shadow_img)
    return remove_shadow_img
