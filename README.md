# object detection on stanford-drone-dataset
This repo contains the codes and steps to perform object detection on stanford drone dataset in DarkNet YOLO-V4 framework. Below you can see the visualization of detected objects with their accuracies.
### Demo 
Inferencing on scene deathCircle of Stanford Drone Dataset:

![output](https://github.com/soumyadbanik/object-detection-on-aerial-images/blob/main/results/output2.gif)

Wait! Wait! There are lot more boring stuffs to do bedore diving into the deep learning. Since this is a video dataset, the major task is to preprocess and clean the data. There is no point to train with the whole dataset. First of all, you need to choose some of the videos according to your purpose of detection. But how you would choose them. 80-90% of the dataset is occupied by pedestrians and bikers. So, if you want to detect only cars, obviously random selection of videos will not work. I've made it easy for you.
(If you want to skip this part, download the prepared dataset from my [Drive](https://drive.google.com/drive/folders/1fxhziv-1ZB5mPqS2aNDAfdJdPCxVL1T-?usp=sharing))

### Preparing the Dataset

1. Download the dataset from [here](https://cvgl.stanford.edu/projects/uav_data/)
2. Modify the directoy format into this format from which ever format you got. This will make the process easier. ![fileformat](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/Screenshot%20from%202021-06-30%2020-22-04.png)
3. Put the `get_stats.py` into the parent directory i.e the dataset directory. This will give you the whole summery into each directory for each video in a Bar chart format. Like this ![bar](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/vid_data.png)This will also help you to maintain the class imbalances in your final dataset.
5. Select the videos according to your detection task and put into another directory.
6. Then rename the videos and labels into this format. 
![img1](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/Screenshot%20from%202021-06-30%2021-05-32.png) ![img2](https://github.com/soumyadbanik/object-detection-on-aerial-videos/blob/main/misc/Screenshot%20from%202021-06-30%2021-06-21.png)
 This is going to help you in your remaining tasks.
7. Put `get_train.py`, `get_test.py`, `get_valid.py` and run them by
    `python3 get_train.py` and similarly remianing two.
8. This will split each video into frames and store each 30th, 89th and 91st frame for train, test & validation respectively(taking 1 frame per second) And also generate corresponding `.csv` files. Make sure your system have `ffmpeg` installed otherwise do 
 `sudo apt update` then `sudo apt install ffmpeg`
9. . It will convert the labels to YOLO format also. YOLO needs the labels in the format `<class_id x_center_norm y_center_norm width height>` where `x_center_norm = x_center/width, y_center_norm = y_center/height` . For example for image.jpg, the image.txt will contain 
```csv
1 0.8778 0.0143 0.04311 0.0287
2 0.8040 0.0236 0.06959 0.0435
2 0.0083 0.1345 0.01664 0.0379
```

  Now you are good to go. 

10. 
