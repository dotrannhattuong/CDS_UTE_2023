import time
import cv2
def go_straight(arrmax, arrmin, left_detect, right_detect):
    if (arrmax>=118 and arrmin>40 and arrmin<50):
        center = arrmin + 35
    elif (arrmin<=43 and arrmax>110 and arrmax<120):
        center = arrmax -35 
    else: center = 1
    return center
def turn_left(current_speed, right_detect):
    if (right_detect==1):
        angle = -17 #45
        speed = 0
    else: 
        angle = -14
        speed = 0
    return angle, speed
def turn_right(current_speed, left_detect):
    if (left_detect==1):
        t_right = 0.48
    else: t_right=0.43
    speed = 0
    angle = 25
    return angle, speed, t_right
def map_right(current_speed):
    a=450 #45 45.5 
    if (float(current_speed)>46.5 and float(current_speed)<48):
        S_right = a - 6
    if (float(current_speed)>46 and float(current_speed)<46.5):
        S_right = a - 4
    if (float(current_speed)>45.5 and float(current_speed)<46):
        S_right = a - 2
    if (float(current_speed)>45 and float(current_speed)<45.5):
        S_right = a 
    if (float(current_speed)<45 and float(current_speed)>44.5):
        S_right = a + 2
    if (float(current_speed)<44.5 and float(current_speed)>44):
        S_right = a + 4
    if (float(current_speed)<44 and float(current_speed)>43.5):
        S_right = a + 6
    if (float(current_speed)<43.5 and float(current_speed)>43):
        S_right = a + 8
    return S_right
def map_left(current_speed):
    a=817# 44.5 - 45
    if (float(current_speed)<45.5 and float(current_speed)>45):
        S_left=a - 2
    if (float(current_speed)<45 and float(current_speed)>44.5):
        S_left=a 
    if (float(current_speed)<44.5 and float(current_speed)>44):
        S_left=a + 2
    if (float(current_speed)<44 and float(current_speed)>43.5):
        S_left=a + 4
    if (float(current_speed)<43.5 and float(current_speed)>43):
        S_left=a + 6
    if (float(current_speed)<43 and float(current_speed)>42.5):
        S_left=a + 8
    if (float(current_speed)<42.5 and float(current_speed)>42):
        S_left=a + 10
    return S_left
def controller(edges, PID, current_angle, current_speed, conf_OD, cls_OD, S, right, left, straight, two_lane):
    """detect duong thang"""
    S_left = 753 # 45.68
    straightarr = []
    line = 15
    set_speed = 0
    t_right = 0.47
    """MAP TURN RIGHT NGA BA THANG"""
    S_right_set = 454 # voi van toc 45
    if (float(current_speed)>46):
        S_right = S_right_set - 4
    if (float(current_speed)>45.5 and float(current_speed)<46):
        S_right = S_right_set - 2
    if (float(current_speed)>45 and float(current_speed)<45.5):
        S_right = S_right_set
    if (float(current_speed)<45 and float(current_speed)>44.5):
        S_right = S_right_set + 2
    if (float(current_speed)<44.5 and float(current_speed)>44):
        S_right = S_right_set + 4
    if (float(current_speed)<44 and float(current_speed)>43.5):
        S_right = S_right_set + 6
    if (float(current_speed)<43.5 and float(current_speed)>43):
        S_right = S_right_set + 8
    if (float(current_speed)<43 and float(current_speed)>42.5):
        S_right = S_right_set + 10
    if (float(current_speed)<42.5):
        S_right = S_right_set + 12

    if (cls_OD==0 and float(current_speed)<43.5):
        line = 18
    if (cls_OD>0 and cls_OD!=7):
        line = 20 # chieu dai duong 70
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
    lane=[]
    line_2lane = edges[15,:]
    for x,y in enumerate(line_2lane):
        if y==255:
            lane.append(x)
    lanemax=max(lane)
    lanemin=min(lane)
    arr=[]
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    arrmax=max(arr)
    arrmin=min(arr)
    set_point = int(edges.shape[1]/2) 
    # print('--------------------------------------------------------', arrmax, arrmin, line)
    # print('---------------------------------------------------+++++', lanemax, lanemin, straight_detect)
    # if ((lanemax-lanemin)>67 and (lanemax-lanemin)<82):
    #     print('==================================================== duong hai lane')
    #     if (line==18):
    #         set_point = int(edges.shape[1]/2) + 10
    #         arrmin = arrmax - 20

    #     if (line==20):
    #         set_point = int(edges.shape[1]/2) + 18
    #         arrmin = arrmax -40

    if (conf_OD==0):
        if (left_detect==1 and right_detect==0 and straight_detect==0 and arrmax >((edges.shape[1]/2) + 5)): #cua trai
            if (arrmin > 30 and float(current_speed)>50):
                arrmax = arrmax + 34
                print('change arrmax')
        elif (right_detect==1 and left_detect==0 and straight_detect==0 and arrmin < ((edges.shape[1]/2) - 5)): #cua phai
            if (arrmax < 130 and float(current_speed)>50):
                arrmin = arrmin - 34
                print('change arrmin')
    if (arrmax < 115 and arrmin > 42 and two_lane==0 and (arrmax - arrmin)<=69 and line==20):
        print('bong ram')
        arrmax = arrmin + 71
    elif (arrmax < 118 and arrmin > 45 and two_lane==0 and (arrmax - arrmin)<=69 and line==20):
        arrmin = arrmax - 71
    center = int((arrmax + arrmin)/2)
    ############################################################################### tra arrmax arrmin
    """xu li di thang thang"""
    if (conf_OD > 0.7):
        if (cls_OD==2): 
            center = go_straight(arrmax=arrmax, arrmin=arrmin, left_detect=left_detect, right_detect=right_detect)
            if (center==1):
                center = int((arrmax + arrmin)/2)
            # straight=1
    error = set_point - center
    print('error:...............', error)
    angle = -PID(error, 0.32, 0.0002, 0.007)#0.3 fps 25 - 30
    ##################################################################################
    
    if (conf_OD>0 and cls_OD!=2 and cls_OD!=7):
        set_speed=45
    """TURN RIGHT"""
    if (right==1):
        print('speed:......................................................................', float(current_speed))  
        right=0
        t1 = time.time()
        while ((time.time()-t1)<t_right):
            if ((arrmax-arrmin)>45 and (arrmax-arrmin)<57 and arrmin > 10 and arrmax < 150):
                print('breaking----------------------', arrmax-arrmin)
                #break
    if (conf_OD > 0.7):
        if (cls_OD==1):
            if (arrmax>150 and left_detect==0):
                angle = 0.9
            if (left_detect==1):
                angle = 2
                S_right = map_right(current_speed=float(current_speed))
                # arrmin = arrmax - 20
                # center = int((arrmax + arrmin)/2)
                # error = set_point - center
                # angle = -PID(error, 0.32, 0.0002, 0.007)#0.3 fps 25 - 30
            if (S > S_right):   
                angle, speed, t_right = turn_right(current_speed=float(current_speed), left_detect=left_detect)
                right = 1
    ##################################################################################
    """TURN LEFT"""
    if (left==1):
        print('speed ......................................................................:', float(current_speed))
        left = 0
        t2 = time.time()
        while ((time.time()-t2)<0.48):
            if ((arrmax-arrmin)>45 and (arrmax-arrmin)<57 and arrmin > 10 and arrmax < 150):
                print('breaking----------------------', arrmax-arrmin)
    if (conf_OD > 0.7):
        if (cls_OD==8):
            if (arrmin==0):
                if (right_detect==1):
                    angle = -1
                    print('tesst')
            else:
                angle=0.8
                S_left=map_left(current_speed=float(current_speed))
            if (S > S_left):     
                angle, speed = turn_left(current_speed=float(current_speed), right_detect=right_detect)
                left = 1
    """ NO TURN RIGHT"""
    if (conf_OD > 0.7):
        if (cls_OD==4):
            if (straight_detect==1):
                center = go_straight(arrmax=arrmax, arrmin=arrmin, left_detect=left_detect, right_detect=right_detect)
                if (center==1):
                    center = int((arrmax + arrmin)/2)
                error = set_point - center
                angle = -PID(error, 0.32, 0.0002, 0.007)#0.3 fps 25 - 30
            if (left_detect==1):
                if (arrmin==0):
                    if (right_detect==1):
                        angle = -1
                        print('tesst')
                else:
                    angle=0.8
                    S_left=map_left(current_speed=float(current_speed))
                if (S > S_left):     
                    angle, speed = turn_left(current_speed=float(current_speed), right_detect=right_detect)
                    left = 1
    """ NO STRAIGHT """
    if (conf_OD > 0.7):
        if (cls_OD==5):
            if (right_detect==1):
                if(arrmax>150 and left_detect==0):
                    angle = 0.9
                if (S > S_right):   
                    angle, speed, t_right = turn_right(current_speed=float(current_speed), left_detect=left_detect)
                    right = 1
            if (left_detect==1):
                if (arrmin==0):
                    if (right_detect==1):
                        angle = -1
                        print('tesst')
                else:
                    angle=0.8
                    S_left=map_left(current_speed=float(current_speed))
                if (S > S_left):     
                    angle, speed = turn_left(current_speed=float(current_speed), right_detect=right_detect)
                    left = 1




    ################## Control speed by error
    if (right==0 and left==0 and straight==0):
        if (set_speed>0):
            if (float(current_speed)>54):
                speed = -15
            elif (float(current_speed)>52 and float(current_speed)<54):
                speed = -5
            elif (float(current_speed)>49 and float(current_speed)<52):
                speed = -1
            elif(float(current_speed)> set_speed):
                speed = 0
            else: speed = 150
        elif (float(current_speed)<45):
            speed=150
        else: 
            if (float(current_speed)>59):
                speed = 0
            else: speed = -10*abs((error)) + 210
    cv2.circle(edges,(arrmin,line),5,(0,0,0),2)
    cv2.circle(edges,(arrmax,line),5,(0,0,0),2)
    cv2.line(edges,(center,line),(set_point,edges.shape[0]),(0,0,0),2)
    cv2.imshow("IMG", edges)
    key = cv2.waitKey(1)
    return angle, speed, right, left, straight, two_lane