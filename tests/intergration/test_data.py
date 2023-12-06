import unittest
# from unittest.mock import patch, MagicMock
from smaug_cmd.model.data import get_menus, create_asset
from smaug_cmd.domain.smaug_types import AssetCreateParams


class TestGetMenusIntegration(unittest.TestCase):
    def test_get_menus(self):
        # Act
        result = get_menus()

        # Assert
        self.assertTrue(result is not None)


class TestAsset(unittest.TestCase):
    # @patch('data._session.post')
    def test_create_asset(self):
        # Arrange
        # expected_status_code = 200
        # expected_response_data = {"result": {"data": {"json": {"detail": "Test detail"}}}}
        # mock_response = MagicMock()
        # mock_response.json.return_value = [expected_response_data]
        # mock_response.status_code = expected_status_code
        # mock_post.return_value = mock_response
        test_payload = AssetCreateParams(name="test", category_id=1, tags=["test"])

        # Act
        result = create_asset(test_payload)
        self.assertTrue(result is not None)
        # Assert
        # self.assertEqual(result, (expected_status_code, expected_response_data["result"]["data"]["json"]["detail"]))


if __name__ == '__main__':
    unittest.main()