
# Import socket module
import socket
import cv2
import numpy as np
import torch
import time
import socket       
import sys      
import cv2
import numpy as np
import json 
import base64
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
import argparse
from unet import UNet
from Controller_UIT_Tuan import Controller


pre_t = time.time()
current_speed = 0
current_angle = 0
def get_args():
    parser = argparse.ArgumentParser(description='Predict masks from input images')
    parser.add_argument('--model', '-m', default='checkpoint_epoch300.pth', metavar='FILE',
                        help='Specify the file in which the model is stored')
    parser.add_argument('--mask-threshold', '-t', type=float, default=0.5,
                        help='Minimum probability value to consider a mask pixel white')
    parser.add_argument('--scale', '-s', type=float, default=1.0,
                        help='Scale factor for the input images')
    parser.add_argument('--bilinear', action='store_true', default=False, help='Use bilinear upsampling')
    return parser.parse_args()
def predict_img(net,
                full_img,
                device,
                scale_factor=0.5,
                out_threshold=0.5):
    net.eval()
    img = torch.from_numpy(full_img)
    img = img.transpose(1, 2).transpose(0, 1)
    img = img / 255.0
    img = img.unsqueeze(0).float()
    img = img.to(device=device, dtype=torch.float32)
    with torch.no_grad():
        output = net(img)
        probs = F.softmax(output, dim=1)[0]
        tf = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((80, 160)),
            transforms.ToTensor()
        ])
        full_mask = tf(probs.cpu()).squeeze()
    return F.one_hot(full_mask.argmax(dim=0), net.n_classes).permute(2, 0, 1).numpy()

def mask_to_image(mask: np.ndarray):
    return Image.fromarray((np.argmax(mask, axis=0) * 255).astype(np.uint8))
device = 'cuda'
torch.cuda.is_available()
""" Load the checkpoint """
args = get_args()
model = UNet(n_channels=3, n_classes=3, bilinear=args.bilinear)
model = model.to(device)
model.load_state_dict(torch.load(args.model, map_location=device))
sendBack_angle = 0
sendBack_speed = 0

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
PORT = 54321
# connect to the server on local computer
s.connect(('127.0.0.1', PORT))
def PID(err, Kp, Ki, Kd):
    global pre_t
    err_arr[1:] = err_arr[0:-1]
    err_arr[0] = err
    delta_t = time.time() - pre_t
    pre_t = time.time()
    P = Kp*err
    D = Kd*(err - err_arr[1])/delta_t
    I = Ki*np.sum(err_arr)*delta_t
    angle = P + I + D
    return int(angle)
def remove_small_contours(image):
    image_binary = np.zeros((image.shape[0], image.shape[1]), np.uint8)
    contours = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    mask = cv2.drawContours(image_binary, [max(contours, key=cv2.contourArea)], -1, (255, 255, 255), -1)
    image_remove = cv2.bitwise_and(image, image, mask=mask)
    return image_remove
angle = 10
speed = 100
error=0
err_arr = np.zeros(5)
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

            message = bytes(f"1 {angle} {speed}", "utf-8")
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
                start = time.time()
                image_crop = image[125:, :]
                image_resize = cv2.resize(image_crop, (160, 80))
                image_resize = cv2.cvtColor(image_resize, cv2.COLOR_RGB2BGR)

                """DETECT LANE"""
                mask = predict_img(net=model,
                           full_img=image_resize,
                           device=device,
                           scale_factor=args.scale,
                           out_threshold=args.mask_threshold,
                           )
                result = mask_to_image(mask)
                out = np.array(result)
                img_remove = remove_small_contours(out)
                edges = img_remove 
                '''Controller'''
                angle, speed, error = Controller(edges=edges, PID=PID, current_speed=current_speed, current_angle=current_angle, error=error)
                # end = time.time()
                # # fps = 1 / (end - start)
                # # print(fps)
                # cv2.imshow("IMG",image_resize)
                # key = cv2.waitKey(1)

            except Exception as er:
                print(er)
                speed = -25
                pass

    finally:
        print('closing socket')
        s.close()
