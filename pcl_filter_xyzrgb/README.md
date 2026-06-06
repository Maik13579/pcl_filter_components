# pcl_filter_xyzrgb

`pcl_filter_xyzrgb` registers the `pcl::PointXYZRGB` instantiations of
the reusable component templates from `pcl_filter_components`.

Registered classes:

- `pcl_filter_xyzrgb::VoxelGridXYZRGBComponent`
- `pcl_filter_xyzrgb::PassThroughXYZRGBComponent`
- `pcl_filter_xyzrgb::CropBoxXYZRGBComponent`
- `pcl_filter_xyzrgb::PointCloudMergerXYZRGBComponent`

This package owns the `PointXYZRGB` filter discovery exports and the loadable
component shared library. Runtime graphs should use:

```yaml
package: pcl_filter_xyzrgb
component_class: pcl_filter_xyzrgb::VoxelGridXYZRGBComponent
```
