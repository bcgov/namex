"""Unit tests for TokenClassifier and classifications_to_lists function."""

from unittest.mock import Mock, patch

import pytest

from namex.services.word_classification.token_classifier import (
    DataFrameFields,
    TokenClassifier,
    classifications_to_lists,
)


class TestClassificationsToLists:
    """Test the classifications_to_lists function for word classification processing."""

    def test_classifications_to_lists_empty_input(self):
        """Test with empty classifications list."""
        result = classifications_to_lists([])
        distinctive, descriptive, unclassified = result

        assert distinctive == []
        assert descriptive == []
        assert unclassified == []

    def test_classifications_to_lists_single_distinctive(self):
        """Test with single distinctive word."""
        classifications = [
            {'word': 'tech', 'word_classification': DataFrameFields.DISTINCTIVE.value}
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert distinctive == ['tech']
        assert descriptive == []
        assert unclassified == []

    def test_classifications_to_lists_single_descriptive(self):
        """Test with single descriptive word."""
        classifications = [
            {'word': 'amazing', 'word_classification': DataFrameFields.DESCRIPTIVE.value}
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert distinctive == []
        assert descriptive == ['amazing']
        assert unclassified == []

    def test_classifications_to_lists_single_unclassified(self):
        """Test with single unclassified word."""
        classifications = [
            {'word': 'unknown', 'word_classification': DataFrameFields.UNCLASSIFIED.value}
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert distinctive == []
        assert descriptive == []
        assert unclassified == ['unknown']

    def test_classifications_to_lists_mixed_classifications(self):
        """Test with multiple words of different classifications."""
        classifications = [
            {'word': 'amazing', 'word_classification': DataFrameFields.DESCRIPTIVE.value},
            {'word': 'tech', 'word_classification': DataFrameFields.DISTINCTIVE.value},
            {'word': 'solutions', 'word_classification': DataFrameFields.DESCRIPTIVE.value},
            {'word': 'unknown', 'word_classification': DataFrameFields.UNCLASSIFIED.value},
            {'word': 'innovative', 'word_classification': DataFrameFields.DISTINCTIVE.value},
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert distinctive == ['tech', 'innovative']
        assert descriptive == ['amazing', 'solutions']
        assert unclassified == ['unknown']

    def test_classifications_to_lists_preserves_order(self):
        """Test that order is preserved within each classification type."""
        classifications = [
            {'word': 'first', 'word_classification': DataFrameFields.DESCRIPTIVE.value},
            {'word': 'second', 'word_classification': DataFrameFields.DESCRIPTIVE.value},
            {'word': 'third', 'word_classification': DataFrameFields.DESCRIPTIVE.value},
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert descriptive == ['first', 'second', 'third']

    def test_classifications_to_lists_duplicate_words(self):
        """Test handling of duplicate words with same classification."""
        classifications = [
            {'word': 'tech', 'word_classification': DataFrameFields.DISTINCTIVE.value},
            {'word': 'tech', 'word_classification': DataFrameFields.DISTINCTIVE.value},
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert distinctive == ['tech', 'tech']  # Should preserve duplicates

    def test_classifications_to_lists_case_sensitivity(self):
        """Test that word case is preserved."""
        classifications = [
            {'word': 'Tech', 'word_classification': DataFrameFields.DISTINCTIVE.value},
            {'word': 'AMAZING', 'word_classification': DataFrameFields.DESCRIPTIVE.value},
        ]

        distinctive, descriptive, unclassified = classifications_to_lists(classifications)

        assert distinctive == ['Tech']
        assert descriptive == ['AMAZING']


class TestTokenClassifier:
    """Test the TokenClassifier class, focusing on the _classify_tokens method."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_word_classification_service = Mock()
        self.classifier = TokenClassifier(self.mock_word_classification_service)

    def test_init(self):
        """Test TokenClassifier initialization."""
        assert self.classifier.word_classification_service == self.mock_word_classification_service
        assert self.classifier.distinctive_word_tokens == []
        assert self.classifier.descriptive_word_tokens == []
        assert self.classifier.unclassified_word_tokens == []

    def test_classify_tokens_empty_input(self):
        """Test _classify_tokens with empty word list."""
        self.classifier._classify_tokens([])

        assert self.classifier.distinctive_word_tokens == []
        assert self.classifier.descriptive_word_tokens == []
        assert self.classifier.unclassified_word_tokens == []

    def test_classify_tokens_no_classification_found(self):
        """Test _classify_tokens when no classification is found for words."""
        # Mock the service to return None (no classification found)
        self.mock_word_classification_service.find_one.return_value = None

        words = ['unknown', 'mystery']
        self.classifier._classify_tokens(words)

        # All words should be unclassified
        assert self.classifier.distinctive_word_tokens == []
        assert self.classifier.descriptive_word_tokens == []
        assert self.classifier.unclassified_word_tokens == ['unknown', 'mystery']

    def test_classify_tokens_with_classifications(self):
        """Test _classify_tokens with words that have classifications."""
        # Create mock classification objects
        mock_distinctive_classification = Mock()
        mock_distinctive_classification.classification = 'DIST'

        mock_descriptive_classification = Mock()
        mock_descriptive_classification.classification = 'DESC'

        # Configure the mock service to return different classifications
        def mock_find_one(word):
            if word == 'tech':
                return [mock_distinctive_classification]
            elif word == 'amazing':
                return [mock_descriptive_classification]
            else:
                return None

        self.mock_word_classification_service.find_one.side_effect = mock_find_one

        words = ['amazing', 'tech', 'unknown']
        self.classifier._classify_tokens(words)

        assert self.classifier.distinctive_word_tokens == ['tech']
        assert self.classifier.descriptive_word_tokens == ['amazing']
        assert self.classifier.unclassified_word_tokens == ['unknown']

    def test_classify_tokens_multiple_classifications_per_word(self):
        """Test _classify_tokens when a word has multiple classifications."""
        # Create mock classification objects
        mock_classification_1 = Mock()
        mock_classification_1.classification = 'DIST'

        mock_classification_2 = Mock()
        mock_classification_2.classification = 'DESC'

        # Configure service to return multiple classifications for one word
        self.mock_word_classification_service.find_one.return_value = [
            mock_classification_1,
            mock_classification_2
        ]

        words = ['multi']
        self.classifier._classify_tokens(words)

        # The word should appear in both lists
        assert self.classifier.distinctive_word_tokens == ['multi']
        assert self.classifier.descriptive_word_tokens == ['multi']
        assert self.classifier.unclassified_word_tokens == []

    def test_classify_tokens_word_normalization(self):
        """Test that words are normalized (lowercased and stripped)."""
        mock_classification = Mock()
        mock_classification.classification = '  DIST  '  # With extra spaces

        self.mock_word_classification_service.find_one.return_value = [mock_classification]

        words = ['  TECH  ']  # Word with spaces and uppercase
        self.classifier._classify_tokens(words)

        # Should be normalized to lowercase and stripped
        assert self.classifier.distinctive_word_tokens == ['tech']

    def test_classify_tokens_classification_normalization(self):
        """Test that classification values are normalized (stripped)."""
        mock_classification = Mock()
        mock_classification.classification = '  DIST  '  # With extra spaces

        self.mock_word_classification_service.find_one.return_value = [mock_classification]

        words = ['tech']
        self.classifier._classify_tokens(words)

        # Should still be classified as distinctive despite extra spaces
        assert self.classifier.distinctive_word_tokens == ['tech']

    @patch('namex.services.word_classification.token_classifier.current_app')
    def test_classify_tokens_logs_unclassified_words(self, mock_current_app):
        """Test that unclassified words are logged."""
        # Mock the service to return None
        self.mock_word_classification_service.find_one.return_value = None

        words = ['unknown']
        self.classifier._classify_tokens(words)

        # Verify logging was called
        mock_current_app.logger.debug.assert_called_with('No word classification found for: unknown')

    @patch('namex.services.word_classification.token_classifier.current_app')
    def test_classify_tokens_handles_exceptions(self, mock_current_app):
        """Test that exceptions during classification are handled properly."""
        # Configure the mock service to raise an exception
        self.mock_word_classification_service.find_one.side_effect = Exception('Database error')

        words = ['test']

        # Should re-raise the exception
        with pytest.raises(Exception, match='Database error'):
            self.classifier._classify_tokens(words)

        # Should log the error
        mock_current_app.logger.error.assert_called()

    def test_name_tokens_property_triggers_classification(self):
        """Test that setting name_tokens triggers classification."""
        mock_classification = Mock()
        mock_classification.classification = 'DIST'
        self.mock_word_classification_service.find_one.return_value = [mock_classification]

        # Setting name_tokens should trigger _classify_tokens
        self.classifier.name_tokens = ['tech', 'solutions']

        assert self.classifier.name_tokens == ['tech', 'solutions']
        assert self.classifier.distinctive_word_tokens == ['tech', 'solutions']

    def test_name_tokens_property_empty_list_no_classification(self):
        """Test that setting empty name_tokens doesn't trigger classification."""
        # Setting empty list should not trigger classification
        self.classifier.name_tokens = []

        # find_one should not be called
        self.mock_word_classification_service.find_one.assert_not_called()
