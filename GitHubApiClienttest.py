import unittest
from GitHubApiClient import GitHubApiClient

class TestGitHubApiClient(unittest.TestCase):
    def setUp(self):
        self.client = GitHubApiClient()

    def test_get_user_contributions(self):
        username = "iron87"  # Replace with a valid GitHub username
        contributions = self.client.get_user_contributions(username,12)
        self.assertIsInstance(contributions, dict)
        for repo, data in contributions.items():
            self.assertIn('events', data)
            self.assertIn('tech_stack', data)
            self.assertIsInstance(data['events'], dict)
            self.assertIsInstance(data['tech_stack'], list)

if __name__ == '__main__':
    unittest.main()