"""Tests for the database URI."""
import sys


def _reload_config():
    if 'config' in sys.modules:
        del sys.modules['config']
    import config
    return config


def test_sqlalchemy_uri_with_instance(monkeypatch):
    """Test the URI when the instance name is set."""
    monkeypatch.setenv('DATABASE_INSTANCE_CONNECTION_NAME', 'test-instance')
    config = _reload_config()
    assert config.Config.SQLALCHEMY_DATABASE_URI == 'postgresql+pg8000://'


def test_sqlalchemy_uri_without_instance(monkeypatch):
    """Test the URI when the instance name is not set."""
    monkeypatch.delenv('DATABASE_INSTANCE_CONNECTION_NAME', raising=False)
    monkeypatch.setenv('DATABASE_USERNAME', 'local')
    monkeypatch.setenv('DATABASE_PASSWORD', 'local-secret')
    monkeypatch.setenv('DATABASE_NAME', 'namex')
    monkeypatch.setenv('DATABASE_HOST', 'localhost')
    monkeypatch.setenv('DATABASE_PORT', '5432')
    config = _reload_config()
    assert config.Config.SQLALCHEMY_DATABASE_URI == 'postgresql+pg8000://local:local-secret@localhost:5432/namex'


def test_private_key_falls_back(monkeypatch):
    """Test a private key that cannot be decoded."""
    monkeypatch.delenv('DATABASE_INSTANCE_CONNECTION_NAME', raising=False)
    monkeypatch.setenv('PRIVATE_KEY', '/w==')
    config = _reload_config()
    assert config.Config.PRIVATE_KEY == '/w=='
