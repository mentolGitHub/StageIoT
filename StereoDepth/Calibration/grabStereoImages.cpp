#include "Spinnaker.h"
#include "SpinGenApi/SpinnakerGenApi.h"
#include <iostream>
#include <sstream>
#include <stdlib.h>

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
        master->TriggerSoftware.Execute();       
        masterImage = master->GetNextImage(1000);
        slaveImage = slave->GetNextImage(1000);
    }
    catch (Spinnaker::Exception& e)
    {
        cout << "Error: " << e.what() << endl;
        result = -1;
    }
    return result;
}

int main(int argc, char** argv)
{
    int nImages = 100;
    if(argc > 1)
        nImages = atoi(argv[1]);

    int result = 0;
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


// uncomment to see the serial numbers of the cameras

/*
    for (unsigned int i = 0; i < numCameras; i++)
    {
        // Select camera
        auto pCam = camList.GetByIndex(i);
        INodeMap& nodeMapTLDevice = pCam->GetTLDeviceNodeMap();

        // Retrieve device serial number for filename
        CStringPtr ptrStringSerial = pCam->GetTLDeviceNodeMap().GetNode("DeviceSerialNumber");

        std::string serialNumber = "";

        if (IsAvailable(ptrStringSerial) && IsReadable(ptrStringSerial))
        {
            serialNumber = ptrStringSerial->GetValue();
        }
        cout<<serialNumber<<endl;
    }

*/



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

// Uncomment to check if the cameras were read okay
/*
        CStringPtr ptrStringSerialMaster = master->GetTLDeviceNodeMap().GetNode("DeviceSerialNumber");
        CStringPtr ptrStringSerialSlave = slave->GetTLDeviceNodeMap().GetNode("DeviceSerialNumber");

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
*/


    ImagePtr pResultImageMaster = nullptr;
    ImagePtr pResultImageSlave = nullptr;



for(int i = 0; i < nImages; i++)
{
    cout<<"Capturing image"<< (i+1)<<endl;
    // sleep(1.0);
    ostringstream filename_left;
    ostringstream filename_right;
    StereoCapture(master, pResultImageMaster, slave, pResultImageSlave);
    filename_left << "../images/left/left" << i << ".png";
    filename_right << "../images/right/right" << i << ".png";
    // pResultImageMaster->Save("left.png");
    // pResultImageSlave->Save("right.png");
    pResultImageMaster->Save(filename_left.str().c_str());
    pResultImageSlave->Save(filename_right.str().c_str());
}

    ImagePtr convertedImageMaster = pResultImageMaster->Convert(PixelFormat_Mono8);
    ImagePtr convertedImageSlave = pResultImageSlave->Convert(PixelFormat_Mono8);

    convertedImageMaster->Save("master.png");
    convertedImageSlave->Save("slave.png");
    // Release images
    pResultImageMaster->Release();
    pResultImageSlave->Release();

    // Clear camera list before releasing system
    camList.Clear();
    // Release system
    system->ReleaseInstance();

    slave->EndAcquisition();
    master->EndAcquisition();
    slave->DeInit();
    master->DeInit();

    cout << endl << "Done! Press Enter to exit..." << endl;
    getchar();
    return result;
}
