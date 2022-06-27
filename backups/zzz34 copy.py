from pprint import pprint
import cv2
from PIL import Image as im
cap= cv2.VideoCapture('/media/eu4/49fa581d-6d91-4c0f-886a-2d6d1a2b9857/project/Automation/telegram_avds/office-work/backups/TDM_EXE.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
fps=cap.set(cv2.CAP_PROP_POS_MSEC,7000)
read,frame=cap.read()
success, image = cap.read()
count = 1
fra=[]
value=[]
bad_pixel=[]
while read:
    cap.set(cv2.CAP_PROP_POS_MSEC,count*1000)
    read,frame=cap.read()
    if success:
            ti=cap.get(cv2.CAP_PROP_POS_MSEC)
            #print(ti)
            milisecond=((ti/1000)%60)*1000
            minutes=(ti/(1000*60))%60
            hours=(ti/(1000*60*60))%24
            #minutes=(ti/(1000*60))%60
            #frame_time1=round(minutes, 2)
            #frame_time=round((milisecond/1000)%60, 4)
            frame_time=round((minutes/1000*60)%60, 4)
            #print("Frame Time:",frame_time)
            for x in range(0,1280-1):
                for y in range(0,720-1):
                    v = image[y,x]
                    v1=v.tolist()
                    #print(v1)
                    #print("Pixel at ({}, {}) - Value {} ".format(x,y,v))
                    if v1>=[127,127,127]:
                        print("Bad pixel Values",v1,minutes,"sec")
            bad_dict={"bad_pixel":v1,"time_stamp":minutes}

            bad_pixel.append(bad_dict)  
        #print("Pixel_Detect:",bad_pixel)       
    #else:
        #print("Good Pixel Values",v1,minutes,"sec") 
    #fra.append(frame)
    count += 17
    if count==10:
        break
    # print("Pixel_Detect:",bad_pixel)
pprint(bad_pixel)
cap.release()
cv2.destroyAllWindows()

