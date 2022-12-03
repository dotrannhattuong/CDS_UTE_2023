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
Dataset_Lane_Segmentation/
│
├── train/ 
│       └── 000000.png - Tất cả các images 
├── trainanot/ 
│       └── 000000.png - Tất cả các lables  
├── val/ 
│       └── 000000.png - Tất cả các images 
├── valanot/ 
│       └── 000000.png - Tất cả các labels 
```
---
## Model

| Model   |      Code      |  Reference |
|----------|:-------------:|:---------:|
|  YOLOV7  |  [Yolov7.ipynb](https://github.com/dotrannhattuong/CDS_UTE_2023/blob/main/notebook/OD_yolov7.ipynb)  |  [Yolov7](https://github.com/thangnch/MiAI_YOLOv7/blob/main/YOLOv7_Miai_vn.ipynb)  |
|  YOLOV7E6  |  [Yolov7-e6.ipynb](https://github.com/dotrannhattuong/CDS_UTE_2023/blob/main/notebook/OD_yolov7e6.ipynb)  |  [Yolov7-e6](https://github.com/WongKinYiu/yolov7)  |
|  UNET |  [Unet.ipynb](https://github.com/dotrannhattuong/CDS_UTE_2023/blob/main/notebook/Lane_Segmentation.ipynb)  |  [Unet](https://github.com/milesial/Pytorch-UNet)  |

---