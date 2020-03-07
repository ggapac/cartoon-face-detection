import cv2
import os
import json
import re


def resize_img(img, max_width):
    if img.shape[1] > max_width:
        resize_factor = 1 / (img.shape[1] / max_width)
        new_height = int(img.shape[0] * resize_factor)
        resized = cv2.resize(img, (max_width, new_height), interpolation=cv2.INTER_AREA)
        return resized
    return img


def img_to_greyscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def dir_structure(path):
    if not os.path.exists(path):
        os.makedirs(path)


def preprocessing(max_width, rgb2gray, subdirectory):
    path_dir_raw = f"../data/raw/{subdirectory}"
    path_dir_test = f"../data/test/{subdirectory}"

    dir_structure(path_dir_test)

    for filename in os.listdir(path_dir_raw):
        img = cv2.imread(f"{path_dir_raw}/{filename}")
        if img is not None:
            if max_width is not None:
                img = resize_img(img, max_width)
            if rgb2gray:
                img = img_to_greyscale(img)
            status = cv2.imwrite(f"{path_dir_test}/{filename}", img)
            if status is False:
                print("Warning, was not able to save the preprocessed image.")


def annotation_preprocessing(file, filename_rgx):
    ann_dict = {}
    with open(file, 'r') as fp:
        for line in fp:
            json_obj = json.loads(line)
            filename = re.search(filename_rgx, json_obj["content"])[0]
            ann_dict[filename] = json_obj["annotation"]
    return ann_dict
