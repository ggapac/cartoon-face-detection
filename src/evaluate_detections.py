import numpy as np


def intersection_over_union(faces, annotations, shape):
    area_annot = np.zeros(shape[0:2])
    area_detect = np.zeros(shape[0:2])

    for i in range(0, len(annotations)):
        ann_points = annotations[i]["points"]
        area_annot[int(ann_points[0][1] * shape[0]):(int(ann_points[2][1] * shape[0])),
        int(ann_points[0][0] * shape[1]):(int(ann_points[2][0] * shape[1]))] = 1

    for j in range(0, len(faces)):
        area_detect[faces[j][1]:(faces[j][1] + faces[j][3]),
        faces[j][0]:(faces[j][0] + faces[j][2])] = 1

    area_intersect = ((area_annot + area_detect) > 1).sum()
    area_annot = np.count_nonzero(area_annot)
    area_detect = np.count_nonzero(area_detect)

    return area_intersect / (area_detect + area_annot - area_intersect)
