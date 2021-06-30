import os
import csv
import cv2
import time
import shutil
import subprocess
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

dirct =  os.getcwd()                  #r'/home/soumyad/mlproj/sdd
sdd = os.path.join(os.path.split(dirct)[0], "stanford_dd_yolo")
img_dir = os.path.join(sdd, "images")
label_dir = os.path.join(sdd, "labels")
_list_dir = [sdd, img_dir, label_dir]

train_csv = os.path.join(sdd, "train.csv")
heights_hist = os.path.join(sdd, "height_hist.png")
widths_hist = os.path.join(sdd, "widths_hist.png")
train_csv_cols = []
heights = []
widths = []
_data = [[]]
c = 0

for dirs in _list_dir:
    try:
        os.mkdir(dirs)
    except OSError as error:
        print(error)
    
total_labels = 0
total_lbl_per_vid = 0
start = time.time()
no_of_vid = 0
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
            
            '''query = "ffmpeg -i " + f + " -qscale:v 2 -crf 18 " + fr_path + "/" + vid_name + "_%d.jpg"
            print(query)
            response = subprocess.Popen(query, shell=True, stdout=subprocess.PIPE).stdout.read()
            s = str(response).encode('utf-8')'''
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
                        height = bottom-top
                        heights.append(height)
                        width = right-left
                        widths.append(width)
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
                        c+=1
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

print(len(widths), c)
#print(heights[len(heights)-1])
print(f'Max_height: {max(heights)}, Max_width: {max(widths)}, Mean_height: {np.mean(heights)}, Mean_width: {np.mean(widths)}')

#height_plot
_data = [widths, heights]

for item in _data:
    plt.ylim(0,1)
    ax = sns.histplot(data=item,binwidth=5, stat='density', color='g', alpha=0.3, linewidth=0)
    ax_kde = sns.kdeplot(data=item,shade=False, color='crimson')
    ax_kde.axvline(np.mean(item), color='r', ls=':', label=f'Mean = {int(np.mean(item))}')
    ax_kde.legend()
    kdeline = ax_kde.lines[0]
    xs = kdeline.get_xdata()
    ys = kdeline.get_ydata()
    ax_kde.fill_between(xs, 0, ys, facecolor='crimson', alpha=0.5)
    fig_kde = ax_kde.get_figure()
    fig = ax.get_figure()
    if item == widths:
        fig.savefig(widths_hist)
        fig_kde.savefig(widths_hist)
        fig.clf()
    else:
        fig.savefig(heights_hist)
        fig_kde.savefig(heights_hist)
        fig.clf()

time.sleep(1)
end = time.time()
print(f"Time taken: {(end-start)/60} minutes")
