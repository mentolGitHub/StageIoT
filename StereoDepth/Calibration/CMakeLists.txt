cmake_minimum_required(VERSION 3.0.0)
project(stereoPipeline VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 14)
SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++14 -pthread -O3 -Wall")

# find_package(Spinnaker REQUIRED)


# include_directories(~/../../opt/spinnaker/src)
# include_directories(/opt/spinnaker/include)

add_executable(grabStereoImages grabStereoImages.cpp)


add_library(spinnaker STATIC IMPORTED)
set_target_properties(spinnaker PROPERTIES IMPORTED_LOCATION /opt/spinnaker/lib/libSpinnaker.so.2)
set_target_properties(spinnaker PROPERTIES INTERFACE_INCLUDE_DIRECTORIES /opt/spinnaker/include)

target_link_libraries(grabStereoImages spinnaker)
# install(TARGETS pthread_task DESTINATION ${CMAKE_INSTALL_PREFIX})
# target_link_libraries(stereoImageAcquisition )
