// Copyright 2026 Maik Knof
// SPDX-License-Identifier: Apache-2.0

#include <rclcpp_components/register_node_macro.hpp>
#include <rclcpp_lifecycle/lifecycle_node.hpp>

#include <string>

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

class ShmKeysComponent : public TestLifecycleComponent
{
public:
  explicit ShmKeysComponent(const rclcpp::NodeOptions & options)
  : TestLifecycleComponent(options)
  {
    this->declare_parameter<std::string>("shm_key.global_map", "global_map");
    this->declare_parameter<std::string>("shm_key.pose_cache", "pose_cache");
  }

  CallbackReturn on_configure(const rclcpp_lifecycle::State &) override
  {
    if (this->get_parameter("shm_key.global_map").as_string() != "slam/global_map") {
      return CallbackReturn::FAILURE;
    }
    if (this->get_parameter("shm_key.pose_cache").as_string() != "pose_cache") {
      return CallbackReturn::FAILURE;
    }
    return CallbackReturn::SUCCESS;
  }
};

}  // namespace filter_component_factory

RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::CropBoxXYZIComponent)
RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::PointCloudMergerXYZIComponent)
RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::VoxelGridXYZIComponent)
RCLCPP_COMPONENTS_REGISTER_NODE(filter_component_factory::ShmKeysComponent)
