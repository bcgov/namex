"""Version information."""
import os

from synonyms.VERSION import __version__


def _build_openshift_run_version_id():
    commit_hash = os.getenv("OPENSHIFT_BUILD_COMMIT", None)
    if commit_hash:
        return "{ver}-{hash}".format(ver=__version__, hash=commit_hash[:10])
    return None


def get_run_version():
    """Return version of service."""
    return __version__ if (_build_openshift_run_version_id() is None) else _build_openshift_run_version_id()
