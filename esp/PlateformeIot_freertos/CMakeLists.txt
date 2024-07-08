cmake_minimum_required(VERSION 3.16.0)
include($ENV{IDF_PATH}/tools/cmake/project.cmake)
project(PlateformeIot_freertos)
idf_component_register(SRCS "main.cpp"
                       INCLUDE_DIRS "."
                       REQUIRES bt nvs_flash)
