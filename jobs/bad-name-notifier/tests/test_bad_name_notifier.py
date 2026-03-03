import sys
import types

# Mock 'config' so Python won't complain
sys.modules["config"] = types.ModuleType("config")

# Optional: add functions or attributes your code expects
sys.modules["config"].get_named_config = lambda name: {}

from app import create_app  # noqa: E402


def test_create_app_returns_flask_app():
    app = create_app()
    assert app is not None
    assert hasattr(app, "run")


def test_app_config_default():
    app = create_app()
    assert app.config is not None
