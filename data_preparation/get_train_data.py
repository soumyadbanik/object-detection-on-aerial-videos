import os
import cv2
import csv
import time
import subprocess
import shutil
import pandas as pd

dirct =  os.getcwd()                  #r'/home/soumyad/mlproj/sdd
sdd = os.path.join(os.path.split(dirct)[0], "stanford_dd_final")
img_dir = os.path.join(sdd, "images")
label_dir = os.path.join(sdd, "labels")
_list_dir = [sdd, img_dir, label_dir]

train_csv = os.path.join(sdd, "train.csv")
train_csv_cols = []

for dirs in _list_dir:
    try:
        os.mkdir(dirs)
    except OSError as error:
        print(error)
    
total_labels = 0
start = time.time()
no_of_vid = 0
start = time.time()
#vid_data_dir = ''
for subdir, dirs, files in os.walk(dirct):
    '''print('subdir', subdir)
    print('dirs:', dirs)
    print('files:', files)'''
    
    for file in files:
        if file.endswith('.mov'):
            #no_of_vid+=1
            f = os.path.join(subdir, file)
            vid_name = f.split('/')[-2]
            #if os.path.isfile(f):
            print('\n')
            print('current subdirectory: ', subdir)
            #print('count:', c)
            fr_path = os.path.join(subdir, 'frames')
            try:
                os.mkdir(fr_path)
            except OSError as error:
                print(error)
            
            print('Video file: ',f)
            print('Frame dir path: ',fr_path)
            print('\n')
            
            query = "ffmpeg -i " + f + " -qscale:v 2 -crf 18 " + fr_path + "/" + vid_name + "_%d.jpg"       #extracting the frames from all videos and keeping them into another directory named 'frames'
            print(query)
            response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()
            s = str(response).encode('utf-8')
            print(vid_name+" is Done...")
            print('current subdirectory: ', subdir)
            
            label_path = os.path.join(dirct, 'labels', vid_name, "annotations.txt")
            df_labels = pd.read_csv(label_path, names=['id', 'left', 'top', 'right', 'bottom', 'frames','a','b','c','class'], sep=' ')  #we are not concerned with some columns e.g. a,b,c
            df_labels.sort_values(['frames'], axis=0, ascending=True, inplace=True)
            selected = pd.DataFrame(df_labels, columns = ['left', 'top', 'right', 'bottom', 'frames','class'])
            print(selected)
            
            frame_list = []
            frame = 0
            for x, row in selected.iterrows():
                frame = int(row['frames'])
                       
                if frame%30 ==0:
                    
                    fr_name = vid_name+'_'+str(frame+1)+'.jpg'
                    frame_path = os.path.join(fr_path, fr_name)
                    img = cv2.imread(frame_path)
                    frame_txt = fr_name.split('.')[0] +'.txt'
                    labels_per_frame = os.path.join(label_dir, frame_txt)
                    
                    rows = selected.loc[selected['frames'] == frame]
                    each_line=[]
                    if frame not in frame_list:
                        frame_list.append(frame)
                    for i, obj in rows.iterrows():
                        class_lbl = 0
                        left  = int(obj['left'])
                        top   = int(obj['top'])
                        right = int(obj['right'])
                        bottom= int(obj['bottom'])
                        _class= obj['class']
                        if _class =='Pedestrian':
                            class_lbl=1
                        elif _class == 'Biker':
                            class_lbl=2
                        elif _class == 'Skater':
                            class_lbl=3
                        elif _class == 'Cart':
                            class_lbl=4
                        elif _class == 'Car':
                            class_lbl=5
                        elif _class == 'Bus':
                            class_lbl=6
                        total_labels+=1
                        x_norm = (left+((right-left)/2))/img.shape[1]
                        y_norm = (top+((bottom-top)/2))/img.shape[0]
                        width_norm = (right-left)/(img.shape[1])
                        height_norm = (bottom-top)/(img.shape[0])
                        _each_line = [class_lbl, x_norm, y_norm, width_norm, height_norm]
                        each_line.append(_each_line)
                
                        with open(labels_per_frame, 'w') as file1:
                            for data in each_line:
                                for _data in data:
                                    file1.writelines("%s " %_data)
                                file1.writelines('\n')
                        file1.close()
            for _frame in frame_list:
                fr_name1 = vid_name+'_'+str(_frame+1)
                shutil.copy(os.path.join(fr_path, fr_name1+'.jpg'), img_dir)
                print(fr_name1)
                train_csv_cols.append({'image': fr_name1+'.jpg',
                                       'label': fr_name1+'.txt'})
            print(_each_line)
            print(left, right, top, bottom)
            print('height: {}, width: {}'.format(img.shape[0], img.shape[1]))
            
            print(frame_list)
            print('Last frame:{}'.format(frame))
            print('Done')
#print(train_csv_cols)
header = ['image', 'label']
with open(train_csv, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=header)
    writer.writeheader()
    writer.writerows(train_csv_cols)
time.sleep(1)
end = time.time()
print(f"Time taken: {(end-start)/60} minutes")
