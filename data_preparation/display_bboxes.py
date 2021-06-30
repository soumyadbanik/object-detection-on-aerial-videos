import cv2
import pandas as pd

file = pd.read_csv('/home/soumyad/mlproj/sdd/gates/gates_annotate/video4/annotations.txt', names=['id', 'left', 'top', 'right', 'bottom', 'frames','a','b','c','class'], sep=' ')
selected = pd.DataFrame(file, columns = ['left', 'top', 'right', 'bottom', 'frames','class'])
c=0
for x, row in selected.iterrows():
    frame = int(row['frames'])
    rows = selected.loc[selected['frames'] == frame]
    im = cv2.imread("/home/soumyad/mlproj/video4/frames/{:d}.jpg".format(frame+1))
    for i, obj in rows.iterrows():
        left  = int(obj['left'])
        top   = int(obj['top'])
        right = int(obj['right'])
        bottom= int(obj['bottom'])
        #frame = int(x.split(' ')[5])+1
        #print(frame)
        c+=1
        #img= cv2.UMat(im)
        if obj['class'] =='Pedestrian':
            color = (0,0,255)
            im = cv2.rectangle(im,(left,top), (right,bottom), color, 1)
        elif obj['class']=='Biker':
            color = (0,255,0)
            im = cv2.rectangle(im,(left,top), (right,bottom), color, 1)
        #img = cv2.imread(bb)
    cv2.imwrite("/home/soumyad/mlproj/video4/annotated_frames/{:d}.jpg".format(frame+1), im)
    break
#f.close()
print('Last frame:{}'.format(frame+1))
print('Done')