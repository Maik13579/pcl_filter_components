# PCL Filter Pipeline

This repository contains sibling ROS 2 packages for reusable PCL point cloud
filter templates, concrete point-type instantiations, a YAML pipeline factory,
and an rqt graph editor.

## Packages

- [pcl_filter_type_adapters](pcl_filter_type_adapters/README.md): generic
  stamped PCL cloud and point-indices `rclcpp::TypeAdapter` templates. It also
  exports common non-filter helper types such as `PointNormal` and
  `PointIndices`.
- [pcl_filter_base](pcl_filter_base/README.md): reusable lifecycle component
  base classes and parameter descriptor helpers.
- [pcl_filter_components](pcl_filter_components/README.md): generic filter
  algorithms and component templates. It does not register concrete components.
- [pcl_filter_xyzi](pcl_filter_xyzi/README.md): `pcl::PointXYZI` type adapter
  aliases, filter metadata, and registered components.
- [pcl_filter_xyz](pcl_filter_xyz/README.md): `pcl::PointXYZ` type adapter
  aliases, filter metadata, and registered components.
- [pcl_filter_xyzrgb](pcl_filter_xyzrgb/README.md): `pcl::PointXYZRGB` type
  adapter aliases, filter metadata, and registered components.
- [pcl_filter_xyzrgba](pcl_filter_xyzrgba/README.md): `pcl::PointXYZRGBA` type
  adapter aliases, filter metadata, and registered components.
- [pcl_filter_factory](pcl_filter_factory/README.md): YAML graph parser,
  lifecycle factory node, and factory executable.
- [pcl_filter_editor](pcl_filter_editor/README.md): rqt editor and filter/type
  discovery code.
- [pcl_filter_tests](pcl_filter_tests/README.md): installed-system integration
  tests across the split packages.

## Architecture

The generic packages do not instantiate point-specific filter components:

```text
pcl_filter_type_adapters
  -> pcl_filter_base
    -> pcl_filter_components
      -> pcl_filter_xyzi / pcl_filter_xyz / pcl_filter_xyzrgb / pcl_filter_xyzrgba
        -> pcl_filter_factory
          -> pcl_filter_tests

pcl_filter_editor -> pcl_filter_tests
```

The editor discovers logical point types and filters from package export tags.
Concrete point-type packages own the cloud type alias, filter metadata, and
registered component classes for their point type. The generic type-adapter
package owns shared helper exports such as `PointIndices`.

Concrete packages export filters with:

```xml
<pcl_filter_component filter="VoxelGridXYZI" input="PointXYZI" output="PointXYZI,PointIndices"/>
```

Concrete packages export their cloud aliases with:

```xml
<pcl_filter_component
  type="PointXYZI"
  type_adapter="pcl_filter_xyzi::ros::PclCloudAdapterPointXYZI"
  message_type="sensor_msgs/msg/PointCloud2"/>
```

## Graph YAML

Pipelines are saved as YAML with editor layout, component identity, parameters,
QoS, synchronization settings, topics, ports, and edges. Filter nodes use the
concrete package and class explicitly:

```yaml
nodes:
  - type: filter
    name: VoxelGridXYZI_1
    package: pcl_filter_xyzi
    filter: VoxelGridXYZI
    component_class: pcl_filter_xyzi::VoxelGridXYZIComponent
    input_type: PointXYZI
    output_type: PointXYZI,PointIndices
```

Topic nodes are graph endpoints or intermediate bindings. The factory turns
topic nodes into topic remaps and loads only filter nodes as components.
