import time
import numpy as np
import cv2

fourcc=cv2.VideoWriter_fourcc(*'XVID')
output_file=cv2.VideoWriter("output.avi",fourcc,20.0,(640,480))
#starting the webcam
cap=cv2.VideoCapture(0)

#following the webcam to start sleeping it for 2 sec
time.sleep(2)
bg=0

for  i in range(60):
    ret,bg=cap.read()

bg=np.flip(bg,axis=1)

while(cap.isOpened()):
    ret,img=cap.read()
    if not ret:
        break
    img=np.flip(img,axis=1)
    #converting color from bgr to hsv
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #generating mask to detect red color
    #these values can be changed as per the color 
    lower_red=np.array([0,120,50])
    upper_red=np.array([[10,255,255]])
    mask_1=cv2.inRange(hsv,lower_red,upper_red)

    lower_red=np.array([170,120,70])
    upper_red=np.array([[180,255,255]])
    mask_2=cv2.inRange(hsv,lower_red,upper_red)

    mask_1=mask_1+mask_2
    #open and expand the image there is mask 1 color 
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
    mask_1=cv2.morphologyEx(mask_1,cv2.MORPH_DILATE,np.ones((3,3),np.uint8))
    
    #selecting only the part that dose not have mask1
    mask_2=cv2.bitwise_not(mask_1)
    
    #keeping the image part witout the red color
    res_1=cv2.bitwise_and(img,img,mask=mask_2)

    #keeping the image part with the red color 
    res_2=cv2.bitwise_and(bg,bg,mask=mask_1)

    #generating the final output by merging res-1 andres_2
    final_output=cv2.addWeighted(res_1,1,res_2,1,0)
    output_file.write(final_output)

    #displaying thhe output to the user
    cv2.imshow("magic",final_output)
    cv2.waitKey(1)
    cap.release()
    out.release()
    cv2.destroyAllWindows()
