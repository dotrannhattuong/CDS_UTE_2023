import time
import cv2
def go_straight(arrmax, arrmin, edges):
    if (arrmax > (edges.shape[1]-30) and arrmin > 15):
        center = arrmin + 34
    elif (arrmax < (edges.shape[1]-15) and arrmin < 30):
        center = arrmax - 34 
    else: center = 1
    return center
def controller(edges, PID, current_angle, current_speed, conf_OD, cls_OD, S, right, left, straight):
    """detect duong thang"""
    straightarr = []
    lineStraight = edges[10,:]
    for x,y in enumerate(lineStraight):
        if y==255:
            straightarr.append(x)
    try: 
        straightmax=max(straightarr)
        straight_detect = 1
    except Exception as er:
        straight_detect = 0
        print('ko co duong thang')
        pass
    """"""
    """detect trai"""
    leftarr = []
    lineLeft = edges[:,5]
    for x,y in enumerate(lineLeft):
        if y==255:
            leftarr.append(x)
    try:
        leftmin=min(leftarr)
        if (leftmin>25):
            left_detect = 0
        else: left_detect = 1
        print('left', left_detect)
    except Exception as er:
        left_detect = 5
        pass
    """"""
    """detect phai"""
    rightarr = []
    lineRight = edges[:,155]
    for x,y in enumerate(lineRight):
        if y==255:
            rightarr.append(x)
    try:
        rightmin=min(rightarr)
        if (rightmin>25):
            right_detect = 0
        else: right_detect = 1
        print('right', right_detect)
    except Exception as er:
        right_detect = 5
        pass
    ###############################################################################
    ###############################################################################
    arr=[]
    lineRow = edges[20,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    arrmax=max(arr)
    arrmin=min(arr)
    set_point = int(edges.shape[1]/2) 
    # print(arrmax-arrmin) #67-68, duonh mot lane, 90 duong 2 lane -> arrmax-25, loi gap nga ba, nga tu
    ###############################################################################
    """detect 2 lane va background"""
    if ((arrmax - arrmin)>85  and (arrmax-arrmin)<105 and straight_detect==1):
        twolanearr = []
        linetwolane = edges[12,:]
        for x,y in enumerate(linetwolane):
            if y==255:
                twolanearr.append(x)
        two_lane_min = min(twolanearr)
        two_lane_max = max(twolanearr)
        if (two_lane_min > 10 and two_lane_max < 150):
            arrmin = arrmax - 10
            set_point = int(edges.shape[1]/2) + 20
            two_lane=1
            print('duong 2 lane')
    else: two_lane=0
    if (arrmax < (edges.shape[1]/2+30) and arrmin > 20 and two_lane==0):
        center = arrmin + 34 #cho lech de no cua ve
    elif (arrmin > (edges.shape[1]/2-30) and arrmax < 140 and two_lane==0):
        center = arrmax - 34 #cho lech de no cua ve
    else: center = int((arrmax + arrmin)/2)
    ############################################################################### tra ve set_point, center
    ###############################################################################
    """xu li di thang thang"""
    if (straight==1 and cls_OD==0):
        center = go_straight(arrmax=arrmax, arrmin=arrmin, edges=edges)
        if (center==1):
            center = int((arrmax + arrmin)/2)
        straight=0
        print('go straight')
    if (conf_OD > 0.7):
        if (cls_OD==2): 
            if (S>350):
                straight=1
    ############################################################################### tra ve center
    error = set_point - center
    angle = -PID(error, 0.29, 0.00, 0.005)#0.3 fps 25 - 30
    ############################################################################### 
    """xu li re phai nga ba thang tam on, chua fix duong hai lane"""
    if (right==1):
        time.sleep(0.6)
        right = 0
    if (conf_OD > 0.6):
        if (cls_OD==1):
            if (S > 405):     
                speed = -12
                angle = 25
                right = 1
    """xu li re trai nga ba thang, chua fix 2 lane"""
    if (left==1):
        time.sleep(0.5)
        left = 0
    if (conf_OD > 0.6):
        if (cls_OD==8):
            if (S > 850):     
                speed = -3
                angle = -25
                left = 1
    """xu li bien no straight"""
    if (conf_OD > 0.7):
        if (cls_OD==5):
            if (right_detect==1):
                if (S>450):
                    speed = -12
                    angle = 25
                    right = 1
            elif (left_detect==1):
                if (S>650):
                    speed = -5
                    angle = -25
                    left = 1
    # """xu li bien no turn left"""
    # if (conf_OD > 0.7):
    #     if (cls_OD==3):
    #         if (straight_detect==1):
    #             k
    #         elif (right_detect==1):
    #             if (S>450):
    #                 speed = -12
    #                 angle = 25
                    # right = 1
            # elif (straight_detect==1):
            #     if (S>650):
            #         speed = -5
            #         angle = -25
            #         left = 1
    ############################################################################### tra ve angle and speed
    if (right==0 and left==0):
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
    # cv2.circle(edges,(arrmin,20),5,(0,0,0),2)
    # cv2.circle(edges,(arrmax,20),5,(0,0,0),2)
    cv2.line(edges,(center,20),(int(edges.shape[1]/2 + 20),edges.shape[0]),(0,0,0),2)
    cv2.imshow("IMG", edges)
    key = cv2.waitKey(1)
    return angle, speed, right, left, straight