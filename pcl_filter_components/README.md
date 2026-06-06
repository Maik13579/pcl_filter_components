# pcl_filter_components

`pcl_filter_components` contains generic PCL filter algorithms and ROS component
templates.

Namespaces:

- `pcl_filter_components::filters` for algorithm templates.
- `pcl_filter_components::ros` for reusable ROS component templates.

This package does not instantiate or register concrete point-type components.
Concrete packages such as `pcl_filter_xyzi`, `pcl_filter_xyz`,
`pcl_filter_xyzrgb`, and `pcl_filter_xyzrgba` own the point-specific aliases,
metadata exports, and `rclcpp_components` registrations.

Single-cloud filters expose one `cloud` input and `cloud` plus `indices`
outputs. `filter.output_indices` selects whether optional-index filters publish
the filtered cloud or point indices. `PointCloudMergerComponent` exposes
`input_1` and `input_2` cloud inputs and one `cloud` output, using the shared
multi-port lifecycle base instead of owning subscriptions directly.
