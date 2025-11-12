import cv2 
import os
import time
import uuid
img_path= 'imgs'
labels= ['hello', 'thanks', 'yes', 'no']
no_imgs= 35
for l in labels:
    os.makedirs(os.path.join(img_path, l), exist_ok=True)
    cap= cv2.VideoCapture(0) 
    print('Collecting images for {}....'.format(l))
    time.sleep(5)
    for imgnum in range(no_imgs):
        ret, frame= cap.read()
        imgname= os.path.join(img_path, l, l+'.'+'{}.jpg'.format(str(uuid.uuid1())))
        cv2.imwrite(imgname, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    print("Done collecting for {}...".format(l))
cv2.destroyAllWindows()
