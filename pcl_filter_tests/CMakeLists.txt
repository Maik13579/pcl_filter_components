cmake_minimum_required(VERSION 3.8)
project(pcl_filter_tests)

find_package(ament_cmake REQUIRED)

if(BUILD_TESTING)
  find_package(ament_cmake_pytest REQUIRED)

  ament_add_pytest_test(test_discovery test/test_discovery.py)
endif()

ament_package()
