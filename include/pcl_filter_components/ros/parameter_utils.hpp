// Copyright 2026 Maik Knof
// SPDX-License-Identifier: Apache-2.0

#ifndef PCL_FILTER_COMPONENTS__ROS__PARAMETER_UTILS_HPP_
#define PCL_FILTER_COMPONENTS__ROS__PARAMETER_UTILS_HPP_

#include <string>

#include <rclcpp_lifecycle/lifecycle_node.hpp>

namespace pcl_filter_components::ros
{

template <typename T>
void declareParameterIfNotDeclared(
  rclcpp_lifecycle::LifecycleNode & node,
  const std::string & name,
  const T & default_value)
{
  if (!node.has_parameter(name)) {
    node.declare_parameter<T>(name, default_value);
  }
}

template <typename T>
T getParameter(
  const rclcpp_lifecycle::LifecycleNode & node,
  const std::string & name)
{
  return node.get_parameter(name).get_value<T>();
}

}  // namespace pcl_filter_components::ros

#endif  // PCL_FILTER_COMPONENTS__ROS__PARAMETER_UTILS_HPP_
