# Copyright 2026 Maik Knof
# SPDX-License-Identifier: Apache-2.0

import pytest

from filter_component_editor.parameter_discovery import ComponentParameterDiscovery
from filter_component_editor.runtime import LivePipelineRuntime, LoadedComponent


class FailingConfigureRuntime(LivePipelineRuntime):
    def __init__(self) -> None:
        super().__init__()
        self.calls: list[tuple[str, str]] = []

    def load(self, node_id: str, spec: dict[str, object], configure: bool = True) -> None:
        self.calls.append(("load", node_id))
        self.loaded[node_id] = LoadedComponent(
            unique_id=1,
            full_node_name=f"/{node_id}",
            package=str(spec["package"]),
            component_class=str(spec["component_class"]),
            parameters=dict(spec["parameters"]),
            configured=False,
        )
        raise RuntimeError(f"Lifecycle transition 1 failed for /{node_id} from unconfigured [1]")

    def unload(self, node_id: str, ensure_started: bool = True) -> None:
        self.calls.append(("unload", node_id))
        self.loaded.pop(node_id, None)


def test_configured_probe_is_unloaded_when_lifecycle_configure_fails() -> None:
    runtime = FailingConfigureRuntime()
    discovery = ComponentParameterDiscovery(runtime)

    with pytest.raises(RuntimeError, match="Lifecycle transition 1 failed"):
        discovery.parameters_for_configured_component(
            "grid_map_components_filter_chain",
            "grid_map_components_filter_chain::RosFilterChainGridMapComponent",
            {
                "filters.filter1.name": "threshold",
                "filters.filter1.type": "gridMapFilters/ThresholdFilter",
            },
        )

    assert runtime.calls == [
        ("load", "parameter_probe_ros_filter_chain_grid_map"),
        ("unload", "parameter_probe_ros_filter_chain_grid_map"),
    ]
    assert runtime.loaded == {}
