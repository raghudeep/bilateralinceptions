
find_package(CUDA REQUIRED)
find_package(OpenCV REQUIRED)

find_package(Boost COMPONENTS system filesystem REQUIRED)
include_directories(${Boost_INCLUDE_DIR})
link_directories(${Boost_LIBRARY_DIR})

include_directories(${CUDA_INCLUDE_DIRS})
include_directories(${OpenCV_INCLUDE_DIRS})

add_executable(compute_superpixels compute_superpixels.cpp)
target_link_libraries(compute_superpixels gSLICr_lib ${CUDA_LIBRARY} ${OpenCV_LIBS} ${Boost_LIBRARIES})
