import cv2
import sys
import time
import logging
from pocketbase import PocketBase

#thres = 0.45 # Threshold to detect object

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

	# pb controller
    pb = PocketBase("https://oss-be-pb.fly.dev/")
    pb.collection('users').auth_with_password(sys.argv[1], sys.argv[2])
    spaceRecord = pb.collection('sportSpaces').get_one(sys.argv[3])
    logger.info("Starting the live stream at {}".format(spaceRecord.name))

    while True:
        success, img = cap.read()
        result, objectInfo = getObjects(img,0.6,0.2,objects=['person'])
        if timer % 120 == 0:
            pb.collection('sportSpaces').update(sys.argv[3], {
                    "name": spaceRecord.name,
                    "logo": spaceRecord.logo,
                    "link": spaceRecord.link,
                    "coords": spaceRecord.coords,
                    "price": spaceRecord.price,
                    "availability": len(objectInfo),
                    "address": spaceRecord.address,
                    "markerLogo": spaceRecord.marker_logo,		
            })
        cv2.imshow("Output",img)
        key = cv2.waitKey(1) & 0xFF
        timer += 1
		# if the `q` key was pressed, break from the loop
        if key == ord("q"):
          break
