#!/usr/bin/env python3

import cv2
import depthai as dai
import numpy as np

# Closer-in minimum depth, disparity range is doubled (from 95 to 190):
extended_disparity = True
# Better accuracy for longer distance, fractional disparity 32-levels:
subpixel = False
# Better handling for occlusions:
lr_check = True

alpha = 0.5
rgbWeight=0.5
depthWeight=1-rgbWeight
# Create pipeline
pipeline = dai.Pipeline()
pipeline.setXLinkChunkSize(0)

# Define sources and outputs
cam_rgb = pipeline.createColorCamera()
cam_rgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
cam_rgb.setInterleaved(True)
cam_rgb.setFps(60)

monoLeft = pipeline.create(dai.node.MonoCamera)
monoRight = pipeline.create(dai.node.MonoCamera)
depth = pipeline.create(dai.node.StereoDepth)
xout = pipeline.create(dai.node.XLinkOut)

xout.setStreamName("disparity")

# Properties
monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoLeft.setBoardSocket(dai.CameraBoardSocket.CAM_B)
monoLeft.setCamera("left")
monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
monoRight.setCamera("right")
monoRight.setBoardSocket(dai.CameraBoardSocket.CAM_C)

# Create a node that will produce the depth map (using disparity output as it's easier to visualize depth this way)
depth.setDefaultProfilePreset(dai.node.StereoDepth.PresetMode.HIGH_DENSITY)
# Options: MEDIAN_OFF, KERNEL_3x3, KERNEL_5x5, KERNEL_7x7 (default)
# depth.initialConfig.setMedianFilter(dai.MedianFilter.KERNEL_7x7)
depth.setRectifyEdgeFillColor(0)  
depth.setLeftRightCheck(lr_check)
depth.setExtendedDisparity(extended_disparity)
depth.setSubpixel(subpixel)

config = depth.initialConfig.get()
config.postProcessing.speckleFilter.enable = False
config.postProcessing.speckleFilter.speckleRange = 50
config.postProcessing.temporalFilter.enable = True
config.postProcessing.spatialFilter.enable = True
config.postProcessing.spatialFilter.holeFillingRadius = 2
config.postProcessing.spatialFilter.numIterations = 1
config.postProcessing.thresholdFilter.minRange = 400
config.postProcessing.thresholdFilter.maxRange = 15000
config.postProcessing.decimationFilter.decimationFactor = 3
depth.initialConfig.set(config)

rgbCamSocket = dai.CameraBoardSocket.CAM_A
depth.setLeftRightCheck(True)

depth.setDepthAlign(rgbCamSocket)


# Linking
monoLeft.out.link(depth.left)
monoRight.out.link(depth.right)
depth.disparity.link(xout.input)

xoutRectifRight = pipeline.create(dai.node.XLinkOut)
xoutRectifRight.setStreamName("rectifiedRight")
depth.rectifiedRight.link(xoutRectifRight.input)
# XLinkOut is a "way out" from the device. Any data you want to transfer to host need to be send via XLink
xout_rgb = pipeline.createXLinkOut()
# For the rgb camera output, we want the XLink stream to be named "rgb"
xout_rgb.setStreamName("rgb")
# Linking camera isp to XLink input, so that the frames will be sent to host
cam_rgb.isp.link(xout_rgb.input)



# Connect to device and start pipeline
with dai.Device(pipeline, maxUsbSpeed=dai.UsbSpeed.HIGH) as device:

    # Output queue will be used to get the disparity frames from the outputs defined above
    q = device.getOutputQueue(name="disparity", maxSize=4, blocking=False)
    q_fix = device.getOutputQueue(name="rectifiedRight", maxSize=8, blocking=False)
    
    q_rgb = device.getOutputQueue("rgb")

    rgb = None
    while True:
        inDisparity = q.tryGet()  # blocking call, will wait until a new data has arrived
        
        in_rgb = q_rgb.tryGet()
        in_fix = q_fix.tryGet()

        if in_rgb is not None:
            # If the packet from RGB camera is present, we're retrieving the frame in OpenCV format using getCvFrame
            rgb = in_rgb.getCvFrame()
        #cv2.imshow("disparity", frame)
            cv2.imshow("rgb", rgb)
        if inDisparity is not None:
            frame = inDisparity.getFrame()
            # Normalization for better visualization
            frame = (frame * (255 / depth.initialConfig.getMaxDisparity())).astype(np.uint8)
            # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
            #frame = cv2.applyColorMap(frame, cv2.COLORMAP_SUMMER)
            cv2.imshow("disparity_color", frame)
            framedepth = cv2.resize(frame, (1920,1080))

        if in_fix is not None:
            name = q_fix.getName()
            frame = in_fix.getCvFrame()
            cv2.imshow(name, frame)

        if rgb is not None and inDisparity is not None:
            blended = cv2.addWeighted(rgb, rgbWeight, framedepth, depthWeight, 0)
            blendedWindowName = "rgb-depth"
            cv2.namedWindow(blendedWindowName)
            cv2.imshow(blendedWindowName, blended)


        if cv2.waitKey(1) == ord('q'):
            break