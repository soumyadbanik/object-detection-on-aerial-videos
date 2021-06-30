import os
#dir_ = "/home/soumyad/mlproj/stanford_dd"
dir_ = os.getcwd()
label_dir = os.path.join(dir_, 'labels')
count = 0
no_of_vids=0
for subdir, _, files in os.walk(dir_):
    for file in files:
        if file.endswith('.mov'):
            no_of_vids+=1
        elif file.endswith('.txt'):
            file_path = os.path.join(subdir, file)
            file1=open(file_path, 'r')
            lines = file1.readlines()
            count+=len(lines)
            #print(file_path)
            #file1.close()
print(count, no_of_vids)