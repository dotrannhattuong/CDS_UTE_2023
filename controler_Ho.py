import numpy as np
import time

error_arr = np.zeros(5)
pre_t = time.time()


def Calc_error(image):
    arr=[]
    height = 25
    lineRow = image[height,:]
    for x, y in enumerate(lineRow):
        if y == 1:
            arr.append(x)
    
    center = int( (min(arr) + max(arr))/2 )
    error = int(image.shape[1]/2) - center
    return error


def Calc_speed(current_speed, set_speed, max_speed):
    speed = set_speed
    if float(current_speed) < 15.0:
        speed = set_speed
    elif float(current_speed) > max_speed:
        speed = -5
    return speed 


def PID(error, p, i, d):
    global pre_t
    global error_arr
    error_arr[1:] = error_arr[0:-1]
    error_arr[0] = error
    P = error*p
    delta_t = time.time() - pre_t
    pre_t = time.time()
    D = (error-error_arr[1])/delta_t*d
    I = np.sum(error_arr)*delta_t*i
    angle = P + I + D
    if abs(angle)>25:
        angle = np.sign(angle)*25
    return int(angle)


