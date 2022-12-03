# Import socket module
import socket
import cv2
import numpy as np
import torch
import time
import argparse
from unet import UNet
import torch.nn.functional as F
from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.torch_utils import select_device, TracedModel
from utils.plots import plot_one_box
from utils.general import check_img_size, non_max_suppression, \
    scale_coords, set_logging
from torchvision import transforms
from PIL import Image
from numpy import random
from pathlib import Path
#from model import build_unet

# Create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the port on which you want to connect
PORT = 54321
pre_t = time.time()# connect to the server on local computer
s.connect(('127.0.0.1', PORT))
angle = 0
speed = 70
line = 20
S = 0
err_arr = np.zeros(5)
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
""" Load the checkpoint """
args = get_args()
model = UNet(n_channels=3, n_classes=3, bilinear=args.bilinear)
model = model.to(device)
model.load_state_dict(torch.load(args.model, map_location=device))
"""OD"""
device_od = '0'
device_od = select_device(device_od)
print(device_od)
model_od = attempt_load('test.pt', map_location=device_od)  # load FP32 model
def detect(source, device, img_size, iou_thres, conf_thres, net):
    net.eval()
    stride = int(net.stride.max())  # model stride
    imgsz = check_img_size(img_size, s=stride)  # check img_size
    dataset = LoadImages(source, img_size=imgsz, stride=stride)
    names = net.module.names if hasattr(net, 'module') else net.names
    colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        with torch.no_grad():
            pred = net(img)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres)
        for i, det in enumerate(pred):  # detections per image
            p, s, im0 = path, '', im0s
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()
                for *xyxy, conf, cls in reversed(det):
                    label = f'{names[int(cls)]} {conf:.2f}'
                    #lay gia tri cua OD
                    label_OD = f'{names[int(cls)]}' 
                    # plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
                return float(xyxy[0]), float(xyxy[1]), float(xyxy[2]), float(xyxy[3]), float(conf), label_OD, im0
            else: return 'n' , 'o', 't', 'h', 'i', 'n', 'g'
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
if __name__ == "__main__":
    try:
        while True:
            message_getState = bytes("0", "utf-8")
            s.sendall(message_getState)
            state_date = s.recv(100)
            try:
                current_speed, current_angle = state_date.decode(
                    "utf-8"
                    ).split(' ')
                # print('current angle: ',current_angle)
            except Exception as er:
                print(er)
                pass
            #send data
            # print('angle', angle)
            message = bytes(f"1 {angle} {speed}", "utf-8")
            s.sendall(message)            
            #while amount received < amount expected
            data = s.recv(100000)
            try:
                start = time.time()
                decoded = cv2.imdecode(np.frombuffer(data, np.uint8), -1)

                img_OD = cv2.resize(decoded,(320, 160))
                image_name = "img_OD.jpg"
                cv2.imwrite(image_name, img_OD)

                image = decoded[120:,:]
                image = cv2.resize(image, (160, 80))
                image_resize = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                """DETECT OBJECT"""
                torch.cuda.is_available()
                with torch.no_grad():
                    xmin, ymin, xmax, ymax, conf_OD, name, img_detect = detect('img_OD.jpg', device, img_size=320, iou_thres=0.25, conf_thres=0.25, net=model_od)
                try:
                    S = (xmax - xmin)*(ymax - ymin)  # S>1000, nga ba arrmax = 160
                except Exception as er:
                    print(er)
                    pass
                """DETECT LANE"""
                arr = []
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

                lineRow = edges[line,:]
                for x,y in enumerate(lineRow):
                    if y==255:
                        arr.append(x)
                arrmax=max(arr)
                arrmin=min(arr)
                center = int((arrmax + arrmin)/2)
                error = int(edges.shape[1]/2) - center
                #err duong xe dang ben phai va can sang trai nen de am de nguoc lai, goc duong la dg bi sang phai
                angle = -PID(error, 0.31, 0.00, 0.005)#0.3
                if (angle > 0 and angle < 5):
                    set_speed = 56
                elif (angle > 20):
                    set_speed = 30
                else: set_speed = 45

                if (float(current_speed) < 15):
                    speed = 150
                elif (abs(float(current_angle))>8):#11
                    speed = -1
                elif (float(current_speed)>set_speed):#53
                    speed = 0
                else: speed = 150
                cv2.circle(edges,(arrmin,line),5,(0,0,0),3)
                cv2.circle(edges,(arrmax,line),5,(0,0,0),3)
                cv2.line(edges,(center,line),(int(edges.shape[1]/2),edges.shape[0]),(0,0,0),3)
                cv2.imshow("IMG", edges)
                key = cv2.waitKey(1)
                print(S, conf_OD, name)
                end = time.time()
                fps = 1 / (end - start)
                print(fps)
            except Exception as er:
                print(er)
                pass
            
    finally:
        print('closing socket')
        s.close()
