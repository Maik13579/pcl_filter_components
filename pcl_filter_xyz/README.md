# pcl_filter_xyz

`pcl_filter_xyz` registers the `pcl::PointXYZ` instantiations of
the reusable component templates from `pcl_filter_components`.

Registered classes:

- `pcl_filter_xyz::VoxelGridXYZComponent`
- `pcl_filter_xyz::PassThroughXYZComponent`
- `pcl_filter_xyz::CropBoxXYZComponent`
- `pcl_filter_xyz::PointCloudMergerXYZComponent`

This package owns the `PointXYZ` filter discovery exports and the loadable
component shared library. Runtime graphs should use:

```yaml
package: pcl_filter_xyz
component_class: pcl_filter_xyz::VoxelGridXYZComponent
```
