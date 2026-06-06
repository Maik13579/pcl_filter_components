# pcl_filter_synchronizer

`pcl_filter_synchronizer` contains a header-only synchronizer for PCL filter
components that use adapted custom message types and `std::unique_ptr`
ownership.

The synchronizer owns one typed subscription per input port, stores unmatched
messages by port name, and invokes a ready callback when a complete input set is
available. Component authors access synchronized messages through typed
accessors rather than raw type-erased storage.

Supported policies are `ExactTime` and `ApproximateTime`. `queue_size` limits
unmatched messages per input port, and `slop` controls the timestamp tolerance
for approximate matching.
