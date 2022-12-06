import math
import random
import numpy as np

total_boxes = int(input("How many boxes are there in total?"))
print("Boxes are named in the fasion if B1, B2...Bn")
total_places = int(input("How columns of box stack is there?"))

all_boxes = [f'B{str(i)}' for i in range(1,16)]
all_boxes = np.array(all_boxes, dtype=np.string_)
all_places = np.full((total_places,5),0, dtype=object)

box1 = input('Choose a box now!')
box2 = input(f'Which box do you want to keep on top of {box1}?')
box1 = bytes(box1, 'utf-8')
box2 = bytes(box2, 'utf-8')


places = list(range(0,total_places))

for i in all_boxes:

    for j in places:
        if np.count_nonzero(all_places[j]) == 5:
            places.remove(j)

    random.shuffle(places)
    index = places[0]
    index
    np.put(all_places[index],[-1],i)
    all_places[index] = np.roll(all_places[index],1)

def find_box(box):
    # Finding the index of the box in question. Indeces need not have to be modified for list or array
    index_box = (np.where(all_places==box)[0][0],np.where(all_places==box)[1][0])
    return index_box

def is_top(box):
    # To find if the box in question is at top of the column or not
    index_box = find_box(box)
    is_top = False
    if index_box[1] == 4:
        is_top = True
    elif all_places[index_box[0],index_box[1]+1] == 0:
        is_top = True
    return is_top

def find_right_space(box1,box2):
    # Find the right column where the box can be dropped
    column1 = find_box(box1)[0]
    column2 = find_box(box2)[0]

    if np.count_nonzero(all_places[column1]) <= 4 and is_top(box1)==True and is_top(box2)==True:
        target_column = column1
    else:
        columns = list(range(0,total_places))
        print("Original:", columns)
        columns.remove(column1)
        columns.remove(column2)
        random.shuffle(columns)
        print("Modified:", columns)
        idx = 0
        for idx in columns:
            if np.count_nonzero(all_places[idx]) <= 4:
                target_column = idx
                break

    return target_column

def grasp_box(box1,box2):
    # return the box that has to grasped so that it can be moved in the next step

    if is_top(box1) and np.count_nonzero(all_places[find_box(box1)[0]])==5:
        idx = find_box(box1)
        grasp = box1
        print('If grasp')
        np.put(all_places[idx[0]],idx[1],0)

    elif is_top(box1) and np.count_nonzero(all_places[find_box(box1)[0]])<=4:
        if is_top(box2):
            idx = find_box(box2)
            grasp = box2
            print('Elif If grasp')
            np.put(all_places[idx[0]],idx[1],0)
        else:
            idx = find_box(box2)
            nz_count = np.count_nonzero(all_places[idx[0]])
            grasp = all_places[(idx[0],nz_count-1)]
            print('Else If grasp')
            np.put(all_places[idx[0]],nz_count-1,0)

    else:
        idx = find_box(box1)
        print(idx)
        nz_count = np.count_nonzero(all_places[idx[0]])
        print(f"nz_count:{nz_count}")
        grasp = all_places[(idx[0],nz_count-1)]
        print('Else grasp')
        print(f"In Position Bfore Put is {all_places[idx[0],nz_count-1]}")
        np.put(all_places[idx[0]],nz_count-1,0)
        print(f"In Position After Put is {all_places[idx[0],nz_count-1]}")
        
    print(f"Grasp is {grasp}")

    return grasp

def move_box(box1,box2):
    target_column = find_right_space(box1,box2)
    box_inhand = grasp_box(box1,box2)
    flag = 1
    # If 1, the loop will continue. If 0, the loop will stop
    if box_inhand == box2:
        print("Move_Box if")
        # This condtion is established if and only if both the boxes are the top of the respective columns
        idx = find_box(box1)
        nz_count = np.count_nonzero(all_places[idx[0]])
        grasp = all_places[(idx[0],idx[1]+1)]
        np.put(all_places[idx[0]],nz_count,box2)
        print("Hurry, Successful!")
        flag = 0

    else:
        print("Move_Box Else")
        print(f"target_column is {target_column}")
        nz_count = np.count_nonzero(all_places[target_column])
        print(nz_count)
        np.put(all_places[target_column],nz_count,box_inhand)
        flag = 1

    print(all_places)
    return flag

flag = 1

while flag == 1:
    flag = move_box(box1,box2)