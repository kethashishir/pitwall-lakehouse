from orchestration.dagster_project.definitions import defs


def test_dagster_definitions_load_assets() -> None:
    asset_graph = defs.resolve_asset_graph()
    asset_keys = {asset_key.to_user_string() for asset_key in asset_graph.get_all_asset_keys()}

    assert asset_keys == {
        "bronze_racedata_fixture",
        "dbt_lakehouse_build",
        "dbt_quality_summary",
    }


def test_dagster_quality_asset_depends_on_dbt_build() -> None:
    asset_graph = defs.resolve_asset_graph()

    quality_key = next(
        asset_key
        for asset_key in asset_graph.get_all_asset_keys()
        if asset_key.to_user_string() == "dbt_quality_summary"
    )

    quality_node = asset_graph.get(quality_key)
    parent_keys = {parent_key.to_user_string() for parent_key in quality_node.parent_keys}

    assert parent_keys == {"dbt_lakehouse_build"}
