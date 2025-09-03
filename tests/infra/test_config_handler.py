from pathlib import Path

from feedgy_ds_repo_template.infra.config_handler import parse_config

from tests.conftest import TEST_DATA_ROOT


def test_parse_config():
    config_file = Path.joinpath(TEST_DATA_ROOT, "config.yaml")
    config = parse_config(str(config_file))
    assert config["model_name"] == "test"
