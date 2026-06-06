# Copyright 2026 Maik Knof
# SPDX-License-Identifier: Apache-2.0

from pathlib import Path

from ament_index_python.packages import get_package_prefix, get_package_share_directory

from pcl_filter_editor.filter_discovery import discover_filters


def test_discovery_reads_filter_and_type_adapter_exports() -> None:
    discovery = discover_filters()

    filters = {(item.package, item.filter): item for item in discovery.filters}
    for package, suffix, point_type in (
        ("pcl_filter_xyz", "XYZ", "PointXYZ"),
        ("pcl_filter_xyzi", "XYZI", "PointXYZI"),
        ("pcl_filter_xyzrgb", "XYZRGB", "PointXYZRGB"),
        ("pcl_filter_xyzrgba", "XYZRGBA", "PointXYZRGBA"),
    ):
        assert (package, f"VoxelGrid{suffix}") in filters
        assert (package, f"PointCloudMerger{suffix}") in filters
        voxel = filters[(package, f"VoxelGrid{suffix}")]
        assert voxel.component_class == f"{package}::VoxelGrid{suffix}Component"
        assert voxel.input_type == point_type
        assert voxel.output_type == f"{point_type},PointIndices"
        merger = filters[(package, f"PointCloudMerger{suffix}")]
        assert merger.input_type == f"{point_type},{point_type}"
        assert merger.output_type == point_type

    voxel = filters[("pcl_filter_xyzi", "VoxelGridXYZI")]
    assert voxel.component_class == "pcl_filter_xyzi::VoxelGridXYZIComponent"

    types = {(item.package, item.point_type): item for item in discovery.types}
    assert types[("pcl_filter_xyz", "PointXYZ")].type_adapter == "pcl_filter_xyz::ros::PclCloudAdapterPointXYZ"
    assert types[("pcl_filter_xyzi", "PointXYZI")].message_type == "sensor_msgs/msg/PointCloud2"
    assert (
        types[("pcl_filter_xyzi", "PointXYZI")].type_adapter
        == "pcl_filter_xyzi::ros::PclCloudAdapterPointXYZI"
    )
    assert (
        types[("pcl_filter_xyzrgb", "PointXYZRGB")].type_adapter
        == "pcl_filter_xyzrgb::ros::PclCloudAdapterPointXYZRGB"
    )
    assert (
        types[("pcl_filter_xyzrgba", "PointXYZRGBA")].type_adapter
        == "pcl_filter_xyzrgba::ros::PclCloudAdapterPointXYZRGBA"
    )
    assert (
        types[("pcl_filter_type_adapters", "PointNormal")].type_adapter
        == "pcl_filter_type_adapters::ros::PclNormalCloudAdapter"
    )
    assert types[("pcl_filter_type_adapters", "PointIndices")].message_type == "pcl_msgs/msg/PointIndices"


def test_components_register_in_rclcpp_components_index() -> None:
    prefix = Path(get_package_prefix("pcl_filter_xyzi"))
    resource = (
        prefix
        / "share"
        / "ament_index"
        / "resource_index"
        / "rclcpp_components"
        / "pcl_filter_xyzi"
    )
    registered = resource.read_text(encoding="utf-8")

    assert "pcl_filter_xyzi::VoxelGridXYZIComponent" in registered
    assert "pcl_filter_xyzi::PassThroughXYZIComponent" in registered
    assert "pcl_filter_xyzi::CropBoxXYZIComponent" in registered
    assert "pcl_filter_xyzi::PointCloudMergerXYZIComponent" in registered


def test_factory_installs_example_pipeline() -> None:
    example = Path(get_package_share_directory("pcl_filter_factory")) / "config" / "example_pipeline.yaml"
    text = example.read_text(encoding="utf-8")

    assert "package: pcl_filter_xyzi" in text
    assert "component_class: pcl_filter_xyzi::VoxelGridXYZIComponent" in text
