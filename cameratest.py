import cv2

num = input('which camera 6,7,8 or 9 :  ')
rtsp_link = "rtsp://admin:q12345678@192.168.7."+num+":554/Streaming/Channels/101 RTSP/1.0"
video_capture = cv2.VideoCapture(rtsp_link)

#print(read_flag,'  ',frame)
#video_capture = cv2.VideoCapture(0)

while True:
    read_flag, frame = video_capture.read()
    cv2.imshow('video2',frame)
    cv2.resize(frame, (1000, 600), interpolation=cv2.INTER_CUBIC)
    #cv2.imshow('video',frame)
    #print(read_flag)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_captuure.release()
cv2.destroyAllWindows()
	





