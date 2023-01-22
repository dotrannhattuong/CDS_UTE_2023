import cv2
import time
def Controller(edges, PID, current_speed, current_angle, check_err, xmax, xmin, conf, cls, right, left, straight, S, notleft, notright):
    angle_check=0
    rightmin=0
    leftmin=0
    od = (xmax + xmin)/2
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
    lineLeft = edges[:,9]
    for x,y in enumerate(lineLeft):
        if y==255:
            leftarr.append(x)
    try:
        leftmin=min(leftarr)
        if (leftmin>25):
            left_detect = 0
        else: left_detect = 1
        # print('left', left_detect)
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
        # print('right', right_detect)
    except Exception as er:
        right_detect = 5
        pass
    """DETECT LANE"""
    line = 30
    arr = []
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    if not arr:
        print('000000000000000000000000000000000000000000')
        line_check = 45
        arr_check = []
        lineRow_check = edges[line_check,:]
        for x,y in enumerate(lineRow_check):
            if y==255:
                arr_check.append(x)
        arrmax=max(arr_check)
        arrmin=min(arr_check)
        center = int((arrmax + arrmin)/2)  
        error = int(edges.shape[1]/2) - center
        angle_check = -PID(error, 0.35, 0.000, 0.065)#0.3
        # if (float(current_angle)>0):
        #     angle_check = float(current_angle)+2
        # if (float(current_angle)<0):
        #     angle_check = float(current_angle)-2
        # if (right>1):
        #     angle_check = 25
        #     print('angle==========================25')
        return angle_check, 80, check_err, right, left, straight, notleft, notright
    arrmax=max(arr)
    arrmin=min(arr)
    arrmax_turn=max(arr)
    arrmin_turn=min(arr)
    # line_turn = 40
    # arr_turn = []
    # lineTurn = edges[line_turn,:]
    # for x,y in enumerate(lineTurn):
    #     if y==255:
    #         arr_turn.append(x)
    # arrmax_turn=max(arr_turn)
    # arrmin_turn=min(arr_turn)
    # print(arrmax, arrmin, xmax, xmin, arrmax_turn, arrmin_turn)
    """ CAR """
    if (conf>0.7):
        if (cls==6 and S>7000):
            print('---------------------------------------------------------------', float(current_speed))
            if (od<320):
                arrmin = 72
            else: 
                arrmax = 88

    # if (check_err==1):
    #     t = time.time()
    #     while((time.time()-t)<0.135):
    #         angle = 25
    #         print('++++++++++++++++++++++++++++++++++++++')
    #     check_err=0

    # if (check_err==2):
    #     t = time.time()
    #     while((time.time()-t)<0.135):
    #         angle = -25
    #         print('-------------------------------------------')
    #     check_err=0
    
    # if (arrmax>150 and arrmin>120):
    #     angle = 25
    #     check_err=1
    #     print('1111111111111111111111111111111')
    # if (arrmax<30 and arrmin<10):
    #     angle = -25
    #     check_err=2
    #     print('2222222222222222222222222222222')

    center = int((arrmax + arrmin)/2)  
    error = int(edges.shape[1]/2) - center
    # print(error)
    angle = -PID(error, 0.35, 0.000, 0.065)#0.3
    if (angle>14 and left==0 and right==0 and conf==0 and float(current_speed)>60):
        angle=25
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ +25')
    if(angle<-14 and left==0 and right==0 and conf==0 and float(current_speed)>60):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ -25')
        angle=-25
    if (cls==6 and S>2500 and conf>0.8):
        set_speed_OD = 70
    elif (conf>0.6 and cls!=7 and S>2800):
        set_speed_OD=69
    elif (right==1 or left==1):
        set_speed_OD = 69
    # elif (notleft==1 or notright==1):
    #     set_speed_OD=70
    else: set_speed_OD=0
    """TIME DELAY TURN RIGHT"""
    # CUA 0.7S
    if (right==3):
        print('speed:......................................................................', float(current_speed))  
        right=0
        t1 = time.time()
        while ((time.time()-t1)<1.1):
            None
    # DI THANG 0.1s
    if (right==2):
        print('speed:......................................................................', float(current_speed))  
        right=3
        t1 = time.time()
        # tdelay_right=0.01
        # if(float(current_speed)<65):
        #     tdelay_right=0.368-0.005*(float(current_speed)) 
        tdelay_right=0.36-0.005*(float(current_speed)) + 0.0007*(70-int(current_speed))*(70-float(current_speed))
        while ((time.time()-t1)<tdelay_right):
            None
        angle = 25
        speed = 140
    """TIME DELAY TURN LEFT"""
    # CUA 0.7S
    if (left==3):
        print('speed:..................................................left....................', float(current_speed))  
        left=0
        t2 = time.time()
        while ((time.time()-t2)<1.1):
            None
    # DI THANG 0.1s
    if (left==2):
        print('speed:.....................................................left.................', float(current_speed))  
        left=3
        t2 = time.time()
        # tdelay_left=0.01
        # if (float(current_speed)<65): #-0.021x+1.437
        #     tdelay_left=0.368-0.005*(float(current_speed))
        # else: tdelay_left=0.36-0.005*(float(current_speed))
        tdelay_left=0.36-0.005*(float(current_speed)) + 0.0007*(70-int(current_speed))*(70-int(current_speed))
        while ((time.time()-t2)<tdelay_left):
            None
        angle = -25
        speed = 140
    """TIME DELAY STRAIGHT"""
    if (straight==2):
        straight=0
        print('speed:.....................................................straight.................', float(current_speed))  
        t3 = time.time()
        while ((time.time()-t3)<0.8):
            None
    ############################################################################################################################################
    """STRAIGHT"""
    if (conf > 0.8 and S>2800): # can sua lai
        if (cls==2):
            straight=1
    if (straight==1 and S>4000):
        angle = 0
        speed = 150
        straight=2
    """TURN RIGHT"""
    if (conf > 0.8 and S>2800): # can sua lai
        if (cls==1):
            right=1
    if (right==1):  
        if (arrmax_turn>152):
            angle = 0
            speed = 150
            right = 2
            notleft=0
        # elif (left_detect==0 and arrmax>150):
        #     print('left________________________________________________________________________________________________detect')
        #     arrmin=5
        #     center = int((arrmax + arrmin)/2)  
        #     error = int(edges.shape[1]/2) - center
        #     angle = -PID(error, 0.35, 0.000, 0.065)#0.3
    """TURN LEFT"""
    if (conf > 0.8 and S>2800): # can sua lai
        if (cls==8):
            left=1
    if (left==1): 
        if (arrmin_turn<8):
            angle = 0
            speed = 150
            left = 2 
            notright=0
        # elif (right_detect==0 and arrmin<10):
        #     print('right_________________________________________________________________________________________________detect')
        #     arrmax=155
        #     center = int((arrmax + arrmin)/2)  
        #     error = int(edges.shape[1]/2) - center
        #     angle = -PID(error, 0.35, 0.000, 0.065)#0.3
    """NO TURN RIGHT"""
    if (conf > 0.8 and S>2800): # can sua lai
        if (cls==4):
            notright=1
    if (notright==1):
        if (left_detect==1):
            left=1
        elif (straight_detect==1):
            straight=1
    """NO TURN LEFT"""
    if (conf > 0.8 and S>2800): # can sua lai
        if (cls==3):
            notleft=1
    if (notleft==1):
        if (right_detect==1):
            right=1
        elif (straight_detect==1):
            straight=1
    #err duong xe dang ben phai va can sang trai nen de am de nguoc lai, goc duong la dg bi sang phai
    if (right<2 and left<2 and straight<2):
        if (set_speed_OD>0):
            if (set_speed_OD>0):
                set_speed =  set_speed_OD
            if (set_speed>0 and float(current_speed)>set_speed):
                er = float(current_speed) - set_speed 
                speed = -er
            else: speed = 150
        else:
            if (abs(angle)<2):
                set_speed=75
            else: set_speed = 68 - abs(error)/6
            if (float(current_speed)<set_speed):
                speed=150
            else: 
                if (float(current_speed)>72):
                    speed = 0
                else: speed = -2.3*abs((error)) + 150
    # cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
    # # cv2.circle(edges,(arrmin_turn,line_turn),5,(0,0,0),3)
    # # cv2.circle(edges,(arrmax_turn,line_turn),5,(0,0,0),3)
    # # cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
    # cv2.imshow("IMG", edges)
    # key = cv2.waitKey(1)
    return angle, speed, check_err, right, left, straight, notleft, notright
    
    
