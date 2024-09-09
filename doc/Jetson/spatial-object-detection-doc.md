[retour à l'arborescence de la doc](../README.md)
# Spatial Object Detection Documentation

## Table of Contents
- [Spatial Object Detection Documentation](#spatial-object-detection-documentation)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Setup](#setup)
  - [Main Components](#main-components)
  - [Object Representation](#object-representation)
  - [Pipeline Configuration](#pipeline-configuration)
  - [Main Loop](#main-loop)
  - [Data Processing](#data-processing)
  - [Output](#output)
  - [Functions and Classes](#functions-and-classes)

## Introduction

This program implements spatial object detection using the DepthAI library and OpenCV. It processes video input from a stereo camera setup to detect objects and their 3D spatial coordinates.

## Setup

The application uses the following main dependencies:
- OpenCV (cv2)
- DepthAI (dai)
- NumPy
- Serial

To set up the device:

1. Ensure the DepthAI model blob file is available
2. Configure the serial port for UART communication
3. Set up the DepthAI pipeline

## Main Components

- DepthAI Pipeline: Configures the data flow for camera input and neural network inference
- MobileNet-SSD: Neural network for object detection
- Stereo Depth: Calculates depth information from stereo camera input
- UART Communication: Sends detected object data via serial port

## Object Representation

Objects are represented by the `ObjetSpatial` class, which includes:
- 3D coordinates (x, y, z)
- Object type
- Method for formatted string representation

## Pipeline Configuration

The DepthAI pipeline is set up with the following components:
- Color Camera
- Mono Cameras (Left and Right)
- Stereo Depth
- Spatial Detection Network (MobileNet-SSD)

## Main Loop

The main loop continuously:
1. Retrieves frames from the camera
2. Processes depth information
3. Runs object detection
4. Formats and sends object data via UART

## Data Processing

- Depth frame processing: Normalizes and color-maps depth information
- Object detection: Applies MobileNet-SSD to detect objects in the scene
- Spatial calculation: Determines 3D coordinates of detected objects

## Output

- UART: Sends formatted object data (type and 3D coordinates)
- Visual (optional): Displays color-mapped depth frame and detection results

## Functions and Classes

### Class: `ObjetSpatial`
- Represents a detected object with spatial coordinates
- Methods:
  - `__init__(self, x, y, z, type_objet)`: Initialize object
  - `__repr__(self)`: String representation
  - `sendingformat(self)`: Formatted string for UART transmission

### Main Script Functions:
- Pipeline setup and configuration
- Camera and neural network initialization
- Main processing loop
  - Frame acquisition
  - Depth processing
  - Object detection
  - Data formatting and transmission

This documentation provides an overview of the main components and functionalities of the Spatial Object Detection program. For more detailed information on each function or component, refer to the inline comments in the source code.

[retour à l'arborescence de la doc](../README.md)