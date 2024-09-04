#include "Spinnaker.h"
#include "SpinGenApi/SpinnakerGenApi.h"
#include <iostream>
#include <sstream>
#include <stdlib.h>

#include "opencv2/opencv.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include <opencv2/core/core.hpp>
#include "opencv2/core/utility.hpp"
#include <chrono>
// #include <libsgm.h>
// #include "imagePairReader.hpp"
#include "stereoPipeline.hpp"

using namespace Spinnaker;
using namespace Spinnaker::GenApi;
using namespace Spinnaker::GenICam;
using namespace std;

int StereoCapture(CameraPtr master, ImagePtr& masterImage, CameraPtr slave, ImagePtr& slaveImage)
{
    int result = 0;
    try    {
        // Execute software trigger
        if (!IsWritable(master->TriggerSoftware))
        {
            cout << "Unable to execute trigger..." << endl;
            return -1;
        }
        // cout<<"Before trigger"<<endl;
        master->TriggerSoftware.Execute();
        // cout<<"Before master image"<<endl;
        // Retrieve the next received image        
        masterImage = master->GetNextImage(1000);
        // cout<<"Before slave image"<<endl;
        slaveImage = slave->GetNextImage(1000);
        // cout<<"....Done...."<<endl;
    }
    catch (Spinnaker::Exception& e)
    {
        cout << "Error: " << e.what() << endl;
        result = -1;
    }
    return result;
}


int convertToMat(cv::Mat& cvImage, ImagePtr& convertedImage)
{

    int cvWidth = convertedImage->GetWidth(); // + convertedImage.GetXPadding();
    int cvHeight = convertedImage->GetHeight(); // + convertedImage.GetYPadding();

    cvImage = cv::Mat(cvHeight, cvWidth, CV_8UC3, convertedImage->GetData(), convertedImage->GetStride());

    return 0;

}

/*
void displayCameraInfo(CameraPtr *master, CameraPtr *slave)
{
    CStringPtr ptrStringSerialMaster = *master->GetTLDeviceNodeMap().GetNode("DeviceSerialNumber");
    CStringPtr ptrStringSerialSlave = *slave->GetTLDeviceNodeMap().GetNode("DeviceSerialNumber");

    std::string serialNumberMaster = "";
    std::string serialNumberSlave = "";

    if (IsAvailable(ptrStringSerialMaster) && IsReadable(ptrStringSerialMaster))
    {
        cout<<"Serial number for master is: "<<ptrStringSerialMaster->GetValue()<<endl;
    }
    else
    {
        cout<<"Not able to read Master"<<endl;
    }

    if (IsAvailable(ptrStringSerialSlave) && IsReadable(ptrStringSerialSlave))
    {
        cout<<"Serial number for master is: "<<ptrStringSerialSlave->GetValue()<<endl;
    }
    else
    {
        cout<<"Not able to read Slave"<<endl;
    }

    cout<<endl;
}

// set up master and slave (and sync them)
void setUpCameras(CameraPtr *master, CameraPtr *slave)
{
    
}
*/

static struct MouseObj
{
	int x, y;
	bool newClick;
} mouse;

void mouse_callback(int event, int x, int y, int flag, void *param)
{
	if (event == cv::EVENT_LBUTTONDOWN)
	{
		mouse.x = x;
		mouse.y = y;
		mouse.newClick = true;
	}
}

void color_map(cv::Mat& input, cv::Mat& SGBM_output, cv::Mat& dest, double focal_length, double baseline){

  int num_bar_w=100;
  int color_bar_w=50;
  int vline=20;

  cv::Mat win_mat(cv::Size(input.cols+num_bar_w+color_bar_w+vline, input.rows), CV_8UC3, cv::Scalar(255,255,255));

  //Input image to
  double Min, Max;
  cv::minMaxLoc(input, &Min, &Max);
  double dispMin, dispMax;
  cv::minMaxLoc(SGBM_output, &dispMin, &dispMax);

  if(Min < 1)
{ //cout<<"less than 1"<<endl;
      Min = 1;
}

  float depth = 0.0;
  std::stringstream streamDepth;
  std::string stringDepth;

  int levels = 8;
  double level_diff = (dispMax - dispMin)/levels;

  // input.convertTo(input,CV_8UC1,255.0/(Max-Min),-255.0*Min/(Max-Min));
  // input.convertTo(input, CV_8UC1);

  cv::Mat M;
  cv::applyColorMap(input, M, cv::COLORMAP_BONE);

  M.copyTo(win_mat(cv::Rect(  0, 0, input.cols, input.rows)));

  //Scale
  int disp;
  cv::Mat num_window(cv::Size(num_bar_w, input.rows), CV_8UC3, cv::Scalar(255,255,255));
  for(int i=0; i<=levels; i++){
      // int j=i*input.rows/levels;
      // disp = Min + (levels - i)*level_diff;
      disp = dispMin + i*level_diff;
      
      int pixel = disp / 16;  // integer part
      int fraction = disp % 16; // fractional part
      float dispVal = (float)pixel + (float)fraction / 16.0f;  // actual disparity
      if (dispVal < 0)
          dispVal = 0;

      depth = (focal_length*baseline / dispVal) / 1000.0;
      streamDepth.str(std::string());

      if(depth == -1.0)
          streamDepth<<"N/A";
      else
          streamDepth<<std::fixed<<std::setprecision(1)<<depth<<"m";
      stringDepth = streamDepth.str();

      cv::putText(num_window, stringDepth, cv::Point(5, i*(num_window.rows/levels)),cv::FONT_HERSHEY_SIMPLEX, 1 , cv::Scalar(0,0,0), 3 , 2 , false);
  }

  //color bar
  cv::Mat color_bar(cv::Size(color_bar_w, input.rows), CV_8UC3, cv::Scalar(255,255,255));
  cv::Mat cb;
  for(int i=0; i<color_bar.rows; i++){
    for(int j=0; j<color_bar_w; j++){
      int v=Min + (i*(Max - Min)/(color_bar.rows - 1));
      color_bar.at<cv::Vec3b>(i,j)=cv::Vec3b(v,v,v);
    }
  }

  color_bar.convertTo(color_bar, CV_8UC3);
  cv::applyColorMap(color_bar, cb, cv::COLORMAP_BONE);

  num_window.copyTo(win_mat(cv::Rect(input.cols+vline+color_bar_w, 0, num_bar_w, input.rows)));
  cb.copyTo(win_mat(cv::Rect(input.cols+vline, 0, color_bar_w, input.rows)));
  dest=win_mat.clone();
}


int main(int argc, char** argv)
{
    double magnificationFactor = 1;
    if(argc > 1)
        magnificationFactor = atof(argv[1]);

    int result = 0;
    bool resize = 0;

    // define new height and width. Preferably of the same aspect ratio of the original images
    int newHeight = 960;
    int newWidth = 1280;

    // get a list of cameras 
    SystemPtr system = System::GetInstance();
    CameraList camList = system->GetCameras();

    unsigned int numCameras = camList.GetSize();
    cout << "Number of cameras detected: " << numCameras << endl << endl;

    // Finish if there are no cameras
    if (numCameras != 2)
    {
        // Clear camera list before releasing system
        camList.Clear();
        // Release system
        system->ReleaseInstance();
        cout << "Incorrect numbers of cameras" << endl;
        cout << "Done! Press Enter to exit..." << endl;
        getchar();
        return -1;
    }

    // set the master and slave serial number here..
    CameraPtr master = camList.GetBySerial("22105702");
    CameraPtr slave = camList.GetBySerial("22105704");

    master->Init();
    slave->Init();

    // def setup_master
    master->TriggerSelector.SetValue(Spinnaker::TriggerSelectorEnums::TriggerSelector_FrameStart);
    master->TriggerSource.SetValue(Spinnaker::TriggerSourceEnums::TriggerSource_Software);
    master->TriggerMode.SetValue(Spinnaker::TriggerModeEnums::TriggerMode_On);
    master->LineSelector.SetValue(Spinnaker::LineSelectorEnums::LineSelector_Line3);
    master->LineMode.SetValue(Spinnaker::LineModeEnums::LineMode_Output);
    master->LineSource.SetValue(Spinnaker::LineSourceEnums::LineSource_ExposureActive);

    // def setup slave
    slave->TriggerSelector.SetValue(Spinnaker::TriggerSelectorEnums::TriggerSelector_FrameStart);
    slave->TriggerSource.SetValue(Spinnaker::TriggerSourceEnums::TriggerSource_Line2);
    slave->TriggerMode.SetValue(Spinnaker::TriggerModeEnums::TriggerMode_On);
    slave->LineSelector.SetValue(Spinnaker::LineSelectorEnums::LineSelector_Line2);
    slave->LineMode.SetValue(Spinnaker::LineModeEnums::LineMode_Input);
    slave->LineSource.SetValue(Spinnaker::LineSourceEnums::LineSource_ExposureActive);

    // set to newest only buffer handling mode.
    Spinnaker::GenApi::INodeMap& master_sNodeMap = master->GetTLStreamNodeMap();
    Spinnaker::GenApi::INodeMap& slave_sNodeMap = slave->GetTLStreamNodeMap();
    CEnumerationPtr master_ptrHandlingMode = master_sNodeMap.GetNode("StreamBufferHandlingMode");
    CEnumerationPtr slave_ptrHandlingMode = slave_sNodeMap.GetNode("StreamBufferHandlingMode");
    CEnumEntryPtr newest_only_buffer_handling_mode = master_ptrHandlingMode->GetEntryByName("NewestOnly");

    master_ptrHandlingMode->SetIntValue(newest_only_buffer_handling_mode->GetValue());
    slave_ptrHandlingMode->SetIntValue(newest_only_buffer_handling_mode->GetValue());

    // at this point you should have a working synchronized camera set
    // start slave first since you want it to get an image when master gets it... and it should't get an image if master doesn't trigger software.
    slave->BeginAcquisition();
    master->BeginAcquisition();

    // display information
    // displayCameraInfo(master, slave);

    // master and slave images
    ImagePtr pResultImageMaster = nullptr;
    ImagePtr pResultImageSlave = nullptr;
    ImagePtr convertedImageMaster = nullptr;
    ImagePtr convertedImageSlave = nullptr;


    // disparity code starts here....
    stereoPipeline stereo;
    cv::Mat imgL, imgR, rectifiedL, rectifiedR;
    cv::Mat DisparityMapSGBM;

    // loading extrincics and intrinsics files
    stereo.CPU_getCameraParameters();

    // capture a pair of in sync master and slave images
    StereoCapture(master, pResultImageMaster, slave, pResultImageSlave);

    // convert images to BGR format
    convertedImageMaster = pResultImageMaster->Convert(PixelFormat_BGR8);
    convertedImageSlave = pResultImageSlave->Convert(PixelFormat_BGR8);

    // convert Spinnaker images to OpenCv images
    convertToMat(imgL, convertedImageMaster);
    convertToMat(imgR, convertedImageSlave);

    double baseline = 120.0;
    double focal_length = 1720.0;
    if(resize)
    {
        focal_length = focal_length * newWidth/imgL.cols;

        cv::resize(imgL, imgL, cv::Size(newWidth, newHeight), cv::INTER_CUBIC);
        cv::resize(imgR, imgR, cv::Size(newWidth, newHeight), cv::INTER_CUBIC);
    }

    // settings to get distance
    cv::namedWindow("Depth Map", cv::WINDOW_NORMAL);
    cv::namedWindow("Left Camera feed", cv::WINDOW_NORMAL);
    cv::setMouseCallback("Depth Map", mouse_callback);

    // computer rectification paramters
    stereo.CPU_computeRemapMatrix(imgL, imgR);

    // define SGBM parameters
    int numDisparity = 128;
    stereo.GPU_initSGBM(0, 29, numDisparity);
    
    float depth = 0.0;
    std::stringstream streamDepth;
    std::string stringDepth;
    char c;
    auto start = std::chrono::high_resolution_clock::now();
    auto elapsed_seconds = std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::high_resolution_clock::now() - start);

    int pixel;
    int fraction;
    float dispVal;
    int count = 0;

    cv::Mat colorMap, colorOutput, Output, colorMapResized, imgLResized;
    bool updateDepth = true;

    //Ramp up pipeline;
    while (1 == 1)
    {
        start = std::chrono::high_resolution_clock::now();

        StereoCapture(master, pResultImageMaster, slave, pResultImageSlave);

        convertedImageMaster = pResultImageMaster->Convert(PixelFormat_BGR8);
        convertedImageSlave = pResultImageSlave->Convert(PixelFormat_BGR8);

        convertToMat(imgL, convertedImageMaster);
        convertToMat(imgR, convertedImageSlave);

        if(resize)
        {
            cv::resize(imgL, imgL, cv::Size(newWidth, newHeight), cv::INTER_CUBIC);
            cv::resize(imgR, imgR, cv::Size(newWidth, newHeight), cv::INTER_CUBIC);
        }

        // perform rectification
        DisparityMapSGBM = stereo.GPU_SGBM(&imgL, &imgR, &rectifiedL, &rectifiedR);

        cv::normalize(DisparityMapSGBM, Output, 1, 255, cv::NORM_MINMAX, CV_8UC1);

        if (count%20 == 0) // generate color map scale once only 20 frames for speed
        {
            color_map(Output, DisparityMapSGBM, colorMap, focal_length, baseline);
            count = 0;
        }
        else
        {
            cv::applyColorMap(Output, colorOutput, cv::COLORMAP_BONE);
            colorOutput.copyTo(colorMap(cv::Rect(  0, 0, Output.cols, Output.rows)));
        }

        count++;
        // color_map(Output, DisparityMapSGBM, colorMap);

        if(updateDepth)
        {
            streamDepth.str(std::string());
            if(depth == -1.0)
                streamDepth<<"N/A";
            else
                streamDepth<<std::fixed<<std::setprecision(2)<<depth<<"m";
            stringDepth = streamDepth.str();
            updateDepth = false;
        }


        if(magnificationFactor != 1)
        {
            cv::resize(colorMap, colorMapResized, cv::Size(ceil(colorMap.cols * magnificationFactor), ceil(colorMap.rows * magnificationFactor)));
            cv::resize(imgL, imgLResized, cv::Size(ceil(imgL.cols * magnificationFactor), ceil(imgL.rows * magnificationFactor)));
        }
        else
        {
            colorMapResized = colorMap.clone();
            imgLResized = imgL.clone();
        }
        cv::putText(colorMapResized, stringDepth, cv::Point2f(mouse.x, mouse.y), cv::FONT_HERSHEY_PLAIN, 2, cv::Scalar(255, 255, 0), 2, 4);
        cv::imshow("Depth Map", colorMapResized);
        // cv::imwrite("disparity.png", colorMap);
        // cv::imwrite("left.png", imgL);
        cv::imshow("Left Camera feed", imgLResized);

        c = (char)cv::waitKey(1);
        if(c==27)
        {
            cv::destroyAllWindows();
            break;
        }

        if (mouse.newClick)
        {
            mouse.newClick = false;
            pixel = DisparityMapSGBM.at<short>(mouse.y / magnificationFactor, mouse.x / magnificationFactor) / 16;  // integer part
            fraction = DisparityMapSGBM.at<short>(mouse.y / magnificationFactor, mouse.x / magnificationFactor) % 16; // fractional part
            dispVal = (float)pixel + (float)fraction / 16.0f;  // actual disparity
            if  (dispVal < 0)
                 dispVal = 0;

            if (fabs(dispVal) < 0.001)
                depth = -1.0f;
            else
                depth = (focal_length*baseline / dispVal) / 1000.0;
            updateDepth = true;
            cout<<depth<<endl;
        }

        elapsed_seconds = std::chrono::duration_cast<std::chrono::duration<double>>(std::chrono::high_resolution_clock::now() - start);
        std::cout<<elapsed_seconds.count()<<endl;
        
    }

    // Release images
    pResultImageMaster->Release();
    pResultImageSlave->Release();
    cout<<"Images released"<<endl;

    // end acquisition
    slave->EndAcquisition();
    master->EndAcquisition();
    slave->DeInit();
    master->DeInit();
    slave = nullptr;
    master = nullptr;
    cout<<"Acquisition ended"<<endl;

    // Clear camera list before releasing system
    camList.Clear();
    cout<<"Camera list cleared"<<endl;

    // Release system
    system->ReleaseInstance();

    return result;
}
