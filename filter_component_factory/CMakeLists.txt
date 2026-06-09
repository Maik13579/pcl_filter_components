cmake_minimum_required(VERSION 3.8)
project(filter_component_factory)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_components REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(yaml_cpp_vendor REQUIRED)
find_package(yaml-cpp REQUIRED)

add_library(${PROJECT_NAME}_pipeline SHARED
  src/pipeline_graph.cpp
  src/pipeline_factory_node.cpp
)
target_include_directories(${PROJECT_NAME}_pipeline PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include/${PROJECT_NAME}>
)
target_link_libraries(${PROJECT_NAME}_pipeline yaml-cpp::yaml-cpp)
ament_target_dependencies(${PROJECT_NAME}_pipeline
  rclcpp
  rclcpp_components
  rclcpp_lifecycle
)

add_executable(filter_pipeline_factory src/pipeline_factory_main.cpp)
target_link_libraries(filter_pipeline_factory ${PROJECT_NAME}_pipeline)
ament_target_dependencies(filter_pipeline_factory
  rclcpp
)

install(TARGETS ${PROJECT_NAME}_pipeline filter_pipeline_factory
  EXPORT export_${PROJECT_NAME}
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION lib/${PROJECT_NAME}
)
install(DIRECTORY include/ DESTINATION include)
install(DIRECTORY config launch DESTINATION share/${PROJECT_NAME})

if(BUILD_TESTING)
  find_package(ament_cmake_gtest REQUIRED)

  add_library(test_filter_components SHARED
    test/test_filter_components.cpp
  )
  ament_target_dependencies(test_filter_components
    rclcpp
    rclcpp_components
    rclcpp_lifecycle
  )
  rclcpp_components_register_nodes(test_filter_components
    "filter_component_factory::CropBoxXYZIComponent"
    "filter_component_factory::PointCloudMergerXYZIComponent"
    "filter_component_factory::VoxelGridXYZIComponent"
  )
  install(TARGETS test_filter_components
    LIBRARY DESTINATION lib
  )

  ament_add_gtest(test_pipeline_graph test/test_pipeline_graph.cpp)
  target_include_directories(test_pipeline_graph PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
  )
  target_link_libraries(test_pipeline_graph ${PROJECT_NAME}_pipeline)

  ament_add_gtest(test_pipeline_factory test/test_pipeline_factory.cpp)
  target_include_directories(test_pipeline_factory PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
  )
  target_compile_definitions(test_pipeline_factory PRIVATE
    PROJECT_SOURCE_DIR="${CMAKE_CURRENT_SOURCE_DIR}"
  )
  target_link_libraries(test_pipeline_factory ${PROJECT_NAME}_pipeline)
  add_dependencies(test_pipeline_factory test_filter_components)
  ament_target_dependencies(test_pipeline_factory
    rclcpp
  )
  set_tests_properties(test_pipeline_factory PROPERTIES
    ENVIRONMENT
      "RMW_IMPLEMENTATION=rmw_fastrtps_cpp;ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST;ROS_LOG_DIR=/tmp/filter_component_factory_test_logs"
  )
endif()

ament_export_include_directories(include)
ament_export_targets(export_${PROJECT_NAME} HAS_LIBRARY_TARGET)
ament_export_dependencies(
  rclcpp
  rclcpp_components
  rclcpp_lifecycle
  yaml_cpp_vendor
  yaml-cpp
)
ament_package()
