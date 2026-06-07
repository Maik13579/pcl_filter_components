# Filter Component Pipeline

This repository contains ROS 2 packages for building filter pipelines from
loadable components. A pipeline is a graph of filter nodes connected to ROS
topics through named, typed ports.

A filter node is a ROS 2 lifecycle component that performs one processing step.
It declares the streams it consumes and produces, exposes parameters for its
operation, and uses typed adapters to convert between ROS messages and the data
representation used by the implementation. Topic nodes are graph bindings: they
name ROS topics that enter, leave, or connect parts of the graph. Topic nodes
are not loaded as components.

## Table of Contents

- [Pipeline Model](#pipeline-model)
- [Packages](#packages)
- [Architecture](#architecture)
- [Graph YAML](#graph-yaml)

## Pipeline Model

The graph has three main concepts:

- Filter components: loadable lifecycle components that process one or more
  typed streams and may publish one or more typed results.
- Ports: named inputs and outputs declared by each component. Port names are
  part of the component contract and are used by graph edges, the editor, and
  the factory.
- Topic nodes: endpoints and intermediate bindings that assign ROS topic names
  to graph edges.

Logical types describe what kind of data flows through a port. Component
packages export those logical types and map them to ROS message types through
type adapters. The editor and factory use that metadata to discover compatible
filters, topic types, and component classes.

Component topic parameters such as `inputs.<port>.topic` and
`outputs.<port>.topic` are normally filled from graph edges by
`filter_component_factory`.

## Packages

- [filter_component_synchronizer](filter_component_synchronizer/README.md): header-only
  unique-pointer synchronizer for filters with named input ports.
- [filter_component_base](filter_component_base/README.md): lifecycle component base classes
  and descriptor helpers for declaring ports, parameters, QoS, and sync.
- [filter_component_factory](filter_component_factory/README.md): saved graph interpreter
  that loads filter nodes and binds their ports to topics.
- [filter_component_editor](filter_component_editor/README.md): rqt graph editor with live
  background pipeline validation.
- [pcl](pcl/README.md): PCL-specific algorithms, type adapters, point-type
  component packages, and PCL validation tests.

## Architecture

The root packages define the generic framework. Concrete component families live
in their own package groups and export discovery metadata through the generic
`<filter_component>` package tag. The current repository includes a PCL
component family under [`pcl/`](pcl/README.md).

```text
filter_component_synchronizer
  -> filter_component_base
    -> component family packages
      -> filter_component_factory
      -> filter_component_editor
```

Component packages export filters with package metadata similar to:

```xml
<filter_component
  filter="ExampleFilter"
  input="ExampleType"
  output="ExampleType"/>
```

They can also export logical type aliases:

```xml
<filter_component
  type="ExampleType"
  type_adapter="example_package::ros::ExampleAdapter"
  message_type="example_interfaces/msg/Example"/>
```

## Graph YAML

Saved YAML is the portable pipeline description. Filter nodes record component
identity, filter parameters, port QoS, optional synchronization settings, and
editor layout. Edges connect named ports. Topic nodes provide the ROS topic
bindings used by those edges.

```yaml
nodes:
  - type: topic
    name: /input
    topic_type: ExampleType
  - type: filter
    name: ExampleFilter_1
    package: example_filter_package
    filter: ExampleFilter
    component_class: example_filter_package::ExampleFilterComponent
    input_type: ExampleType
    output_type: ExampleType
    parameters:
      filter.example_parameter: 1.0
  - type: topic
    name: /output
    topic_type: ExampleType
edges:
  - from: {node: /input, port: out}
    to: {node: ExampleFilter_1, port: input}
  - from: {node: ExampleFilter_1, port: output}
    to: {node: /output, port: in}
```

When the factory reads a graph, it loads filter nodes as components and maps the
topic-node edges to the corresponding component topic parameters.
