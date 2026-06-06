# Copyright 2026 Maik Knof
# SPDX-License-Identifier: Apache-2.0

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

import os


def generate_launch_description():
    package_share = get_package_share_directory("pcl_filter_factory")
    parameters_file = os.path.join(package_share, "config", "filters.yaml")

    return LaunchDescription([
        ComposableNodeContainer(
            name="pcl_filter_container",
            namespace="",
            package="rclcpp_components",
            executable="component_container_mt",
            composable_node_descriptions=[
                ComposableNode(
                    package="pcl_filter_xyzi",
                    plugin="pcl_filter_xyzi::VoxelGridXYZIComponent",
                    name="voxel_grid_filter",
                    parameters=[parameters_file],
                    extra_arguments=[{"use_intra_process_comms": True}],
                ),
                ComposableNode(
                    package="pcl_filter_xyzi",
                    plugin="pcl_filter_xyzi::PassThroughXYZIComponent",
                    name="passthrough_filter",
                    parameters=[parameters_file],
                    extra_arguments=[{"use_intra_process_comms": True}],
                ),
                ComposableNode(
                    package="pcl_filter_xyzi",
                    plugin="pcl_filter_xyzi::CropBoxXYZIComponent",
                    name="crop_box_filter",
                    parameters=[parameters_file],
                    extra_arguments=[{"use_intra_process_comms": True}],
                ),
            ],
            output="screen",
        )
    ])
