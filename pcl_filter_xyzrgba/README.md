# pcl_filter_xyzrgba

`pcl_filter_xyzrgba` registers the `pcl::PointXYZRGBA` instantiations of
the reusable component templates from `pcl_filter_components`.

Registered classes:

- `pcl_filter_xyzrgba::VoxelGridXYZRGBAComponent`
- `pcl_filter_xyzrgba::PassThroughXYZRGBAComponent`
- `pcl_filter_xyzrgba::CropBoxXYZRGBAComponent`
- `pcl_filter_xyzrgba::PointCloudMergerXYZRGBAComponent`

This package owns the `PointXYZRGBA` filter discovery exports and the loadable
component shared library. Runtime graphs should use:

```yaml
package: pcl_filter_xyzrgba
component_class: pcl_filter_xyzrgba::VoxelGridXYZRGBAComponent
```
