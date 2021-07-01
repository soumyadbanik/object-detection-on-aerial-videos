# object detection on stanford-drone-dataset
This repo contains the codes and steps to perform object detection on stanford drone dataset in DarkNet YOLO-V4 framework. Below you can see the visualization of detected objects with their accuracies.
### Demo 
Inferencing on scene `deathCircle` of Stanford Drone Dataset:(Trained on very small data. So low accuracy). Let's start to get some cool detections like this! 

![output](https://github.com/soumyadbanik/object-detection-on-aerial-images/blob/main/results/output2.gif)

Wait! Wait! There are lot more boring stuffs to do bedore diving into the deep learning. Since this is a video dataset, the major task is to preprocess and clean the data. There is no point to train with the whole dataset. First of all, you need to choose some of the videos according to your purpose of detection. *But how you would choose them??* 80-90% of the dataset is occupied by pedestrians and bikers. So, if you want to detect only cars, obviously random selection of videos will not work. I've made it easy for you.
(If you want to skip this part, download the prepared dataset from my [Drive](https://drive.google.com/drive/folders/1fxhziv-1ZB5mPqS2aNDAfdJdPCxVL1T-?usp=sharing))

### Preparing the Dataset

1. Download the dataset from [here](https://cvgl.stanford.edu/projects/uav_data/)
2. Modify the directoy format into this format from which ever format you got. This will make the process easier. ![fileformat](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/Screenshot%20from%202021-06-30%2020-22-04.png)
3. Put the `get_stats.py` into the parent directory i.e the dataset directory. This will give you the whole summery into each directory for each video in a Bar chart format. Like this 

  |<img src="https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/vid_data.png" width="400" height="250">| 
  |---|

This will also help you to overcome the class imbalances in your final dataset.

4. Select the videos according to your detection task and put into another directory.
5. Then rename the videos and labels into this format.

|![img1](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/Screenshot%20from%202021-06-30%2021-05-32.png) | ![img2](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/Screenshot%20from%202021-06-30%2021-06-21.png) |
|---|---|
 
 This is going to help you in your remaining tasks.
 
6. Put `get_train.py`, `get_test.py`, `get_valid.py` and run them by
    `python3 get_train.py` and similarly remianing two.
7. This will split each video into frames and store each 30th, 89th and 91st frame for train, test & validation respectively (taking 1 frame per second) And also generate corresponding `.csv` files. Make sure your system have `ffmpeg` installed otherwise do 
 `sudo apt update` then `sudo apt install ffmpeg`
8. . It will convert the labels to YOLO format also. YOLO needs the labels in the format `<class_id x_center_norm y_center_norm width height>` where `x_center_norm = x_center/width, y_center_norm = y_center/height` . For example for image.jpg, the image.txt will contain 
```csv
1 0.8778 0.0143 0.04311 0.0287
2 0.8040 0.0236 0.06959 0.0435
2 0.0083 0.1345 0.01664 0.0379
```
  Now you are good to go. 

### Training

1. Clone the repository `git clone https://github.com/AlexeyAB/darknet.git`

For training on Stanford Drone Data, follow the step 1 from [AlexeyAB's Repo](https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects)
If you are training on local gpu, make sure you have `cuda` and `cuDNN` with compatible version installed in your system.

2. Create file `obj.names` in the directory `darknet/data/`, with objects names - each in new line
```csv
  pedestrian
  biker
  skater
  car
  cart
  bus
  ```
3. Create file `obj.data` in the directory `darknet/data/`, containing (where **classes = number of objects**):

  ```ini
  classes = 6
  train  = data/train.txt
  valid  = data/test.txt
  names = data/obj.names
  backup = backup/
  ```

4. Put image-files (.jpg) of your objects in the directory `darknet/data/obj/`
5. Create file `train.txt` in directory `darknet/data/`, with filenames of your images, each filename in new line, for example containing:

  ```csv
  data/obj/img1.jpg
  data/obj/img2.jpg
  data/obj/img3.jpg
  ```

7. Download pre-trained weights for the convolutional layers and put to the directory `build\darknet\x64`
    - for `yolov4.cfg`, `yolov4-custom.cfg` (162 MB): [yolov4.conv.137](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137) (Google drive mirror [yolov4.conv.137](https://drive.google.com/open?id=1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp) )
    
8. Start training by using the command line: `./darknet detector train data/obj.data yolo-obj.cfg yolov4.conv.137`
   
### Inferencing

1. For Image:
`!./darknet detector test data/obj.data cfg/yolov4-custom.cfg yolov4-custom_best.weights test_image.jpg -thresh 0.3`
check `darknet/predictions.jpg`

2. For video:
`!./darknet detector demo data/obj.data cfg/yolov4-custom.cfg yolov4-custom_best.weights -dont_show test_vid.mp4 -thresh 0.5 -i 0 -out_filename output.mp4`

