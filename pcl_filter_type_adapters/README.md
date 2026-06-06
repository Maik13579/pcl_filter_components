# pcl_filter_type_adapters

`pcl_filter_type_adapters` provides header-only `rclcpp::TypeAdapter`
definitions for stamped PCL clouds and PCL point indices.

This package also exports editor discovery metadata for common non-filter cloud
types:

- `PointNormal`
- `PointIndices`

Concrete point-type packages export named aliases and discovery metadata for
specific filtered cloud types. Packages that need typed PCL subscriptions or
publishers should depend on this package and include headers from
`pcl_filter_type_adapters/ros/...`.
