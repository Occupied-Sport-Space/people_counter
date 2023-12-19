import sys
import logging
import cv2
import socketio

#thres = 0.45 # Threshold to detect object
cameraId = 0 # Change for every camera setup!

logging.basicConfig(level = logging.INFO, format = "[INFO] %(message)s")
logger = logging.getLogger(__name__)

classNames = []
classFile = "./coco.names"
with open(classFile,"rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = "./ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = "./frozen_inference_graph.pb"

net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/ 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)


def getObjects(img, thres, nms, draw=True, objects=[]):
    classIds, confs, bbox = net.detect(img,confThreshold=thres,nmsThreshold=nms)
    if len(objects) == 0: objects = classNames
    objectInfo =[]
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            className = classNames[classId - 1]
            if className in objects:
                objectInfo.append([box,className])
                if (draw):
                    cv2.rectangle(img,box,color=(0,255,0),thickness=2)
                    cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                    cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                    cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)

    return img,objectInfo


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    cap.set(3,1920)
    cap.set(4,480)
    timer = 0

    # socket.io instance
    sio = socketio.SimpleClient()
    sio.connect('http://localhost:8000')

    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.6,0.2,objects=['person'])
        sio.emit('count', {"count": len(objectInfo), "spaceId": sys.argv[3], "cameraId": cameraId})
        cv2.imshow("Output",img)
        key = cv2.waitKey(1) & 0xFF
        timer += 1
		# if the `q` key was pressed, break from the loop
        if key == ord("q"):
          break
