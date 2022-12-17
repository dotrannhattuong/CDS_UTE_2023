import cv2
def Controller(edges, PID, current_speed, current_angle):
    line = 28
    if (float(current_speed)<54):
        line = 32
    print('-----------------------------------', line)
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
    angle = -PID(error, 0.31, 0.0001, 0.006)#0.3
    if (float(current_speed)<45):
            speed=150
    else: 
        if (float(current_speed)>60):
            speed = 0
        else: speed = -10*abs((error)) + 230
    cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
    cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
    cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
    cv2.imshow("IMG", edges)
    key = cv2.waitKey(1)
    return angle, speed