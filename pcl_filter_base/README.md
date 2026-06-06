# pcl_filter_base

`pcl_filter_base` contains reusable header-only ROS 2 infrastructure for PCL
filter components:

- lifecycle filter base class
- parameter descriptor helpers

Headers use the `pcl_filter_base/...` include root and the
`pcl_filter_base::ros` namespace. Concrete filters and registered components live
in `pcl_filter_components`.

Filter components declare input and output port descriptors. The base class
creates subscriptions, publishers, and synchronization state from those
descriptors during lifecycle configuration. Topic parameters use
`inputs.<port>.topic` and `outputs.<port>.topic`.

Derived components consume synchronized messages through typed accessors such as
`takeInput<AdapterT>("cloud")` and publish through
`publish<AdapterT>("cloud", message)`. Multi-input components additionally
declare `sync.policy`, `sync.queue_size`, and `sync.slop`.

## Creating a custom component

Custom components derive from `PclFilterComponentBase<PointT, FilterT>` and pass
compile-time input and output descriptor arrays into the base constructor. The
base uses those descriptors to declare topic parameters and create the typed ROS
subscriptions and publishers.

```cpp
template <typename PointT>
class MyComponent
  : public pcl_filter_base::ros::PclFilterComponentBase<PointT, MyFilter<PointT>>
{
public:
  using Base = pcl_filter_base::ros::PclFilterComponentBase<PointT, MyFilter<PointT>>;
  using CloudAdapter = typename Base::CloudAdapter;
  using PortDescriptor = typename Base::PortDescriptor;

  explicit MyComponent(const rclcpp::NodeOptions & options)
  : Base("my_filter", options, inputPorts(), outputPorts())
  {
    // Declare filter-specific parameters here.
  }

protected:
  static std::array<PortDescriptor, 1> inputPorts()
  {
    return {{
      Base::template inputPort<CloudAdapter>(
        "cloud",
        "/points/input",
        "Input point cloud topic."),
    }};
  }

  static std::array<PortDescriptor, 1> outputPorts()
  {
    return {{
      Base::template outputPort<CloudAdapter>(
        "cloud",
        "/points/output",
        "Filtered point cloud topic."),
    }};
  }

  void configureFilter() override
  {
    // Read filter-specific parameters and configure this->filter_.
  }
};
```

For multiple inputs, add more entries to `inputPorts()`. The constructor declares
`sync.policy`, `sync.queue_size`, and `sync.slop` automatically when the input
descriptor array has more than one entry. The synchronized input set is then
available through `takeInput<AdapterT>("port_name")`.

Outputs are also descriptor-driven. A component that can publish different
message types declares each output with its own adapter type and publishes to the
matching named port with `publish<AdapterT>("port_name", message)`.
