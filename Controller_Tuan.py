import time
import cv2
def go_straight(arrmax, arrmin, left_detect, right_detect):
    if (right_detect==1):
        center = arrmin + 25
    elif (left_detect==1):
        center = arrmax - 25 
    else: center = 1
    return center
def turn_left(current_speed):
    if (float(current_speed)>=45):
        speed= 0
    elif (float(current_speed>=43)): 
        speed= 25
    angle = -25
    return angle, speed
def turn_right(current_speed):
    if (float(current_speed)>=45):
        speed= 0
    elif (float(current_speed>=43)): 
        speed= 25
    else: speed = 50
    angle = 25
    return angle, speed
def controller(edges, PID, current_angle, current_speed, conf_OD, cls_OD, S, right, left, straight):
    """detect duong thang"""
    S_left = 750
    S_right = 450 # voi van toc 45
    straightarr = []
    line = 15
    set_speed = 0
    two_lane=0
    if (float(current_speed)<44):
        S_right = 460
    if (cls_OD==0 and float(current_speed)<47):
        line = 18
    lineStraight = edges[5,:]
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
    lineLeft = edges[:,10]
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
    lineRight = edges[:,150]
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
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    arrmax=max(arr)
    arrmin=min(arr)
    set_point = int(edges.shape[1]/2) 
    print('chieu dai duong...................', arrmax-arrmin) 
    if (conf_OD==0):
        if (left_detect==1 and right_detect==0 and straight_detect==0 and arrmax >((edges.shape[1]/2) + 10)): #cua trai
            if (arrmin > 30 and float(current_speed)>51):
                arrmax = arrmax + 34
                print('change arrmax')
        elif (right_detect==1 and left_detect==0 and straight_detect==0 and arrmin < ((edges.shape[1]/2) - 10)): #cua phai
            if (arrmax < 130 and float(current_speed)>51):
                arrmin = arrmin - 34
                print('change arrmin')
    ###############################################################################
    center = int((arrmax + arrmin)/2)
    """xu li di thang thang"""
    if (straight==1):
        center = go_straight(arrmax=arrmax, arrmin=arrmin, left_detect=left_detect, right_detect=right_detect)
        if (center==1):
            center = int((arrmax + arrmin)/2)
        straight=0
        print('go straight')
    if (conf_OD > 0.75):
        if (cls_OD==2): 
            straight=1
    error = set_point - center
    print('error:...............', error)
    angle = -PID(error, 0.32, 0.0002, 0.007)#0.3 fps 25 - 30
    ##################################################################################
    if (arrmax < 110 and arrmin > 50 and two_lane==0 and (arrmax - arrmin)<=45 and line==15):
        print('bong ram')
        if (arrmax < 110):
            arrmax = arrmin + 51
        else: arrmin = arrmax - 51
    if (arrmax < 115 and arrmin > 45 and two_lane==0 and (arrmax - arrmin)<=55 and line==17):
        print('bong ram')
        if (arrmax < 110):
            arrmax = arrmin + 61
        else: arrmin = arrmax - 61
    if (conf_OD>0): #and cls_OD!=7):
        set_speed=45
    """xu li re phai"""
    if (right==1):
        print('speed:......................................................................', float(current_speed))  
        right=0
        t1 = time.time()
        while ((time.time()-t1)<0.5):
            if ((arrmax-arrmin)>45 and (arrmax-arrmin)<57 and arrmin > 10 and arrmax < 150):
                print('breaking----------------------', arrmax-arrmin)
                # break
    if (conf_OD > 0.6):
        if (cls_OD==1):
            if(arrmax>=140):
                if (left_detect==1):
                    S_right=415
                    arrmin = 60
                else: angle=-0.5
            if (S > S_right):   
                angle, speed = turn_right(current_speed=float(current_speed))
                right = 1
    ##################################################################################
    """xu li re trai nga"""
    if (left==1):
        print('speed ......................................................................:', float(current_speed))
        left = 0
        t2 = time.time()
        while ((time.time()-t2)<0.52):
            if ((arrmax-arrmin)>45 and (arrmax-arrmin)<57 and arrmin > 10 and arrmax < 150):
                print('breaking----------------------', arrmax-arrmin)
    if (conf_OD > 0.6):
        if (cls_OD==8):
            if (arrmin==0):
                if (right_detect==1):
                    arrmax = 105
                else: 
                    arrmax = 150
                    S_left=800
                center = int((arrmax + arrmin)/2)
                error = set_point - center
                angle = -PID(error, 0.32, 0.0002, 0.007)#0.3 fps 25 - 30
            if (S > S_left):     
                angle, speed = turn_left(float(current_speed))
                left = 1

    ################## Control speed by error
    if (straight==1):
        speed=150
    if (right==0 and left ==0):
        if (set_speed>0):
            if (float(current_speed)>54):
                speed = -10
            elif (float(current_speed)>52 and float(current_speed)<54):
                speed = -2
            elif (float(current_speed)>49 and float(current_speed)<52):
                speed = -1
            elif(float(current_speed)> set_speed):
                speed = 0
            else: speed = 150
        elif (float(current_speed)<45):
            speed=150
        else: 
            if (float(current_speed)>58):
                speed = 0
            else: speed = -10*abs((error)) + 210
    cv2.circle(edges,(arrmin,line),5,(0,0,0),2)
    cv2.circle(edges,(arrmax,line),5,(0,0,0),2)
    cv2.line(edges,(center,line),(set_point,edges.shape[0]),(0,0,0),2)
    cv2.imshow("IMG", edges)
    key = cv2.waitKey(1)
    return angle, speed, right, left, straight