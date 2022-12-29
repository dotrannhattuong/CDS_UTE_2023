import cv2
def Controller(edges, PID, current_speed, current_angle):
    line = 32
    arr = []
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)

    if not arr:
        return 25, 0

    arrmax=max(arr)
    arrmin=min(arr)
    center = int((arrmax + arrmin)/2)
    if ((arrmax - arrmin)<60 and arrmin<60 and arrmax<110): #88 34
        center = arrmin - 30
    if ((arrmax - arrmin)<60 and arrmax>110 and arrmax>110):
        center = arrmax + 30
   
    
    
    error = int(edges.shape[1]/2) - center
    # print(error)
    #err duong xe dang ben phai va can sang trai nen de am de nguoc lai, goc duong la dg bi sang phai
    angle = -PID(error, 0.34, 0.000, 0.065)#0.3
    if (abs(error)<18):
        set_speed = 51
    else: set_speed = 47
    # set_speed = 51
    if (float(current_speed)<set_speed):
        speed=150
    else: 
        if (float(current_speed)>60):
            speed = 0
        else: speed = -5.7*abs((error)) + 150
    # cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
    # cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
    # cv2.imshow("IMG", edges)
    # key = cv2.waitKey(1)
    return angle, speed