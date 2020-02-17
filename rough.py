import cv2



def f1():
    cap=cv2.VideoCapture(0)
    ad=cap.read()
    print(ad)
    cap.release()
    cv2.destroyAllWindows()
    return str(ad[0])