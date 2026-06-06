# pcl_filter_base

`pcl_filter_base` contains reusable header-only ROS 2 infrastructure for PCL
filter components:

- lifecycle filter base class
- optional point-indices output base template
- parameter descriptor helpers

Headers use the `pcl_filter_base/...` include root and the
`pcl_filter_base::ros` namespace. Concrete filters and registered components live
in `pcl_filter_components`.
