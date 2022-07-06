import numpy as np
import cv2


def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # return the ordered coordinates
    return rect


def auto_scan_image(image):
    # load the image and compute the ratio of the old height
    # to the new height, clone it, and resize it
    # document.jpg ~ docuemnt7.jpg

    orig = image.copy()
    r = 800.0 / image.shape[0]
    dim = (int(image.shape[1] * r), 800)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    # convert the image to grayscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    kernel = np.ones((5, 5), np.uint8)  # Reduce Noise Of Image
    erosion = cv2.erode(gray, kernel, iterations=1)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    edged = cv2.Canny(closing, 20, 240)

    # show the original image and the edge detected image
    #print("STEP 1: Edge Detection")
    #cv2.imshow("Image", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    # cv2.waitKey(1)
    thresh = cv2.adaptiveThreshold(edged, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts, _ = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    # show the contour (outline) of the piece of paper
    #print("STEP 2: Find contours of paper")

    cv2.drawContours(image, screenCnt, -1, (0, 255, 0), 25)
    #cv2.imshow("Outline", image)
    #cv2.imwrite("./scan_book/book1.jpg",image)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()


    # apply the four point transform to obtain a top-down
    # view of the original image
    rect = order_points(screenCnt.reshape(4, 2) / r)
    (topLeft, topRight, bottomRight, bottomLeft) = rect

    w1 = abs(bottomRight[0] - bottomLeft[0])
    w2 = abs(topRight[0] - topLeft[0])
    h1 = abs(topRight[1] - bottomRight[1])
    h2 = abs(topLeft[1] - bottomLeft[1])
    maxWidth = max([int(w1), int(w2)])
    maxHeight = max([int(h1), int(h2)])

    dst = np.float32([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]])

    M = cv2.getPerspectiveTransform(rect, dst)

    warped = cv2.warpPerspective(orig, M, (maxWidth, maxHeight))

    # show the original and scanned images
    #print("STEP 3: Apply perspective transform")
    #cv2.imshow("Warped", warped)
    #cv2.imwrite("./scan_book/warped.jpg",warped)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    return warped

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
