"""

def auto_scan_image2(img):

    height, width, channels = img.shape  # Find Height And Width Of Image

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # RGB To Gray Scale

    kernel = np.ones((5, 5), np.uint8)  # Reduce Noise Of Image
    erosion = cv2.erode(gray, kernel, iterations=1)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

    edges = cv2.Canny(closing, 20, 240)  # Find Edges

    # Get Threshold Of Canny
    thresh = cv2.adaptiveThreshold(edges, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Find Contours In Image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Find Biggest Contour
    areas = [cv2.contourArea(c) for c in contours]
    max_index = np.argmax(areas)
    print(max_index)

    # Find approxPoly Of Biggest Contour
    epsilon = 0.1 * cv2.arcLength(contours[max_index], True)
    approx = cv2.approxPolyDP(contours[max_index], epsilon, True)

    # Crop The Image To approxPoly
    pts1 = np.float32(approx)
    pts = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts)
    result = cv2.warpPerspective(img, matrix, (width, height))

    #flip = cv2.flip(result, 1)  # Flip Image
    #rotate = cv2.rotate(flip, cv2.ROTATE_90_COUNTERCLOCKWISE)  # Rotate Image
    cv2.imwrite("./scan_book/warped1.jpg",result)
    cv2.imshow('Result', result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result

"""


"""
if a == "e":
    print(prev_count)
    prev_count = prev_count - 1
    print(prev_count)
    b = string[prev_count]
    print(b)
    count = prev_count + 1
    # c = b.encode('utf-8')
    # arduino.write(c)
    if 0 > prev_count:
        daum = False
        break
        
        
elif a == "q":
    print(count)
    b = string[count]
    print(b)
    count = count + 1
    prev_count = count-1
    print(prev_count)
    print(count)
    #c = b.encode('utf-8')
    #arduino.write(c)
    if len(string) == count:
        daum = False
        break
"""