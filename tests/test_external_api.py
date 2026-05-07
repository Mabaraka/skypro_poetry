from unittest.mock import Mock
from unittest.mock import patch

from src.external_api import convert_currency


@patch("src.external_api.requests.get")
@patch("src.external_api.os.getenv")
def test_convert_currency(mock_getenv, mock_requests_get):
    mock_getenv.return_value = "test_api_key"

    mock_response = Mock()
    mock_response.json.return_value = {"result": 1500}

    mock_requests_get.return_value = mock_response

    result = convert_currency("USD", 50)

    expected_url = "https://api.apilayer.com/exchangerates_data/convert" "?to=RUB&from=USD&amount=50"

    mock_requests_get.assert_called_once_with(expected_url, headers={"apikey": "test_api_key"})

    assert result == 1500
