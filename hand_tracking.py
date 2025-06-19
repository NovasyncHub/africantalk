import cvzone 
import cv2 


from cvzone.HandTrackingModule import HandDetector 


detector=HandDetector(detectionCon=0.8,maxHands=1)


sequence=[]
def track(video_path="None"):
    stop=False
    if video_path=="None":
        cap=cv2.VideoCapture(0 if video_path=="None" else video_path)
    else:
        cap=cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) if video_path != "None" else float('inf')
    while True:
        message=None
        sucess,frame=cap.read()
        hands,frame=detector.findHands(frame)

        if hands:
            for hand in hands:
                #lmList=hand['lmList']
                #bbox=hand['bbox']
                #center=hand['center']
                #type=hand['type']
                fingers=detector.fingersUp(hand)

                if fingers==[0,1,1,0,0]:
                    cv2.putText(frame,"Peace",(50,100),cv2.FONT_HERSHEY_SIMPLEX,
                                2,(0,255,0),3)
                    message="Peace"
                elif fingers==[0,0,0,0,0]:
                    cv2.putText(frame,"Poing",(50,100),cv2.FONT_HERSHEY_SIMPLEX,
                                2,(0,0,255),3)
                    message="Poing"
                elif fingers==[1,1,1,1,1]:
                    cv2.putText(frame,"Main ouverte",(50,100),cv2.FONT_HERSHEY_SIMPLEX,
                                2,(255,0,0),3)
                
                    message="Main ouverte"
                if message:
                    if sequence!=[]:
                        if sequence[-1]!=message:               
                            sequence.append(message)
                    else:
                        sequence.append(message)
                
                if fingers==[1,0,0,0,0]:
                    stop=True
            
                    
       #cv2.imshow("Tracking",frame)
        crt_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
        
        if cv2.waitKey(1) & 0xFF ==ord('q') or stop or crt_frame >= total_frames:
            break 
        #cap.release()
        #cv2.destroyAllWindows()
    print("List sequence",sequence)
    output=None
    if len(sequence)>1:
        output=",".join(sequence)
    elif len(sequence)==1:
        output=sequence[0]
    print("Sortie",output)
    return output
