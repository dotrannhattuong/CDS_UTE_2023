# Import socket module
import socket
import cv2
import numpy as np
import time
import math

global sendBack_angle, sendBack_Speed, current_speed, current_angle
sendBack_angle = 0
sendBack_Speed = 0
current_speed = 0
current_angle = 0

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
PORT = 54321
# connect to the server on local computer
s.connect(('127.0.0.1', PORT))

 
count = 0
count1 = 0

def Control(angle, speed):
    global sendBack_angle, sendBack_Speed
    sendBack_angle = angle
    sendBack_Speed = speed
 
if __name__ == "__main__":
    try:
        while True:

            """
            - Chương trình đưa cho bạn 1 giá trị đầu vào:
                * image: hình ảnh trả về từ xe
                * current_speed: vận tốc hiện tại của xe
                * current_angle: góc bẻ lái hiện tại của xe
            - Bạn phải dựa vào giá trị đầu vào này để tính toán và
            gán lại góc lái và tốc độ xe vào 2 biến:
                * Biến điều khiển: sendBack_angle, sendBack_Speed
                Trong đó:
                    + sendBack_angle (góc điều khiển): [-25, 25]
                        NOTE: ( âm là góc trái, dương là góc phải)
                    + sendBack_Speed (tốc độ điều khiển): [-150, 150]
                        NOTE: (âm là lùi, dương là tiến)
            """

            message_getState = bytes("0", "utf-8")
            s.sendall(message_getState)
            state_date = s.recv(100)

            try:
                current_speed, current_angle = state_date.decode(
                    "utf-8"
                    ).split(' ')
            except Exception as er:
                print(er)
                pass

            message = bytes(f"1 {sendBack_angle} {sendBack_Speed}", "utf-8")
            s.sendall(message)
            data = s.recv(100000)

            try:
                image = cv2.imdecode(
                    np.frombuffer(
                        data,
                        np.uint8
                        ), -1
                    )

                # print(current_speed, current_angle)
                # print(image.shape)
                # your process here
                # -------------------------------------------Workspace---------------------------------- #
                #Show image head car
                cv2.imshow('image', image)
                cv2.waitKey(1)
            
                #code lấy data             #    "G:\Knowledge_AI\Code UTE RACING CAR\data"
                seconds = time.time() 
                #path save img 
                image_name = "/home/hiu/Desktop/Data/image/image_no_straight_{}.jpg".format(count)
                count1 += 1                     # bien dem time 
                begin_get = 200                # bien tao do tre de lay data
                imgs = 100                      # so luong anh muon lay 
                frame_num = 10                  # khung hinh/s muon luu
                end_get = begin_get + frame_num*imgs + 1   
                if count1 % frame_num == 0 and begin_get < count1 < end_get :
                    count += 1
                    cv2.imwrite(image_name, image )
                    print("save success", "count = ", count, "cout1 = " , count1)
                    
                elif count1 > end_get: print ("unsave")


                Control(sendBack_angle, sendBack_Speed)


            except Exception as er:
                print(er)
                pass

    finally:
        print('closing socket')
        s.close()
