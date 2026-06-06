# pcl_filter_base

`pcl_filter_base` contains reusable header-only ROS 2 infrastructure for PCL
filter components:

- lifecycle filter base class
- optional point-indices output base template
- parameter descriptor helpers

Headers use the `pcl_filter_base/...` include root and the
`pcl_filter_base::ros` namespace. Concrete filters and registered components live
in `pcl_filter_components`.

Filter components declare input and output port descriptors. The base class
creates subscriptions, publishers, and synchronization state from those
descriptors during lifecycle configuration. Topic parameters use
`inputs.<port>.topic` and `outputs.<port>.topic`; `input_topic` and
`output_topic` remain compatibility aliases for the default `cloud` port.

Derived components consume synchronized messages through typed accessors such as
`takeInput<AdapterT>("cloud")` and publish through
`publish<AdapterT>("cloud", message)`. Multi-input components additionally
declare `sync.policy`, `sync.queue_size`, and `sync.slop`.
