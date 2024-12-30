import unittest

from githubapiclient import GitHubApiClient


class TestGitHubApiClient(unittest.TestCase):

    def setUp(self):
        self.client = GitHubApiClient()

    def test_get_user_contributions(self):
        username = "iron87"    # Replace with a valid GitHub username
        contributions = self.client.get_user_contributions(username, 12)
        self.assertIsInstance(contributions, dict)
        repos = contributions['repos']
        for repo, data in repos.items():
            self.assertIn('events', data)
            self.assertIn('tech_stack', data)
            self.assertIsInstance(data['events'], dict)
            self.assertIsInstance(data['tech_stack'], list)

    def test_get_user_contributions_does_not_contains_public_and_watch_events(
            self):
        username = "iron87"    # Replace with a valid GitHub username
        contributions = self.client.get_user_contributions(username, 12)
        self.assertIsInstance(contributions, dict)
        repos = contributions['repos']
        for repo, data in repos.items():
            self.assertIn('events', data)
            self.assertIsNot('events.type', 'WatchEvent')
            self.assertIsNot('events.type', 'PublicEvent')


if __name__ == '__main__':
    unittest.main()
