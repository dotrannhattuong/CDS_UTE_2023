## Downloads Dataset

[Traffic Sign](https://github.com/dotrannhattuong/Dataset_OD_SelfDrivingCar).

[Segmentation](https://github.com/dotrannhattuong/Dataset_Lane_Segmentation).

---
## Format Data YOLO

```
Dataset_OD_SelfDrivingCar/
│
├── train/ 
│   ├── images/
│       └── 000000.png - Tất cả các images 
│   ├── labels/
│       └── 000000.txt - Tất cả các labels
│
├── val/ 
│   ├── images/
│       └── 000000.png - Tất cả các images 
│   ├── labels/
│       └── 000000.txt - Tất cả các labels
│
├── test/ 
│   ├── images/
│       └── 000000.jpg - Tất cả các images 
│   ├── labels/
│       └── 000000.txt - Tất cả các labels
```
---
## Format Data UNET

```
Dataset_Lane_Segmentation
│
├── train/ 
│   ├── images/
│       └── 000000.png - Tất cả các images 
│├── trainanot/ 
│   ├── images/
│       └── 000000.png - Tất cả các labels 
├── val/ 
│   ├── images/
│       └── 000000.png - Tất cả các images 
├── valanot/ 
│   ├── images/
│       └── 000000.png - Tất cả các labels 
```
---
## Model

| Model   |      Code      |  Reference |
|----------|:-------------:|:---------:|
|  YOLOV7  |  [Yolov7.ipynb](https://github.com/anminhhung/pytorch_tutorial/blob/master/CNN/LeNet_5.ipynb)  |  [Yolov7.ipynb](https://github.com/thangnch/MiAI_YOLOv7/blob/main/YOLOv7_Miai_vn.ipynb)  |
|  YOLOV7E6  |  [Yolov7-e6.ipynb](https://github.com/anminhhung/pytorch_tutorial/blob/master/CNN/LeNet_5.ipynb)  |  [Yolov7-e6.ipynb](https://github.com/WongKinYiu/yolov7)  |
|  UNET |  [Unet.ipynb](https://github.com/anminhhung/pytorch_tutorial/blob/master/CNN/AlexNet.ipynb)  |  [Unet.ipynb](https://github.com/milesial/Pytorch-UNet)  |

---