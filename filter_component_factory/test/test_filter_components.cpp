// Copyright 2026 Maik Knof
// SPDX-License-Identifier: Apache-2.0

#include <rclcpp_components/register_node_macro.hpp>
#include <rclcpp_lifecycle/lifecycle_node.hpp>

namespace filter_component_factory
{

class TestLifecycleComponent : public rclcpp_lifecycle::LifecycleNode
{
public:
  explicit TestLifecycleComponent(const rclcpp::NodeOptions & options)
  : rclcpp_lifecycle::LifecycleNode("test_filter_component", options)
  {
  }

  CallbackReturn on_configure(const rclcpp_lifecycle::State &) override
  {
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_activate(const rclcpp_lifecycle::State &) override
  {
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_deactivate(const rclcpp_lifecycle::State &) override
  {
    return CallbackReturn::SUCCESS;
  }

  CallbackReturn on_cleanup(const rclcpp_lifecycle::State &) override
  {
    return CallbackReturn::SUCCESS;
  }
};

class CropBoxXYZIComponent : public TestLifecycleComponent
{
public:
  using TestLifecycleComponent::TestLifecycleComponent;
};

class PointCloudMergerXYZIComponent : public TestLifecycleComponent
{
public:
  using TestLifecycleComponent::TestLifecycleComponent;
};

class VoxelGridXYZIComponent : public TestLifecycleComponent
{
public:
  using TestLifecycleComponent::TestLifecycleComponent;
};

}  // namespace filter_component_factory

RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::CropBoxXYZIComponent)
RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::PointCloudMergerXYZIComponent)
RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::VoxelGridXYZIComponent)
