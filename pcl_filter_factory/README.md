# pcl_filter_factory

`pcl_filter_factory` parses saved YAML pipeline graphs and loads the requested
filter components into one process with intra-process communication enabled.

The `executor_threads` parameter selects single-threaded or multi-threaded
execution. Topic nodes in YAML become input, output, and intermediate topic
bindings. Filter nodes are loaded through `rclcpp_components`, then configured
and activated through their lifecycle interface.

Incoming edges are mapped to `inputs.<target_port>.topic` parameters and
outgoing edges are mapped to `outputs.<source_port>.topic` parameters. Legacy
graph ports `in` and `out` are normalized to the `cloud` port. A filter node's
YAML `sync` map is passed through as `sync.*` parameters for components that
declare multiple inputs.

Factory headers use the `pcl_filter_factory/...` include root and the
`pcl_filter_factory::pipeline` namespace.
