import time
def controller(edges, PID, current_angle, current_speed, conf_OD, cls_OD, S, right, left, straight):
    arr=[]
    lineRow = edges[20,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    arrmax=max(arr)
    arrmin=min(arr)
    center = int((arrmax + arrmin)/2)
    error = int(edges.shape[1]/2) - center
    angle = -PID(error, 0.29, 0.00, 0.005)#0.3 fps 25 - 30
    """detect duong thang"""
    straightarr = []
    lineStraight = edges[5,:]
    for x,y in enumerate(lineStraight):
        if y==255:
            straightarr.append(x)
    try: 
        straightmax=max(straightarr)
        straightmin=min(straightarr)
    except Exception as er:
        straightmax=0
        straightmin=0
        print('ko co duong thang')
        pass
    """"""
    """detect trai"""
    leftarr = []
    lineLeft = edges[:,10]
    for x,y in enumerate(lineLeft):
        if y==255:
            leftarr.append(x)
    try:
        leftmin=min(leftarr)
        if (leftmin>25):
            print('ko co duong trai')
        else: print('co duong trai')
    except Exception as er:
        pass
    """"""
    """detect trai"""
    rightarr = []
    lineRight = edges[:,150]
    for x,y in enumerate(lineRight):
        if y==255:
            rightarr.append(x)
    try:
        rightmin=min(rightarr)
        if (rightmin>25):
            print('ko co duong phai')
        else: print('co duong phai')
    except Exception as er:
        pass
    """"""
    """xu li re phai nga ba thang tam on, chua fix duong hai lane"""
    if (right==1):
        time.sleep(0.5)
        right = 0
    if (conf_OD > 0.6):
        if (cls_OD==1):
            if (S > 450):     
                speed = -12
                angle = 25
                right = 1
    """xu li re trai nga ba thang, chua fix 2 lane"""
    if (left==1):
        time.sleep(0.5)
        left = 0
    if (conf_OD > 0.6):
        if (cls_OD==8):
            if (S > 650):     
                speed = -5
                angle = -25
                left = 1
    """xu li di thang thang, fix bong ram"""
    if (straight==1):
        time.sleep(1)
        straight = 0
    if (conf_OD > 0.8):
        if (cls_OD==2):
            if (S > 1000):     
                speed = 150
                angle = 0
                straight = 1
    """xu li bien no straight"""

    if (right==0 and left==0 and straight==0):
        if (abs(float(current_angle))<3):
            if (float(current_speed)> 45):
                speed = 0
            else: speed = 150
        elif (abs(float(current_angle))<7 and abs(float(current_angle))>2):
            if (float(current_speed)< 40):
                speed = 150
            elif (float(current_speed)< 42):
                speed = 0
            else: speed = -10
        elif (abs(float(current_angle))>6 and abs(float(current_angle))<11):
            if (float(current_speed)< 38):
                speed = 150
            elif (float(current_speed)< 40):
                speed = 0
            else: speed = -13
        else:
            if (float(current_speed)< 36):
                speed = 150
            elif (float(current_speed)< 38):
                speed = 0
            else: speed = -15
    return angle, speed, right, left, straight