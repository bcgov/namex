import importlib
import sys

import pytest


def reload_config_module():
    if "bad_designation_notifier.config" in sys.modules:
        del sys.modules["bad_designation_notifier.config"]
    import bad_designation_notifier.config as config
    return config


def test_sqlalchemy_uri_with_instance(monkeypatch):
    monkeypatch.setenv("DATABASE_INSTANCE_CONNECTION_NAME", "test-instance")

    config = reload_config_module()

    assert config.Config.SQLALCHEMY_DATABASE_URI == "postgresql+pg8000://"


def test_sqlalchemy_uri_without_instance(monkeypatch):
    monkeypatch.delenv("DATABASE_INSTANCE_CONNECTION_NAME", raising=False)

    config = reload_config_module()

    assert "postgresql+pg8000://" in config.Config.SQLALCHEMY_DATABASE_URI


def test_get_named_config_valid():
    import bad_designation_notifier.config as config

    assert config.get_named_config("development") == config.DevConfig
    assert config.get_named_config("testing") == config.TestConfig
    assert config.get_named_config("production") == config.ProdConfig
    assert config.get_named_config("default") == config.ProdConfig


def test_get_named_config_invalid():
    import bad_designation_notifier.config as config

    with pytest.raises(KeyError) as exc_info:
        config.get_named_config("invalid-config")

    assert "Unknown configuration" in str(exc_info.value)