import serial



arduino = serial.Serial('/dev/ttyACM0', 9600)

def send_data(string):
    count = 0
    prev_count = 0
    print(len(string))

    while True:
        a = arduino.readline().decode("utf-8")
        a = str(a)
        #print(a)
        ard1 = str(a[0:4])

        if ard1=='next':
            print(count)
            a = string[count]
            b=' '.join(s for s in a)
            print(b)
            c = b.encode('utf-8')
            arduino.write(c)
            count = count + 1
            prev_count = count - 1
            print(prev_count)
            print(count)
            if len(string) == count:
                daum = False
                break
        elif ard1=='prev':
            print(prev_count)
            prev_count = prev_count - 1
            print(prev_count)
            if 0 ==prev_count:
                daum = False
                break
            a = string[prev_count]
            b=' '.join(s for s in a)
            print(b)
            c = b.encode('utf-8')
            arduino.write(c)
            count = prev_count + 1


    return daum




def test_send_data(string):

    count = 0
    prev_count=0
    while True:
        a=input()
        #print(a)
        if a == "e":
            print(prev_count)
            prev_count = prev_count - 1
            print(prev_count)
            b = string[prev_count]
            print(b)
            count = prev_count + 1
            #c = b.encode('utf-8')
            #arduino.write(c)
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
    return daum


