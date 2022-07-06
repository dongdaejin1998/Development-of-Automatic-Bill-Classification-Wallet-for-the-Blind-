import pytesseract
from PIL import Image
from jamo import h2j,j2hcj
#import arduino
import cv2

korean_table = {
' ':"0",
    'ㄱ': '1',
    'ㄴ': '2',
    'ㄷ': '3',
    'ㄹ': '4',
    'ㅁ': '5',
    'ㅂ': '6',
    'ㅅ': '7',
    'ㅇ': '8',
    'ㅈ': '9',
    'ㅊ': '10',
    'ㅋ': '11',
    'ㅌ': '12',
    'ㅍ': '13',
    'ㅎ': '14',
    'ㅏ': '15',
    'ㅑ': '16',
    'ㅓ': '17',
    'ㅕ': '18',
    'ㅗ': '19',
    'ㅛ': '20',
    'ㅜ': '21',
    'ㅠ': '22',
    'ㅡ': '23',
    'ㅣ': '24',
    'ㅐ': '25',
    'ㅒ': '26',
    'ㅔ': '27',
    'ㅖ': '28',
    'ㅘ': '29',
    'ㅙ': '30',
    'ㅚ': '31',
    'ㅝ': '32',
    'ㅞ': '33',
    'ㅟ': '34',
    'ㅢ': '35',
    '.': '36',
'?': '37',
'!': '38',
',': '39',
'-': '40',
'"': '41',
'~':'42',
'1': '43',
'2': '44',
'3': '45',
'4': '46',
'5': '47',
'6': '48',
'7': '49',
'8': '50',
'9': '51',
'0': '52',
'ㄲ': '1',
'ㄸ': '3',
'ㅃ': '6',
'ㅆ': '7',
'ㅉ': '9',
'ㄳ':'7',
'ㄺ':'1',
'ㅀ':'13',
'ㄵ':'9',
'ㄶ':'13',
'ㅄ':'7',
'ㄻ':'5',
'ㄼ':'6',
'ㄾ':'12',
'[':'61',
']':'62',

#'ㅒ':,
#'ㅙ':,
#'ㅞ':,
#'ㅟ':
}
def ocr(image):


    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


    data = pytesseract.image_to_osd(image)
    #print(data)
    keys = []
    values = []
    data_list = data.split("\n")
    data_list.pop()
    for i in data_list:
        pair = i.split(":")
        keys.append(pair[0])
        values.append(pair[1])
    #print(keys)
    #print(values)
    my_dict = dict(zip(keys, values))

    #print(my_dict)
    if my_dict["Rotate"]==" 180":
        image=cv2.rotate(image,cv2.ROTATE_180)
        cv2.imshow("hi", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    elif my_dict["Rotate"] == " 0":
        image=image
        cv2.imshow("hi", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    text = pytesseract.image_to_string(image, lang='Hangul')
    print(text)
    string = korea_divide(text)
    return string
    #korea_divide(text)
    #os.remove("save_image.jpg")

    



def korea_divide(text):
    jamo_str=j2hcj(h2j(text))
    #print(jamo_str)
    jamo_str=jamo_str.replace("\n", "")
    jamo_str = jamo_str.replace("\f", "")
    count=0
    j=0
    a=[]
    a.append([])
    for i in range(len(jamo_str)):
        if jamo_str[i]=="ㄲ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("66")
                count = count + 1
        elif jamo_str[i] == "ㄸ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("66")
                count = count + 1
        elif jamo_str[i] == "ㅃ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("66")
                count=count+1
        elif jamo_str[i] == "ㅆ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("66")
                count=count+1
        elif jamo_str[i] == "ㅉ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("66")
                count=count+1
        elif jamo_str[i] == "ㄶ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("2")
                count=count+1
        elif jamo_str[i] == "ㄺ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("4")
                count=count+1
        elif jamo_str[i] == "ㄳ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("1")
                count=count+1
        elif jamo_str[i] == "ㅀ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("4")
                count=count+1
        elif jamo_str[i] == "ㄵ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("2")
                count=count+1
        elif jamo_str[i] == "ㅄ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("6")
                count=count+1
        elif jamo_str[i] == "ㄻ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("4")
                count=count+1
        elif jamo_str[i] == "ㄼ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("4")
                count=count+1
        elif jamo_str[i] == "ㄾ":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("4")
                count=count+1
        elif jamo_str[i] == "~":
            if count >= 7:
                count = 0
                j = j + 1
                a.append([])
            else:
                a[j].append("67")
                count=count+1
        chuga=korean_table.get(jamo_str[i],"0")
        korean_table[jamo_str[i]]=chuga
        korean=korean_table[jamo_str[i]]

        a[j].append(korean)

        count=count+1

        if count>7:
            count=0
            j=j+1
            if len(a[j-1])==8:
                a.append([])
            else:
                break
    if len(a[-1])==0:
        del a[-1]
    elif len(a[-1])!=8:
        for i in range(8-len(a[-1])):
            a[-1].append("0")
    #for i in range(len(a)):
    #    print(str(a[i])+"\n")
    return a

"""
str1="김동규"
a=korea_divide(str1)
str2="서동민 낄쌈해 않아 1 0 10"
count=0
string=korea_divide(str2)
daum=arduino.test_send_data(string)
if daum==False:
    print("끝")
"""