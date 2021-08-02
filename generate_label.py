import csv
import json
import os
import matplotlib.pyplot
from PIL import Image
import random 
from os import path
import sys
import numpy as np
from skimage.draw import * 
from matplotlib import cm
import argparse
import glob

def create_mask_from_annotation(image,image_data ,filename, dest_path,className,image_path =None):


    #todo: add class list and relative class value for multiple labels
    or_img=np.asarray(image)
    width = or_img.shape[1]
    height = or_img.shape[0]
    print(height,width)
    img = np.zeros((height, width), dtype=np.uint8)

    #for each region labeled in the image 
    for region in range(len(image_data["regions"])):
        print(region)
        #pick only patch regions
        if( image_data["regions"][str(region)]['region_attributes']['label'] == className):      
            
            x = image_data["regions"][str(region)]["shape_attributes"]['all_points_x']
            y = image_data["regions"][str(region)]["shape_attributes"]['all_points_y']
   
            rr, cc = polygon(y, x) 
            problem = False
            for r in rr:
                if(r >  height): 
                    print("problem", filename)
                    problem = True
                    break
            for c in cc:
                if(c >  width): 
                    print("problem", filename)
                    problem = True
                    break
            if(problem is not True):
                img[rr,cc] = 1


    im = Image.fromarray(np.uint8(cm.gist_earth(img)*255))
    im.save(dest_path +'/' + filename, "PNG")
    #blend image with labels generation
    #original_img = Image.open(image_path + "/" + filename).convert("RGB")
    #label_img = Image.open(path + "/" + filename).convert("RGB")
    #i = Image.blend(label_img, original_img, 0.6)
    #i.save(path + "/" + filename, "PNG")

    return img

def generate_labels(dataset_path, label_file_path,label_name):
    images_path = dataset_path  + '/images'
    label_path = dataset_path  + '/labels'
    #check wheter directory already exists
    if( os.path.isdir(label_path) is not True): 
        os.mkdir(label_path)  

    if( os.path.isdir(images_path) is not True): 
        os.mkdir(images_path) 

    try:
        with open(label_file_path) as json_file:
            data = json.load(json_file)
            for filename in data:
                print('checking existence for ' + dataset_path + '/' + filename)
                print(os.path.isfile(dataset_path + '/' + filename))
                if(os.path.isfile(dataset_path + '/' + filename)):
                    #open image
                    img = Image.open( dataset_path + '/' + filename) 
                    #get coordinates and generate labeled image
                    create_mask_from_annotation(img, data[filename], filename, label_path ,label_name, dataset_path)
                    img.save(images_path +'/' + filename, "PNG")

    except OSError as e:
        print("No label file was found. Make sure you had placed it in the same directory you indicated for the dataset path.")
    

def generate_labels_splitted_dataset(dataset_path, labels_path,label_name):

    train_image_path = dataset_path + '/images/train'
    valid_image_path = dataset_path + '/images/valid'
    label_path = dataset_path + '/labels'

    #check wheter directory already exists
    if( os.path.isdir(label_path) is not True): 
        os.mkdir(label_path)  

    #check wheter directory already exists
    train_label_path = dataset_path + '/labels/train'
    if( os.path.isdir(train_label_path) is not True): 
        os.mkdir(train_label_path)  

    valid_label_path = dataset_path + '/labels/valid'
    if( os.path.isdir(valid_label_path) is not True): 
        os.mkdir(valid_label_path)  


    with open(label_file_path) as json_file:
        data = json.load(json_file)
        for filename in data:
            print(train_image_path + '/' + filename)
            print(os.path.isfile(train_image_path + '/' + filename))
            if(os.path.isfile(train_image_path + '/' + filename)):
                #open image
                img = Image.open( train_image_path + '/' + filename) 
                #get coordinates and generate labeled image
                create_mask_from_annotation(img, data[filename], filename, label_path + "/train",train_image_path)

            elif(os.path.isfile(valid_image_path + '/' + filename)):   
                img = Image.open( valid_image_path + '/' + filename) 
                #get coordinates and generate labeled image
                create_mask_from_annotation(img, data[filename], filename, label_path + "/valid",valid_image_path)

def check_unnannotated_labels(dataset_path,label_file_path):

    #check existence of the label_file
    assert(os.path.isfile(label_file_path) is True)  

    with open(label_file_path) as json_file:
        
        data = json.load(json_file)

        files = glob.glob(dataset_path + "/*.png")
        files = sorted(files, key=lambda x: int(os.path.basename(x).split('.')[0].split('-')[1]) )
        print('all the files still to be labeled are the following:')
        count = 0
        for file in files:
            if(os.path.basename(file) not in data):
                print(os.path.basename(file))
                count += 1
        print('totat number to still label:  ', count)

def count_images(dataset_path, starting_point):
    ind = starting_point
    base = 'Image-'
    for r, d, f in os.walk(dataset_path):
        for file in f:
            filename = base + str(ind)
            if(file.split(".")[1] != "py"):
                os.rename(file, filename + ".png")
            ind = ind + 1


if __name__ == "__main__":
    # initialize ArgumentParser class of argparse
    parser = argparse.ArgumentParser()
    # the argument split_dataset should be True if the dataset was already splitted into train,valid and test set
    parser.add_argument(
    "--split_dataset",
    type=bool
    )

    parser.add_argument(
    "--check_labels",
    type=bool
    )

    #dataset path is the main directory where to find the dataset
    parser.add_argument(
    "--dataset_path",
    type=str
    )

    #label name to look for in the label json 
    parser.add_argument(
    "--label_name",
    type=str
    )

    #name of the label json containing the annotated labels
    parser.add_argument(
    "--label_file_path",
    type=str
    )

    #name of the label json containing the annotated labels
    parser.add_argument(
    "--count_labels",
    type=int
    )


    #name of the label json containing the annotated labels
    parser.add_argument(
    "--starting_point",
    type=int
    )




    # read the arguments from the command line
    args = parser.parse_args()

    #we can count or check labels. We can't do both of the things
    assert((args.check_labels and not args.count_labels) or (not args.check_labels and args.count_labels)  or \
    (not args.check_labels and not args.count_labels))

    # do we have to check which image still needs to be annotated?
    if(args.count_labels): 
        count_images(args.dataset_path,args.starting_point)
    # do we have to check which image still needs to be annotated?
    if(args.check_labels): 
        check_unnannotated_labels(args.dataset_path,args.label_file_path)
    else:  
        if args.split_dataset:
            generate_labels_splitted_dataset(args.dataset_path, args.label_file_path, args.label_name)
        else:
            generate_labels(args.dataset_path,args.label_file_path, args.label_name)