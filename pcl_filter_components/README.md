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
