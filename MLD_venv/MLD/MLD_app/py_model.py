# import necessary modules
import cv2
import numpy as np
import os
# import the yolo detector file
from MLD_app.YoloDetector import YoloDetector
import MLD_app.sqlite_db as sqlite_db
import MLD_app.history_delete as del_sql


def Dropdwn_class():
	classes = []
	with open("E:\MLD\MLD_app\coco.names", 'r') as f:
		classes = [w.strip() for w in f.readlines()]
	class_list = list(cls for n, cls in enumerate(classes))
	
	return class_list


def selectedimg(selectedimages):
	classes = []
	with open("E:\MLD\MLD_app\coco.names", 'r') as f:
		classes = [w.strip() for w in f.readlines()]
	selected = {}
	# select specific classes that you want to detect out of the 80 and assign a color to each detection # 
	#for img in selectedimages:
	#selected = {"person": (0, 255, 255),
			#"laptop": (0, 0, 0)}
	#if selectedimages in selected.keys():
	selected = {str(selectedimages): tuple(np.random.randint(0,255, size=3)) }
	# initialize the detector with the paths to cfg, weights, and the list of classes
	detector = YoloDetector("E:\MLD\MLD_app\yolov3-tiny.cfg", "E:\MLD\MLD_app\yolov3-tiny.weights", classes)
	# initialize video stream
	cap = cv2.VideoCapture("E:\MLD\MLD_app\input_video.mp4")
	# read first frame
	count = 0
	ret, frame = cap.read()
	# loop to read frames and update window
	while ret and count < 4:
		# this returns detections in the format {cls_1:[(top_left_x, top_left_y, top_right_x, top_right_y), ..],
		#                                        cls_4:[], ..}
		# Note: you can change the file as per your requirement if necessary
		detections = detector.detect(frame)
		# loop over the selected items and check if it exists in the detected items, if it exists loop over all the items of the specific class
		# and draw rectangles and put a label in the defined color
		for cls, color in selected.items():
			if cls in detections:
				for box in detections[cls]:
					x1, y1, x2, y2 = box
					thickness = 1
					color = tuple(int(c) for c in color)
					# frame = np.rollaxis(frame,2,0)
					cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
					frames = cv2.putText(frame, cls, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)
					path = os.path.join('E:/MLD/media/', cls)+'/' 
					
					if cls.startswith('person') or cls.startswith('laptop'):
						if not os.path.exists(path):
							os.mkdir(path)
						else :
							print("Directory already existed : ")
						cv2.imwrite(str(path) + cls+str(count)+'.jpg',frames)
						blobdata = sqlite_db.convertToBinaryData(str(path) + cls+str(count)+'.jpg')
						sqlite_db.db_sqlite_qry(cls, blobdata)
						count+=1
		ret, frame = cap.read()
	
	delete_query = del_sql.deleteHistory()
	print(delete_query)
			
	return str(count)
	