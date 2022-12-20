import cv2
def Controller(edges, PID, current_speed, current_angle, error):
    line = 17
    # if (float(current_speed)<42):
    #     line = 17
    # print('-----------------------------------', line)
    # print('-----------------------------------', error)
    arr = []
    lineRow = edges[line,:]
    for x,y in enumerate(lineRow):
        if y==255:
            arr.append(x)
    arrmax=max(arr)
    arrmin=min(arr)
    center = int((arrmax + arrmin)/2)
    error = int(edges.shape[1]/2) - center
    #err duong xe dang ben phai va can sang trai nen de am de nguoc lai, goc duong la dg bi sang phai
    angle = -PID(error, 0.335, 0.000, 0.065)#0.377 0 0.075 khi cv2
    if (float(current_speed)<52.3): #53
            speed=140
    else: 
        if (float(current_speed)>60):
            speed=0
        else: 
            speed = -15*abs(error)+150
            # speed = -20*abs(error)+183 #17 200

        # set_speed = -1.5*abs((error)) + 60
        # if (float(current_speed)>set_speed):
        #     if ((set_speed - float(current_speed))>5):
        #         speed = -10
        #     elif ((set_speed - float(current_speed))>2.5):
        #         speed = -5
        #     else: speed = 0
        # else: speed = 150
    # cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
    # cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
    # cv2.imshow("IMG", edges)
    # key = cv2.waitKey(1)
    return angle, speed, error