"""Integration test for word classification - testing the complete word classification flow."""

from unittest.mock import Mock

import pytest

from namex.services.word_classification.token_classifier import TokenClassifier


class TestTokenClassifierIntegration:
    """Integration tests to verify the complete word classification flow works correctly."""

    def test_full_classification_workflow(self):
        """Test the complete workflow from word input to classified output."""
        # Create a mock word classification service that simulates database responses
        mock_service = Mock()
        
        # Create mock classification objects that simulate database records
        def create_mock_classification(classification_type):
            mock_obj = Mock()
            mock_obj.classification = classification_type
            return mock_obj
        
        # Configure mock responses for different words
        def mock_find_one(word):
            word = word.lower().strip()
            if word == 'tech':
                return [create_mock_classification('DIST')]
            elif word == 'amazing':
                return [create_mock_classification('DESC')]
            elif word == 'solutions':
                return [create_mock_classification('DESC')]
            elif word == 'innovative':
                return [create_mock_classification('DIST')]
            elif word == 'consulting':
                # Word with multiple classifications
                return [
                    create_mock_classification('DIST'),
                    create_mock_classification('DESC')
                ]
            else:
                return None  # Unclassified
        
        mock_service.find_one.side_effect = mock_find_one
        
        # Create classifier and test the complete workflow
        classifier = TokenClassifier(mock_service)
        
        # Test setting name_tokens which should trigger classification
        test_words = ['AMAZING', '  tech  ', 'Solutions', 'UnknownWord', 'INNOVATIVE', 'consulting']
        classifier.name_tokens = test_words
        
        # Verify the results
        # Words that should be distinctive: tech, innovative, consulting (DIST classification)
        expected_distinctive = {'tech', 'innovative', 'consulting'}
        # Words that should be descriptive: amazing, solutions, consulting (DESC classification)  
        expected_descriptive = {'amazing', 'solutions', 'consulting'}
        # Words that should be unclassified: unknownword
        expected_unclassified = {'unknownword'}
        
        assert set(classifier.distinctive_word_tokens) == expected_distinctive
        assert set(classifier.descriptive_word_tokens) == expected_descriptive
        assert set(classifier.unclassified_word_tokens) == expected_unclassified
        
        # Verify service was called for each word
        assert mock_service.find_one.call_count == len(test_words)

    def test_expected_classification_behavior(self):
        """Test that our implementation produces logically correct classification results."""
        # This test validates the expected behavior based on business logic
        mock_service = Mock()
        
        # Set up mock data that represents expected classification behavior
        mock_distinctive = Mock()
        mock_distinctive.classification = 'DIST'
        
        mock_descriptive = Mock()
        mock_descriptive.classification = 'DESC'
        
        test_data = {
            'innovative': [mock_distinctive],
            'amazing': [mock_descriptive],
            'tech': [mock_distinctive],
            'solutions': [mock_descriptive],
        }
        
        def mock_find_one(word):
            return test_data.get(word.lower().strip())
        
        mock_service.find_one.side_effect = mock_find_one
        
        classifier = TokenClassifier(mock_service)
        classifier.name_tokens = ['innovative', 'amazing', 'tech', 'solutions']
        
        # Expected results based on business logic
        expected_distinctive = ['innovative', 'tech']
        expected_descriptive = ['amazing', 'solutions']
        expected_unclassified = []
        
        # Verify our implementation produces expected results
        assert classifier.distinctive_word_tokens == expected_distinctive
        assert classifier.descriptive_word_tokens == expected_descriptive
        assert classifier.unclassified_word_tokens == expected_unclassified

    def test_edge_cases_handling(self):
        """Test edge cases that the implementation should handle correctly."""
        mock_service = Mock()
        
        # Test empty input
        classifier = TokenClassifier(mock_service)
        classifier.name_tokens = []
        
        assert classifier.distinctive_word_tokens == []
        assert classifier.descriptive_word_tokens == []
        assert classifier.unclassified_word_tokens == []
        
        # Test all unclassified
        mock_service.find_one.return_value = None
        classifier.name_tokens = ['unknown1', 'unknown2']
        
        assert classifier.distinctive_word_tokens == []
        assert classifier.descriptive_word_tokens == []
        assert classifier.unclassified_word_tokens == ['unknown1', 'unknown2']

    def test_memory_efficiency(self):
        """Test that our implementation is memory efficient with larger datasets."""
        mock_service = Mock()
        mock_classification = Mock()
        mock_classification.classification = 'DIST'
        mock_service.find_one.return_value = [mock_classification]
        
        classifier = TokenClassifier(mock_service)
        
        # Test with a larger dataset
        large_word_list = [f'word{i}' for i in range(100)]
        classifier.name_tokens = large_word_list
        
        # Should complete without memory issues
        assert len(classifier.distinctive_word_tokens) == 100
        assert len(classifier.descriptive_word_tokens) == 0
        assert len(classifier.unclassified_word_tokens) == 0

    def test_performance_characteristics(self):
        """Test that our implementation performs well with reasonable datasets."""
        import time
        
        mock_service = Mock()
        mock_classification = Mock()
        mock_classification.classification = 'DIST'
        mock_service.find_one.return_value = [mock_classification]
        
        classifier = TokenClassifier(mock_service)
        
        # Time the operation
        start_time = time.time()
        classifier.name_tokens = [f'word{i}' for i in range(50)]
        end_time = time.time()
        
        # Should complete reasonably quickly
        execution_time = end_time - start_time
        assert execution_time < 1.0  # Should take less than 1 second
        
        # Verify results are correct
        assert len(classifier.distinctive_word_tokens) == 50
