#include "stereoPipeline.hpp"
#include "opencv2/calib3d/calib3d.hpp"
#include "opencv2/imgproc.hpp"
#include "opencv2/imgcodecs.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/core/utility.hpp"
#include "opencv2/cudaimgproc.hpp"
#include <opencv2/cudawarping.hpp>
#include <opencv2/cudaarithm.hpp>
// #include <benchmark/benchmark.h>
// #include <libsgm.h>
#include <iostream>
#include <sstream>
#include <unistd.h>
using namespace std;

stereoPipeline::stereoPipeline()
{
}

stereoPipeline::~stereoPipeline()
{
}

void stereoPipeline::CPU_getCameraParameters(std::string intrinsicsFile, std::string extrinsicsFile)
{
    cv::FileStorage ymlFile;
    ymlFile.open(intrinsicsFile, cv::FileStorage::READ);
    if (!ymlFile.isOpened())
    {
        printf("Failed to open intrinsics file \n");
    }
    ymlFile["M1"] >> M1;
    ymlFile["D1"] >> D1;
    ymlFile["M2"] >> M2;
    ymlFile["D2"] >> D2;

    ymlFile.open(extrinsicsFile, cv::FileStorage::READ);
    if (!ymlFile.isOpened())
    {
        printf("Failed to open extrinsics file \n");
    }
    ymlFile["R"] >> R;
    ymlFile["T"] >> T;
}
void stereoPipeline::CPU_computeRemapMatrix(cv::Mat imgL, cv::Mat imgR)
{
    cv::Mat temp_map11, temp_map12, temp_map21, temp_map22;
    stereoRectify(M1, D1, M2, D2, imgL.size(), R, T, R1, R2, P1, P2, Q, cv::CALIB_ZERO_DISPARITY, -1, imgL.size(), &roi1, &roi2);
    // initUndistortRectifyMap(M1, D1, R1, P1, imgL->size(), CV_8U, map11, map12);
    // initUndistortRectifyMap(M2, D2, R2, P2, imgL->size(), CV_8U, map21, map22);

    initUndistortRectifyMap(M1, D1, R1, P1, imgL.size(), CV_32FC1, temp_map11, temp_map12);
    initUndistortRectifyMap(M2, D2, R2, P2, imgL.size(), CV_32FC1, temp_map21, temp_map22);
    cout<<"remap made"<<endl;
    GPU_Q.upload(Q);
    cout<<Q;
    cout<<"Q uploaded"<<endl;

    GPU_map11.upload(temp_map11);
    GPU_map12.upload(temp_map12);
    GPU_map21.upload(temp_map21);
    GPU_map22.upload(temp_map22);
}

void stereoPipeline::GPU_initLBM(int WindowSize, int NumOfDisparity)
{
    BlockSize = WindowSize;
    MaxDisparity = NumOfDisparity;

    GPU_bm = cv::cuda::createStereoBM(NumOfDisparity, WindowSize);

    BlockSize = WindowSize;
    MaxDisparity = NumOfDisparity;
    // GPU_bm->setPreFilterType(cv::StereoBM::PREFILTER_XSOBEL );
    //GPU_bm->setUsePrefilter(true);
    //GPU_bm->setPreFilterSize(31);
    // GPU_bm->setPreFilterCap(11);
    GPU_bm->setBlockSize(BlockSize);
    GPU_bm->setMinDisparity(0);
    GPU_bm->setNumDisparities(MaxDisparity);
}

void stereoPipeline::GPU_initSGBM(int minDisparity, int WindowSize, int NumOfDisparity)
{
    BlockSize = WindowSize;
    MaxDisparity = NumOfDisparity;
    // GPU_sgbm = cv::cuda::createStereoSGM(0, NumOfDisparity, 80, 200, 5, cv::cuda::StereoSGM::MODE_HH );
    GPU_sgbm = cv::cuda::createStereoSGM(minDisparity, NumOfDisparity, 10, 120, 5, cv::cuda::StereoSGM::MODE_HH );
    GPU_sgbm->setBlockSize(BlockSize);
    // GPU_sgbm->setP1(1000);
    // GPU_sgbm->setP2(4000);
    GPU_sgbm->setUniquenessRatio(10);
    GPU_sgbm->setSpeckleRange(4);
    GPU_sgbm->setSpeckleWindowSize(200);
    // GPU_sgbm->setMinDisparity(0);
    // GPU_sgbm->setNumDisparities(MaxDisparity);
    // cout<<"initialization done!";

    // GPU_sgbm = cv::cuda::createStereoSGM(0, MaxDisparity, 9, P1, P2, 10);

}
void stereoPipeline::GPU_initBP(int NumOfDisparity, int NumOfIterators, int NumOfLevels)
{
    GPU_bp = cv::cuda::createStereoBeliefPropagation(NumOfDisparity);
    GPU_bp->setNumIters(NumOfIterators);
    GPU_bp->setNumLevels(NumOfLevels);
}
void stereoPipeline::GPU_initCSBP(int NumOfDisparity, int NumOfIterators, int NumOfLevels)
{
    GPU_csbp = cv::cuda::createStereoConstantSpaceBP(MaxDisparity);
    GPU_bp->setNumIters(NumOfIterators);
    GPU_bp->setNumLevels(NumOfLevels);
}


cv::cuda::GpuMat getActualDisparity(cv::cuda::GpuMat disparity)
{
    cv::cuda::GpuMat pixel;
    cv::cuda::GpuMat fraction;
    cv::cuda::GpuMat actualDisparity;

    cv::cuda::divide(disparity, 16, pixel);
    cv::cuda::divide(disparity, 16, fraction);
    cv::cuda::add(pixel, fraction, actualDisparity);

    return actualDisparity;
}



cv::Mat stereoPipeline::GPU_SGBM(cv::Mat *imgL, cv::Mat *imgR, cv::Mat *rectifiedL, cv::Mat *rectifiedR)
{

    cv::cvtColor(*imgL, temp_imgL, 6);
    cv::cvtColor(*imgR, temp_imgR, 6);

    GPU_imgL.upload(temp_imgL, leftStream);
    GPU_imgR.upload(temp_imgR, rightStream);

    cv::cuda::remap(GPU_imgL, imgL_r, GPU_map11, GPU_map12, cv::INTER_LINEAR, 0, 0, leftStream);
    cv::cuda::remap(GPU_imgR, imgR_r, GPU_map21, GPU_map22, cv::INTER_LINEAR, 0, 0, rightStream);

    // cv::cuda::equalizeHist(imgL_r, imgL_r, leftStream);
    // cv::cuda::equalizeHist(imgR_r, imgR_r, rightStream);

    imgL_r.download(*rectifiedL);
    imgR_r.download(*rectifiedR);

    GPU_sgbm->compute(imgL_r, imgR_r, GPU_disp, rightStream);
    GPU_disp.download(CPU_disp_SGBM);

    return CPU_disp_SGBM;
}

cv::Mat stereoPipeline::GPU_LBM(cv::Mat *imgL, cv::Mat *imgR, cv::Mat *rectifiedL, cv::Mat *rectifiedR)
{

    cv::cvtColor(*imgL, temp_imgL, 6);
    cv::cvtColor(*imgR, temp_imgR, 6);

    GPU_imgL.upload(temp_imgL, leftStream);
    GPU_imgR.upload(temp_imgR, rightStream);

    cv::cuda::remap(GPU_imgL, imgL_r, GPU_map11, GPU_map12, cv::INTER_LINEAR, 0, 0, leftStream);
    cv::cuda::remap(GPU_imgR, imgR_r, GPU_map21, GPU_map22, cv::INTER_LINEAR, 0, 0, rightStream);

    cv::cuda::equalizeHist(imgL_r, imgL_r, leftStream);
    cv::cuda::equalizeHist(imgR_r, imgR_r, rightStream);

    imgL_r.download(*rectifiedL);
    imgR_r.download(*rectifiedR);
    cout<<"imgR_r size: "<<imgR_r.size()<<endl;

    GPU_bm->compute(imgL_r, imgR_r, GPU_disp, rightStream);

    cv::cuda::GpuMat Norm_disp;

    GPU_disp.convertTo(Norm_disp, CV_8UC1, 256. / MaxDisparity);
    Norm_disp.download(CPU_disp_LBM);
    return CPU_disp_LBM;
}

cv::Mat stereoPipeline::GPU_BP(cv::Mat *imgL, cv::Mat *imgR)
{

    cout<<"starting BP"<<endl;
    cv::cvtColor(*imgL, temp_imgL, 6);
    cv::cvtColor(*imgR, temp_imgR, 6);
    cout<<"color convert done"<<endl;

    GPU_imgL.upload(temp_imgL, leftStream);
    GPU_imgR.upload(temp_imgR, rightStream);
    cout<<"upload done"<<endl;
/*
    (*imgL).convertTo(*imgL, CV_8U, 0.00390625);
    (*imgR).convertTo(*imgR, CV_8U, 0.00390625);

    GPU_imgL.upload(*imgL);
    GPU_imgR.upload(*imgR);
*/
    cv::cuda::remap(GPU_imgL, GPU_imgL, map11, map12, cv::INTER_LINEAR, 0, 0, leftStream);
    cv::cuda::remap(GPU_imgR, GPU_imgR, map21, map22, cv::INTER_LINEAR, 0, 0, rightStream);
    cout<<"remap done"<<endl;

    cv::Mat CPU_disp_BP((*imgL).size(), CV_8U);
    cv::cuda::GpuMat GPU_disp_BP((*imgL).size(), CV_8U);

    GPU_bp->compute(GPU_imgL, GPU_imgR, GPU_disp_BP, rightStream);
    cout<<"compute done"<<endl;

    GPU_disp_BP.download(CPU_disp_BP);

    return CPU_disp_BP;
}
cv::Mat stereoPipeline::GPU_CSBP(cv::Mat *imgL, cv::Mat *imgR)
{
    cout<<"starting CSBP"<<endl;
    GPU_imgL.upload(*imgL);
    GPU_imgR.upload(*imgR);
    cout<<"upload done"<<endl;

    cv::Mat CPU_disp_CSBP((*imgL).size(), CV_8U);
    cv::cuda::GpuMat GPU_disp((*imgL).size(), CV_8U);
    cout<<"starting CSBP"<<endl;

    cv::cuda::remap(GPU_imgL, GPU_imgL, map11, map12, cv::INTER_LINEAR, 0, 0, leftStream);
    cv::cuda::remap(GPU_imgR, GPU_imgR, map21, map22, cv::INTER_LINEAR, 0, 0, rightStream);

    GPU_csbp->compute(GPU_imgL, GPU_imgR, GPU_disp, rightStream);

    GPU_disp.download(CPU_disp_CSBP);
    return CPU_disp_CSBP;
}
