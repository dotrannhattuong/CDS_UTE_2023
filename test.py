import cv2
def Controller(edges, PID, current_speed, current_angle):
    line =34 # doi 33 -> 34
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
    angle = -PID(error, 0.34, 0.000, 0.065)#0.33 -> 0.34
    if (float(current_speed)<46): #45 -> 46
            speed=140 # 150 -> 140
    else: 
        if (float(current_speed)>50):
            speed = 0
        else: speed = -10*abs((error)) + 150
    # cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
    # cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
    # cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
    # cv2.imshow("IMG", edges)
    # key = cv2.waitKey(1)
    return angle, speed