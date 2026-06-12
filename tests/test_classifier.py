import pytest
from unittest.mock import patch, MagicMock
from agents.classifier import classify_email

def test_classify_complaint():
    with patch('agents.classifier.client') as mock_client:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "complaint"
        mock_client.chat.completions.create.return_value = mock_response

        result = classify_email("My order never arrived and I am very angry")
        assert result == "complaint"

def test_classify_spam():
    with patch('agents.classifier.client') as mock_client:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "spam"
        mock_client.chat.completions.create.return_value = mock_response

        result = classify_email("Buy cheap medicines now click here!!!")
        assert result == "spam"

def test_classify_inquiry():
    with patch('agents.classifier.client') as mock_client:
        mock_response = MagicMock()
        mock_response.choices[0].message.content = "inquiry"
        mock_client.chat.completions.create.return_value = mock_response

        result = classify_email("Can you explain your refund policy?")
        assert result == "inquiry"

def test_classify_returns_other_on_failure():
    with patch('agents.classifier.client') as mock_client:
        mock_client.chat.completions.create.side_effect = Exception("API down")

        result = classify_email("some email text")
        assert result == "other"