from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError

from api_functions import (get_post_by_id, get_post_by_id_with_validation,
                           get_posts_by_user_id)


@patch('api_functions.http_get')
def test_get_post_by_id_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 1, "title": "Test Post"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = get_post_by_id(1)
    assert result == {"id": 1, "title": "Test Post"}
    mock_get.assert_called_once_with(
        'https://jsonplaceholder.typicode.com/posts/1')


@patch('api_functions.http_get')
def test_get_post_by_id_http_error(mock_get):
    mock_get.side_effect = HTTPError()
    result = get_post_by_id(999)
    assert result is None


@patch('api_functions.http_get')
def test_get_posts_by_user_id_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {"id": 1, "userId": 1, "title": "User's Post"}]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = get_posts_by_user_id(1)
    assert result == [{"id": 1, "userId": 1, "title": "User's Post"}]
    mock_get.assert_called_once_with(
        'https://jsonplaceholder.typicode.com/posts?userId=1')


@patch('api_functions.http_get')
def test_get_posts_by_user_id_http_error(mock_get):
    mock_get.side_effect = HTTPError()

    result = get_posts_by_user_id(999)
    assert result is None


@patch('api_functions.http_get')
def test_get_post_by_id_with_validation_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"id": 2, "title": "Validated Post"}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response
    result = get_post_by_id_with_validation(2)
    assert result == {"id": 2, "title": "Validated Post"}
    mock_get.assert_called_once_with(
        'https://jsonplaceholder.typicode.com/posts/2')


def test_get_post_by_id_with_validation_invalid_id():
    with pytest.raises(ValueError, match='post_id must be greater than 0'):
        get_post_by_id_with_validation(0)


@patch('api_functions.http_get')
def test_get_post_by_id_with_validation_http_error(mock_get):
    mock_get.side_effect = HTTPError()
    result = get_post_by_id_with_validation(999)
    assert result is None
