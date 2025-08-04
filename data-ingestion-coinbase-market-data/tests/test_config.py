import importlib.util
from pathlib import Path


def load_config_module():
    module_path = Path(__file__).resolve().parents[1] / "app" / "config.py"
    spec = importlib.util.spec_from_file_location("config", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_config_keeps_defaults_when_env_missing():
    config_module = load_config_module()
    cfg = config_module.Config({})
    assert cfg.KAFKA_BROKERS == "localhost:9094"


def test_config_overrides_with_env():
    config_module = load_config_module()
    cfg = config_module.Config({"KAFKA_BROKERS": "example:9092"})
    assert cfg.KAFKA_BROKERS == "example:9092"
