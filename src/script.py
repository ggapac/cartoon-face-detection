from prepare_data import *
from viola_jones import *
from evaluate_detections import *
import numpy as np
import json


# parameters
cartoons = ["frozen", "southpark", "simpsons"]
max_width = 700
rgb2gray = True
use_combined_detection = False
save_faces = True

# classifiers
face_cascade = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier(f"{cv2.data.haarcascades}haarcascade_eye.xml")


results = {}

for cartoon in cartoons:

    # paths
    path_dir_test = f"../data/test/{cartoon}"
    path_dir_output = f"../output/{cartoon}"
    if use_combined_detection:
        path_dir_output = f"{path_dir_output}_2"
    ann_file = f"../data/test/{cartoon}.json"

    filename_rgx = f"(?:{cartoon}_)\\s*(.*$)"

    # preprocessing
    preprocessing(max_width, rgb2gray, cartoon)
    dir_structure(path_dir_output)
    ann_dict = annotation_preprocessing(ann_file, filename_rgx)

    # detection
    iou_overall = np.zeros(len(os.listdir(path_dir_test)))
    i = 0

    for filename in os.listdir(path_dir_test):
        img = cv2.imread(f"{path_dir_test}/{filename}")
        if img is not None:
            if use_combined_detection:
                faces = viola_jones_combine(img, face_cascade, eye_cascade)
            else:
                faces = viola_jones_face(img, face_cascade)

            iou = 0
            if faces is not None:
                iou = intersection_over_union(faces, ann_dict[f"{cartoon}_{filename}"], img.shape)
                if save_faces:
                    for (x, y, w, h) in faces:
                        img = cv2.rectangle(img, (x, y), (x + w, y + h), (4, 8, 170), 2)
            if save_faces:
                cv2.imwrite(f"{path_dir_output}/{filename}", img)

            iou_overall[i] = iou
        i += 1

    results[cartoon] = iou_overall.tolist()


json = json.dumps(results)
if use_combined_detection:
    outfile = "../output/results_2.json"
else:
    outfile = "../output/results.json"
f = open(outfile, "w")
f.write(json)
f.close()

