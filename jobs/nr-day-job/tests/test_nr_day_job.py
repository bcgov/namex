from unittest.mock import MagicMock, patch

import pytest

from nr_day_job import create_app, furnish_request_message, publish_email_message


def test_create_app_returns_flask_app():
    app = create_app()
    assert app is not None
    assert hasattr(app, 'run')


def test_app_config_default():
    app = create_app()
    assert app.config is not None


def test_publish_email_message_logs_and_publishes():
    app = create_app()
    with app.app_context():
        with patch('nr_day_job.queue.publish') as mock_publish, \
             patch('nr_day_job.current_app.logger') as mock_logger:
            payload = {'test': 'data'}
            publish_email_message(payload)
            mock_logger.debug.assert_called()
            mock_publish.assert_called_with(topic=app.config.get('EMAILER_TOPIC', ''), payload=payload)


def test_furnish_request_message_sets_flags():
    app = create_app()
    with app.app_context():
        mock_request = MagicMock()
        mock_request.nrNum = 'NR123'
        mock_request.save_to_db = MagicMock()
        with patch('nr_day_job.queue.publish') as mock_publish:
            # Test before-expiry
            furnish_request_message(mock_request, 'before-expiry')
            assert mock_request.notifiedBeforeExpiry is True
            # Test expired
            furnish_request_message(mock_request, 'expired')
            assert mock_request.notifiedExpiry is True
            assert mock_request.stateCd == 'EXPIRED'
            mock_request.save_to_db.assert_called()
            mock_publish.assert_called()
