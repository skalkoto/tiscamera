
include_directories("${CMAKE_SOURCE_DIR}/dependencies/catch")
include_directories("${CMAKE_SOURCE_DIR}/src/tcam-network")

add_executable(test-tcam-network main.cpp)

target_link_libraries(test-tcam-network tcam-network)

add_test(tcam-network test-tcam-network)
