import time
import cv2
import numpy as np
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
def controller(edges, PID, current_angle, current_speed, conf_OD, cls_OD, S, right, left, straight, two_lane, PID_speed, check_err):
    """lachs"""
    corner = 0
    two_lane_turn = 0
    """detect duong thang"""
    straightarr = []
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
    """Detect Lane"""
    line = 15
    if (cls_OD==0 and float(current_speed)<43.5):
        line = 18
    if (cls_OD>0 and cls_OD!=7):
        line = 20
    arr=[]
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    if not arr:
        if (float(current_angle)>0):
            angle_er = 25
        else: angle_er = -25
        return angle_er, 70
    arrmax=max(arr)
    arrmin=min(arr)
    arrmax_turn=max(arr)
    arrmin_turn=min(arr)
    set_point = int(edges.shape[1]/2) 
    """2 lane"""
    lane=[]
    linelane = edges[22,:]
    for x,y in enumerate(linelane):
        if y==255:
            lane.append(x)
    arrmax_lane=max(lane)
    arrmin_lane=min(lane)
    lane_check=[]
    linelane_check = edges[39,:]
    for x,y in enumerate(linelane_check):
        if y==255:
            lane_check.append(x)
    arrmax_lane_check=max(lane_check)
    arrmin_lane_check=min(lane_check)
    """-----------------------------------------"""
    set_point = int(edges.shape[1]/2) 

    # print(arrmax - arrmin, line, arrmax, arrmin)
    print((arrmax_lane - arrmin_lane), arrmax_lane, arrmin_lane)
    print(arrmax_lane_check, arrmin_lane_check)

    if (conf_OD==0):
        if (left_detect==1 and right_detect==0 and straight_detect==0 and arrmax >((edges.shape[1]/2) + 15)): #cua trai
            if (arrmin > 30 and float(current_speed)>47):
                arrmax = arrmax + 32
                corner = 1
        elif (right_detect==1 and left_detect==0 and straight_detect==0 and arrmin < ((edges.shape[1]/2) - 15)): #cua phai
            if (arrmax < 130 and float(current_speed)>47):
                arrmin = arrmin - 32
                corner = 1
    #################################################################################
    if (arrmax < 110 and arrmin > 43 and arrmin < 53 and line==20):
        print('bong ram')
        arrmax = arrmin + 62
    elif (arrmax < 114 and arrmax > 104 and arrmin > 49 and line==20):
        arrmin = arrmax - 62
        print('bong ram')
    #####################################################################
    """DUONG HAI LANE"""
    if ((arrmax_lane-arrmin_lane)>90 and arrmin_lane_check==0 and arrmax_lane<130 and arrmax_lane>100):
        print('............................................................................/.duong hai lane', two_lane)
        two_lane=two_lane+1
        if (two_lane>6):
            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++xac nhan hai lane')
            set_point = int(edges.shape[1]/2) + 10
            arrmin = arrmax - 20
            two_lane_turn = 1
    else: two_lane=0

    ##############
    center = int((arrmax + arrmin)/2)
    error = set_point - center
    if (corner==1):
        angle = -PID(error, 0.32, 0.000, 0.007)#0.377 0 0.075 khi cv2 
    else: angle = -PID(error, 0.35, 0.000, 0.065)#0.377 0 0.075 khi cv2 
    ##############
    set_speed=0
    if (conf_OD>0 and cls_OD!=7):
        set_speed=45
    #####################################################################
    if (straight==1):
        print('speed:......................................................................', float(current_speed))  
        straight=0
        t3 = time.time()
        while ((time.time()-t3)<0.25):
            if (center<110 and center>50):
                print('breaking----------------------', arrmax-arrmin)
                break
    """Straight"""
    if (conf_OD > 0.8):
        if (cls_OD==2 and S>1000): 
            print('speed:....................................................................STRAIGHT..') 
            if (float(current_angle)>2):
                angle = 0.5
            elif (float(current_angle)<-2):
                angle = -0.5
            else: angle = 0
            straight=1
    """TURN RIGHT"""
    if (right==1):
        print('speed:......................................................................', float(current_speed))  
        right=0
        t1 = time.time()
        while ((time.time()-t1)<0.48):
            if ((arrmax-arrmin)>45 and (arrmax-arrmin)<57 and arrmin > 10 and arrmax < 150):
                print('breaking----------------------', arrmax-arrmin)
                #break
    if (conf_OD > 0.8):
        if (cls_OD==1):
            angle = -0.15
            if (left_detect==1):
                angle = 0.9
            if (arrmax_turn>125):   
                angle = 25
                speed = 0
                right = 1
    """TURN LEFT"""
    if (left==1):
        print('speed ..left....................................................................:', float(current_speed))
        left = 0
        t2 = time.time()
        while ((time.time()-t2)<0.57):
            if ((arrmax-arrmin)>45 and (arrmax-arrmin)<57 and arrmin > 10 and arrmax < 150):
                print('breaking----------------------', arrmax-arrmin)
    if (conf_OD > 0.8):
        if (cls_OD==8):
            if (right_detect==0):
                angle = 0.6
            if (arrmin_turn<30 and two_lane_turn==0):  
                if (right_detect==0):
                    angle = -13
                else: angle = -12.2
                speed = 0
                left = 1
    """ NO TURN RIGHT"""
    if (conf_OD > 0.8):
        if (cls_OD==4):
            if (straight_detect==1):
                print('speed:....................................................................STRAIGHT..') 
                angle = 0
                straight=1
            if (left_detect==1):
                if (right_detect==0):
                    angle = 0.6
                if (arrmin_turn<30 and two_lane_turn==0):  
                    if (right_detect==0):
                        angle = -13
                    else: angle = -12.5
                    speed = 0
                    left = 1
    """ NO STRAIGHT """
    if (conf_OD > 0.8):
        if (cls_OD==5):
            if (right_detect==1):
                angle = -0.15
                if (left_detect==1):
                    angle = 0.9
                if (arrmax_turn>125):   
                    angle = 25
                    speed = 0
                    right = 1
            if (left_detect==1):
                if (right_detect==0):
                    angle = 0.6
                if (arrmin_turn<30 and two_lane_turn==0):  
                    if (right_detect==0):
                        angle = -13
                    else: angle = -12.5
                    speed = 0
                    left = 1
    ############################################################################### tra arrmax arrmin
    ######## fix PID tosc do
    if (straight==1):
        speed = 80
    if (right==0 and left==0 and straight==0):
        if (set_speed>0 and float(current_speed)>set_speed):
            er = float(current_speed) - set_speed 
            speed = -er*1.5
        elif (float(current_speed)<45): #53
                speed=140
        else: 
            if (float(current_speed)>58):
                speed=0
            else: 
                speed = -10*abs(error)+150
    # cv2.circle(edges,(arrmin,line),5,(0,0,0),2)
    # cv2.circle(edges,(arrmax,line),5,(0,0,0),2)
    # cv2.line(edges,(center,line),(set_point,edges.shape[0]),(0,0,0),2)
    # cv2.circle(edges,(arrmin_lane,22),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax_lane,22),5,(0,0,0),3)
    # cv2.circle(edges,(arrmin_lane_check,35),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax_lane_check,35),5,(0,0,0),3)
    # # cv2.line(edges,(center,linelane),(arrmax_lane,linelane),(0,0,0),2)
    # cv2.imshow("IMG", edges)
    key = cv2.waitKey(1)
    return angle, speed, right, left, straight, two_lane, check_err