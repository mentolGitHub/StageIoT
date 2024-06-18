set(CUDA_USE_STATIC_CUDA_RUNTIME OFF)

cmake_minimum_required(VERSION 3.0.0)
project(stereoPipeline VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -O3 -Wall")

find_package(OpenCV REQUIRED)
find_package(CUDA REQUIRED)

set(
    CUDA_NVCC_FLAGS
    ${CUDA_NVCC_FLAGS};
    -O3 -lineinfo
    -gencode=arch=compute_62,code=sm_62
    -gencode=arch=compute_53,code=sm_53
    )

include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(../libSGM/include)
# include_directories(../libSGM/src)
# include_directories(../benchmark/build/include)
# include_directories(../../../benchmark/include/benchmark)

add_library(spinnaker STATIC IMPORTED)
set_target_properties(spinnaker PROPERTIES IMPORTED_LOCATION /opt/spinnaker/lib/libSpinnaker.so.2)
set_target_properties(spinnaker PROPERTIES INTERFACE_INCLUDE_DIRECTORIES /opt/spinnaker/include)

#add_library(sgm STATIC IMPORTED)
#set_target_properties(sgm PROPERTIES IMPORTED_LOCATION /home/nvidia/libSGM/build/src/libsgm.so)
#set_target_properties(sgm PROPERTIES INTERFACE_INCLUDE_DIRECTORIES /home/nvidia/libSGM/include)

add_library(stereoPipeline stereoPipeline.cpp)
target_link_libraries(stereoPipeline ${OpenCV_LIBS})

add_executable(live_disparity live_disparity.cpp)
target_link_libraries(live_disparity stereoPipeline spinnaker ${OpenCV_LIBS})



