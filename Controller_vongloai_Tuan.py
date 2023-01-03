import cv2
import time
def Controller(edges, PID, current_speed, current_angle, check_err):
    line = 26
    arr = []
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    if not arr:
        return float(current_angle), 100
    arrmax=max(arr)
    arrmin=min(arr)
    print(arrmax, arrmin)

    if (check_err==1):
        t = time.time()
        while((time.time()-t)<0.13):
            angle = 25
            print('++++++++++++++++++++++++++++++++++++++')
        check_err=0

    if (check_err==2):
        t = time.time()
        while((time.time()-t)<0.13):
            angle = -25
            print('-------------------------------------------')
        check_err=0
    
    if (arrmax>150 and arrmin>125):
        angle = 25
        check_err=1
        print('1111111111111111111111111111111')
    if (arrmax<35 and arrmin<10):
        angle = -25
        check_err=2
        print('2222222222222222222222222222222')

    center = int((arrmax + arrmin)/2)
    # print(arrmax, arrmin)
    # if ((arrmax - arrmin)<60 and arrmin<60 and arrmax<110): #88 34
    #     center = arrmin - 20
    # if ((arrmax - arrmin)<60 and arrmax>110 and arrmax>110):
    #     center = arrmax + 20
    
    error = int(edges.shape[1]/2) - center
    # print(error)
    #err duong xe dang ben phai va can sang trai nen de am de nguoc lai, goc duong la dg bi sang phai
    if (check_err==0):
        angle = -PID(error, 0.35, 0.000, 0.065)#0.3
        set_speed = 65 - abs(error)/5
        # set_speed = 51
        if (float(current_speed)<set_speed):
            speed=150
        else: 
            if (float(current_speed)>65):
                speed = 0
            else: speed = -5*abs((error)) + 150
    else: speed = 80
    # cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
    # cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
    # cv2.imshow("IMG", edges)
    # key = cv2.waitKey(1)
    return angle, speed, check_err