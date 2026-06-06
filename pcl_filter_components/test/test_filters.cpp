// Copyright 2026 Maik Knof
// SPDX-License-Identifier: Apache-2.0

#include <gtest/gtest.h>

#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

#include "pcl_filter_components/filters/crop_box_filter.hpp"
#include "pcl_filter_components/filters/passthrough_filter.hpp"
#include "pcl_filter_components/filters/voxel_grid_filter.hpp"

namespace
{

pcl::PointXYZI makePoint(float x, float y, float z, float intensity = 1.0F)
{
  pcl::PointXYZI point;
  point.x = x;
  point.y = y;
  point.z = z;
  point.intensity = intensity;
  return point;
}

pcl::PointCloud<pcl::PointXYZI> makeCloud()
{
  pcl::PointCloud<pcl::PointXYZI> cloud;
  cloud.push_back(makePoint(0.0F, 0.0F, 0.0F));
  cloud.push_back(makePoint(0.01F, 0.01F, 0.01F));
  cloud.push_back(makePoint(2.0F, 2.0F, 3.0F));
  cloud.width = static_cast<std::uint32_t>(cloud.size());
  cloud.height = 1;
  cloud.is_dense = true;
  return cloud;
}

TEST(VoxelGridFilter, ReducesPointsInSameLeaf)
{
  pcl_filter_components::filters::VoxelGridFilter<pcl::PointXYZI> filter;
  filter.configure({0.1F, 0.1F, 0.1F, false});

  pcl::PointCloud<pcl::PointXYZI> output;
  filter.filter(makeCloud(), output);

  EXPECT_EQ(output.size(), 2U);
}

TEST(VoxelGridFilter, OutputsRepresentativeIndices)
{
  pcl_filter_components::filters::VoxelGridFilter<pcl::PointXYZI> filter;
  filter.configure({0.1F, 0.1F, 0.1F, false});

  std::vector<int> output;
  filter.filterIndices(makeCloud(), output);

  EXPECT_EQ(output.size(), 2U);
}

TEST(VoxelGridFilter, InvertsRepresentativeIndices)
{
  pcl_filter_components::filters::VoxelGridFilter<pcl::PointXYZI> filter;
  filter.configure({0.1F, 0.1F, 0.1F, true});

  std::vector<int> output;
  filter.filterIndices(makeCloud(), output);

  EXPECT_EQ(output.size(), 1U);
}

TEST(PassThroughFilter, RemovesPointsOutsideLimits)
{
  pcl_filter_components::filters::PassThroughFilter<pcl::PointXYZI> filter;
  filter.configure({"z", -0.5, 1.0, false});

  pcl::PointCloud<pcl::PointXYZI> output;
  filter.filter(makeCloud(), output);

  ASSERT_EQ(output.size(), 2U);
  for (const auto & point : output) {
    EXPECT_GE(point.z, -0.5F);
    EXPECT_LE(point.z, 1.0F);
  }
}

TEST(PassThroughFilter, OutputsIndicesAndSupportsInvert)
{
  pcl_filter_components::filters::PassThroughFilter<pcl::PointXYZI> filter;
  filter.configure({"z", -0.5, 1.0, false});

  std::vector<int> output;
  filter.filterIndices(makeCloud(), output);
  EXPECT_EQ(output, (std::vector<int>{0, 1}));

  filter.configure({"z", -0.5, 1.0, true});
  filter.filterIndices(makeCloud(), output);
  EXPECT_EQ(output, (std::vector<int>{2}));
}

TEST(CropBoxFilter, RemovesPointsOutsideBounds)
{
  pcl_filter_components::filters::CropBoxFilter<pcl::PointXYZI> filter;
  filter.configure({-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, false});

  pcl::PointCloud<pcl::PointXYZI> output;
  filter.filter(makeCloud(), output);

  ASSERT_EQ(output.size(), 2U);
  for (const auto & point : output) {
    EXPECT_GE(point.x, -1.0F);
    EXPECT_LE(point.x, 1.0F);
    EXPECT_GE(point.y, -1.0F);
    EXPECT_LE(point.y, 1.0F);
    EXPECT_GE(point.z, -1.0F);
    EXPECT_LE(point.z, 1.0F);
  }
}

TEST(CropBoxFilter, OutputsIndicesAndSupportsInvert)
{
  pcl_filter_components::filters::CropBoxFilter<pcl::PointXYZI> filter;
  filter.configure({-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, false});

  std::vector<int> output;
  filter.filterIndices(makeCloud(), output);
  EXPECT_EQ(output, (std::vector<int>{0, 1}));

  filter.configure({-1.0, -1.0, -1.0, 1.0, 1.0, 1.0, true});
  filter.filterIndices(makeCloud(), output);
  EXPECT_EQ(output, (std::vector<int>{2}));
}

}  // namespace
