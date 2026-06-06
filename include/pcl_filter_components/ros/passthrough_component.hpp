// Copyright 2026 Maik Knof
// SPDX-License-Identifier: Apache-2.0

#ifndef PCL_FILTER_COMPONENTS__ROS__PASSTHROUGH_COMPONENT_HPP_
#define PCL_FILTER_COMPONENTS__ROS__PASSTHROUGH_COMPONENT_HPP_

#include <string>

#include <rclcpp/rclcpp.hpp>

#include "pcl_filter_components/filters/passthrough_filter.hpp"
#include "pcl_filter_components/ros/optional_indices_output_component.hpp"
#include "pcl_filter_components/ros/parameter_utils.hpp"

namespace pcl_filter_components::ros
{

template <typename PointT>
class PassThroughComponent
  : public OptionalIndicesOutputComponent<PointT, filters::PassThroughFilter<PointT>>
{
public:
  explicit PassThroughComponent(const rclcpp::NodeOptions & options = rclcpp::NodeOptions())
  : OptionalIndicesOutputComponent<PointT, filters::PassThroughFilter<PointT>>(
      "passthrough_filter",
      options)
  {
    declareParameterIfNotDeclared(*this, "filter.field_name", std::string{"z"});
    declareParameterIfNotDeclared(*this, "filter.min_value", -1.0);
    declareParameterIfNotDeclared(*this, "filter.max_value", 2.0);
    declareParameterIfNotDeclared(*this, "filter.invert", false);
  }

protected:
  void configureFilter() override
  {
    typename filters::PassThroughFilter<PointT>::Params params;
    params.field_name = getParameter<std::string>(*this, "filter.field_name");
    params.min_value = getParameter<double>(*this, "filter.min_value");
    params.max_value = getParameter<double>(*this, "filter.max_value");
    params.invert = getParameter<bool>(*this, "filter.invert");
    this->filter_.configure(params);
  }
};

}  // namespace pcl_filter_components::ros

#endif  // PCL_FILTER_COMPONENTS__ROS__PASSTHROUGH_COMPONENT_HPP_
