import cv2


def viola_jones_face(img, classifier):
    faces = classifier.detectMultiScale(img)
    return faces


def viola_jones_combine(img, class_face, class_eye):
    faces = class_face.detectMultiScale(img)
    eyes = class_eye.detectMultiScale(img)

    faces_keep = []

    if len(eyes) >= 2 and len(faces) >= 1:
        for i in range(0, len(faces)):
            eye_count = 0
            for j in range(0, len(eyes)):
                if eyes[j][0] > faces[i][0] and eyes[j][1] > faces[i][1]\
                        and eyes[j][2] < faces[i][2] and eyes[j][3] < faces[i][3]:
                    eye_count += 1

            if eye_count == 2:
                faces_keep.append(i)

    if len(faces_keep) is 0:
        return None
    return faces[faces_keep]
