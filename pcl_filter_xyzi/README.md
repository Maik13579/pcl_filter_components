# pcl_filter_xyzi

`pcl_filter_xyzi` registers the `pcl::PointXYZI` instantiations of
the reusable component templates from `pcl_filter_components`.

Registered classes:

- `pcl_filter_xyzi::VoxelGridXYZIComponent`
- `pcl_filter_xyzi::PassThroughXYZIComponent`
- `pcl_filter_xyzi::CropBoxXYZIComponent`
- `pcl_filter_xyzi::PointCloudMergerXYZIComponent`

This package owns the `PointXYZI` filter discovery exports and the loadable
component shared library. Runtime graphs should use:

```yaml
package: pcl_filter_xyzi
component_class: pcl_filter_xyzi::VoxelGridXYZIComponent
```
