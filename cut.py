import numpy as np
import cv2



def cut_half(img):
    img1=img.copy()

    height, width = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    # 선을 추출
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100, minLineLength=80, maxLineGap=5)
    tmp_candy = []
    tmp_abs = []


    for i in range(len(lines)):
        for x1,y1,x2,y2 in lines[i]:
            cv2.line(img1, (x1, y1), (x2, y2), (0, 255, 0), 1)
            gapY = np.abs(y2-y1)
            gapX = np.abs(x2-x1)
            # 선의 x축의 차이가 5이하 y축의 차이가 10이상이면 세로줄로 판별
            if gapX < 5 and gapY > 50 :
                tmp_candy.append(x1)
                tmp_abs.append(np.abs(x1- width//2))

    left_img = img[0:height,0:tmp_candy[np.argmin(tmp_abs)]]
    right_img = img[0:height,tmp_candy[np.argmin(tmp_abs)]+1:width]
    cv2.imwrite("./cut_image/gray.jpg",gray)
    cv2.imwrite("./cut_image/edges.jpg",edges)
    cv2.imwrite("./cut_image/lines.jpg",img1)
    cv2.imwrite("./cut_image/left.jpg",left_img)
    cv2.imwrite("./cut_image/right.jpg",right_img)

    cv2.waitKey(0)
    return left_img, right_img

def cut_half2(image):
    print("a")
    # Convert RGB to grayscale:
    grayscaleImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Set the sample ROI and crop it:
    (imageHeight, imageWidth) = grayscaleImage.shape[:2]
    roiX = 0
    roiY = int(0.05 * imageHeight)
    roiWidth = imageWidth
    roiHeight = int(0.05 * imageHeight)

    # Crop the image:
    imageRoi = grayscaleImage[roiY:roiY + roiHeight, roiX:roiWidth]

    # Thresholding:
    _, binaryImage = cv2.threshold(imageRoi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Reduce the ROI to a 1 x imageWidth row:
    reducedImg = cv2.reduce(binaryImage, 0, cv2.REDUCE_MAX)

    # Store the transition positions here:
    linePositions = []

    # Find transitions from 0 to 255:
    pastPixel = 255
    for x in range(reducedImg.shape[1]):
        print(x)
        # Get current pixel:
        currentPixel = reducedImg[0, x]
        # Check for the "jumps":
        if currentPixel == 255 and pastPixel == 0:
            # Store the jump locations in list:
            print("Got Jump at:" + str(x))
            linePositions.append(x)
        # Set current pixel to past pixel:
        pastPixel = currentPixel
    print(linePositions)
    # Crop pages:
    for i in range(len(linePositions)):
        # Get top left:
        cropX = linePositions[i]

        # Get top left:
        if i != len(linePositions) - 1:
            # Get point from the list:
            cropWidth = linePositions[i + 1]
        else:
            # Set point from the image's original width:
            cropWidth = reducedImg.shape[1]

        # Crop page:
        cropY = 0
        cropHeight = imageHeight
        currentCrop = image[cropY:cropHeight, cropX:cropWidth]

        # Show current crop:
        cv2.imshow("CurrentCrop", currentCrop)
        cv2.waitKey(0)

