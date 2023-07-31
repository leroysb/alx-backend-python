#!/usr/bin/env python3
"""test_client module
"""
import unittest
from client import GithubOrgClient
from parameterized import parameterized
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient class
    """
    
    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, test_org_name, mock_get_json):
        """test_org function.
        Tests that GithubOrgClient.org returns the correct value.
        """
        test_class = GithubOrgClient(test_org_name)
        test_class.org()
        mock_get_json.assert_called_once_with(f'https://api.github.com/orgs/{test_org_name}')

    def test_public_repos_url(self):
        """test_public_repos_url function.
        Tests that the result of _public_repos_url is the expected one
        based on the mocked payload.
        """
        with patch('client.GithubOrgClient.org',
                PropertyMock(return_value={"repos_url": "test_url"})):
            test_class = GithubOrgClient("test")
            self.assertEqual(test_class._public_repos_url, "test_url")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """test_public_repos function.
        Tests that the list of repos is what you expect from the chosen payload.
        """
        payload = [{"name": "Google"}, {"name": "Twitter"}]
        mock_get_json.return_value = payload
        with patch('client.GithubOrgClient._public_repos_url',
                PropertyMock(return_value="test_url")):
            test_class = GithubOrgClient("test")
            self.assertEqual(test_class.public_repos(), ["Google", "Twitter"])
            mock_get_json.assert_called_once_with("test_url")

    @parameterized.expand([
        ({'license': {'key': 'my_license'}}, 'my_license', True),
        ({'license': {'key': 'other_license'}}, 'my_license', False)
    ])
    @patch('client.get_json')
    def test_has_license(self, repo, license_key, expected, mock_get_json):
        """test_has_license function.
        Tests that the result of has_license is the expected one
        based on the mocked payload.
        """
        with patch.object(GithubOrgClient, 'has_license') as mock_has_license:
            mock_has_license.return_value = expected
            self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected)
            mock_has_license.assert_called_once_with(repo, license_key)


if __name__ == '__main__':
    unittest.main()
