#!/usr/bin/env python3

from pathlib import Path
import cv2
import depthai as dai
import numpy as np
import argparse
import time
import errno
import blobconverter
import os
from utils.functions import *

'''
YOLOP demo running on device with video input from host.
Run as:
python3 -m pip install -r requirements.txt
python3 main.py

ONNX is taken from:
https://github.com/hustvl/YOLOP

DepthAI 2.11.0.0 is required. Blob was compiled using OpenVino 2021.4
'''
syncNN = False

SHAPE = 416
labelMap = [ "person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign", "parking meter", "teddy bear"]

# --------------- Arguments ---------------
parser = argparse.ArgumentParser()
parser.add_argument("-conf", "--confidence_thresh", help="set the confidence threshold", default=0.5, type=float)
parser.add_argument("-iou", "--iou_thresh", help="set the NMS IoU threshold", default=0.3, type=float)

args = parser.parse_args()

CONFIDENCE_THRESHOLD = args.confidence_thresh
IOU_THRESHOLD = args.iou_thresh

# resize input to smaller size for faster inference
NN_WIDTH = 320
NN_HEIGHT = 320

# set initial resize so the input is not too large
IR_WIDTH = 640
IR_HEIGHT = 360

# --------------- Get Blob ------------------
NN_PATH = str(blobconverter.from_zoo(name="yolop_320x320", zoo_type="depthai", shaves = 7))

# --------------- Pipeline ---------------
# Start defining a pipeline
pipeline = dai.Pipeline()
pipeline.setOpenVINOVersion(version = dai.OpenVINO.VERSION_2021_4)

# Create camera node
cam_rgb = pipeline.create(dai.node.ColorCamera)
cam_rgb.setPreviewSize(IR_WIDTH, IR_HEIGHT)
cam_rgb.setInterleaved(False)
cam_rgb.setFps(30)

# Create Manip for image resizing and NN for count inference
manip = pipeline.create(dai.node.ImageManip)
detection_nn = pipeline.create(dai.node.NeuralNetwork)

# Create output links
xout_manip = pipeline.create(dai.node.XLinkOut)
xout_nn = pipeline.create(dai.node.XLinkOut)

xout_manip.setStreamName("manip")
xout_nn.setStreamName("nn")

# Properties
manip.initialConfig.setResize(NN_WIDTH, NN_HEIGHT)
manip.initialConfig.setFrameType(dai.ImgFrame.Type.BGR888p)

# setting node configs
detection_nn.setBlobPath(NN_PATH)
detection_nn.setNumPoolFrames(4)
detection_nn.input.setBlocking(False)
detection_nn.setNumInferenceThreads(2)

# Linking
cam_rgb.preview.link(manip.inputImage)
manip.out.link(xout_manip.input)
manip.out.link(detection_nn.input)
detection_nn.out.link(xout_nn.input)

nn = pipeline.create(dai.node.NeuralNetwork)
nn.setBlobPath(str(Path("yolox_tiny.blob").resolve().absolute()))
nn.setNumInferenceThreads(2)
nn.input.setBlocking(True)

# Send converted frames from the host to the NN
nn_xin = pipeline.create(dai.node.XLinkIn)
nn_xin.setStreamName("nnInput")
nn_xin.out.link(nn.input)

# Send bounding boxes from the NN to the host via XLink
nn_xout = pipeline.create(dai.node.XLinkOut)
nn_xout.setStreamName("nnObj")
nn.out.link(nn_xout.input)

# --------------- Inference ---------------
# Pipeline defined, now the device is assigned and pipeline is started
with dai.Device(pipeline) as device:
    q_manip = device.getOutputQueue(name="manip", maxSize=4, blocking=False)
    q_nn = device.getOutputQueue(name="nn", maxSize=4, blocking=False)
    qNnInput = device.getInputQueue("nnInput", maxSize=4, blocking=False)
    qNn = device.getOutputQueue(name="nnObj", maxSize=4, blocking=True)

    startTime = time.monotonic()
    counter = 0
    fps = 0

    while True:
        manip = q_manip.get()
        manip_frame = manip.getCvFrame()
        
        # Set these according to your dataset
        mean = (0.485, 0.456, 0.406)
        std = (0.229, 0.224, 0.225)
        
        image, ratio = preproc(manip_frame, (SHAPE, SHAPE), mean, std)
        image = list(image.tobytes())
        
        dai_frame = dai.ImgFrame()
        dai_frame.setHeight(SHAPE)
        dai_frame.setWidth(SHAPE)
        dai_frame.setData(image)
        qNnInput.send(dai_frame)
        in_nn = qNn.tryGet()
        if in_nn is not None:
            data = np.array(in_nn.getLayerFp16('output')).reshape(1, 3549, 85)
            predictions = demo_postprocess(data, (SHAPE, SHAPE), p6=False)[0]
            
            boxes = predictions[:, :4]
            scores = predictions[:, 4, None] * predictions[:, 5:]

            boxes_xyxy = np.ones_like(boxes)
            boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2.
            boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2.
            boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2.
            boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2.
            dets = multiclass_nms(boxes_xyxy, scores, nms_thr=0.45, score_thr=0.3)

            if dets is not None:
                final_boxes = dets[:, :4]
                final_scores, final_cls_inds = dets[:, 4], dets[:, 5]

                for i in range(len(final_boxes)):
                    bbox = final_boxes[i]
                    score = final_scores[i]
                    class_index = int(final_cls_inds[i])

                    if score >= 0.1 and class_index < len(labelMap):
                        class_name = labelMap[class_index]
                        
                        # Limit the bounding box to 0..SHAPE
                        bbox[bbox > SHAPE - 1] = SHAPE - 1
                        bbox[bbox < 0] = 0
                        xy_min = (int(bbox[0]), int(bbox[1]))
                        xy_max = (int(bbox[2]), int(bbox[3]))
                        # Display detection's BB, label and confidence on the frame
                        cv2.rectangle(manip_frame, xy_min , xy_max, (255, 0, 0), 2)
                        cv2.putText(manip_frame, class_name, (xy_min[0] + 10, xy_min[1] + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                        cv2.putText(manip_frame, f"{int(score * 100)}%", (xy_min[0] + 10, xy_min[1] + 40), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
            
        in_nn = q_nn.get()

        # read output
        area = np.array(in_nn.getLayerFp16("drive_area_seg")).reshape((1, 2, NN_HEIGHT, NN_WIDTH))
        lines = np.array(in_nn.getLayerFp16("lane_line_seg")).reshape((1, 2, NN_HEIGHT, NN_WIDTH))
        dets = np.array(in_nn.getLayerFp16("det_out")).reshape((1, 6300, 6))

        # generate and append density map
        boxes = np.array(non_max_suppression(dets, CONFIDENCE_THRESHOLD, IOU_THRESHOLD)[0])
        show_boxes(manip_frame, boxes)
        show_masks(manip_frame, area, lines)

        # show fps and predicted count
        color_black, color_white = (0,0,0), (255, 255, 255)
        label_fps = "Fps: {:.2f}".format(fps)
        (w1, h1), _ = cv2.getTextSize(label_fps, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)
        cv2.rectangle(manip_frame, (0,manip_frame.shape[0]-h1-6), (w1 + 2, manip_frame.shape[0]), color_white, -1)
        cv2.putText(manip_frame, label_fps, (2, manip_frame.shape[0] - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, color_black)

        cv2.imshow("Predict count", manip_frame)

        # FPS counter
        counter += 1
        current_time = time.monotonic()
        if (current_time - startTime) > 1:
            fps = counter / (current_time - startTime)
            counter = 0
            startTime = current_time

        if cv2.waitKey(1) == ord('q'):
            break
