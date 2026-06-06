# pcl_filter_components

`pcl_filter_components` provides reusable, templated, header-only PCL filters for
`pcl::PointCloud<PointT>` and exposes `pcl::PointXYZI` variants as ROS 2
lifecycle components.

The ROS wire type stays `sensor_msgs/msg/PointCloud2`. Internally, the
components use an `rclcpp::TypeAdapter` to receive and publish stamped, typed
PCL clouds while preserving the original message header.

The components use `std::unique_ptr` subscription callbacks and publishing for
efficient intra-process communication. True zero-copy behavior only applies when
the filters are composed into the same process with intra-process communication
enabled; inter-process communication still serializes as `sensor_msgs/msg/PointCloud2`.
