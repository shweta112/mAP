import sys
import os
import glob
import json


# change directory to the one with the files to be changed
path_to_folder = '../ground-truth'
#print(path_to_folder)
os.chdir(path_to_folder)

# old files (json) will be moved to a "backup" folder
## create the backup dir if it doesn't exist already
if not os.path.exists('backup'):
    os.makedirs('backup')

# get json format files
json_list = glob.glob('*.json')
if len(json_list) == 0:
    print('Error: no .json files found in predicted')
    sys.exit()

for tmp_file in json_list:
    #print(tmp_file)
    data = json.load(open(tmp_file, 'r'))

    for img in data:
        # 1. create new file
        with open(img['filename'].replace('png', 'txt'), 'a') as new_f:
            for obj in img['annotations']:
                obj_name = 'person'
                left = obj['x']
                top = obj['y']
                right = obj['width'] + left
                bottom = obj['height'] + top
                new_f.write(obj_name + ' ' + str(left) + ' ' + str(top) + ' ' + str(right) + ' ' + str(bottom) + '\n')
    # 2. move old file (json format) to backup
    os.rename(tmp_file, "backup/" + tmp_file)
print("Ground truth conversion completed!")

# change directory to the one with the files to be changed
path_to_folder = '../predicted'
#print(path_to_folder)
os.chdir(path_to_folder)

# get json format files
json_list = glob.glob('*.json')
if len(json_list) == 0:
    print('Error: no .json files found in predicted')
    sys.exit()

for tmp_file in json_list:
    #print(tmp_file)
    data = json.load(open(tmp_file, 'r'))

    for bb in data:
        # 1. create new file or open existing
        with open(bb['image_id'].replace('png', 'txt'), 'a') as new_f:
            obj_name = 'person'
            obj_conf = bb['score']
            left = bb['bbox'][0]
            top = bb['bbox'][1]
            right = bb['bbox'][2] + left
            bottom = bb['bbox'][3] + top
            new_f.write(obj_name + ' ' + str(obj_conf) + ' ' + str(left) + ' ' + str(top) + ' ' + str(right) + ' ' + str(bottom) + '\n')
    # 2. move old file (json format) to backup
    os.rename(tmp_file, "backup/" + tmp_file)
print("Predicted conversion completed!")
