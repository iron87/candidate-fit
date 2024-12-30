import os
from datetime import datetime, timedelta
from typing import Dict, List

import requests


class GitHubApiClient:

    def __init__(self):
        self.base_url = "https://api.github.com"

    def fetch_events(self, username: str) -> List[Dict]:
        events = []
        url = f"{self.base_url}/users/{username}/events?perpage=100"
        response = requests.get(url)
        events = response.json()
        return events

    def get_repo_tech_stack(self, repo_name: str) -> List[str]:
        url = f"{self.base_url}/repos/{repo_name}/languages"
        response = requests.get(url)
        return list(response.json().keys())

    def is_event_within_the_timeframe(self, event_date: str,
                                      months_number: int) -> bool:
        event_datetime = datetime.strptime(event_date, "%Y-%m-%dT%H:%M:%SZ")
        three_months_ago = datetime.now() - timedelta(days=30 * months_number)
        return event_datetime >= three_months_ago

    def is_event_a_real_contribution(self, event_type: str) -> bool:
        return event_type not in ['WatchEvent', 'PublicEvent']

    def get_user_contributions(self, username: str, months_number: int) -> Dict:
        events = self.fetch_events(username)
        contributions = {}
        contributions['total_events'] = 0
        contributions['repos'] = {}
        for event in events:
            if 'repo' in event and 'name' in event[
                    'repo'] and 'created_at' in event:
                if self.is_event_within_the_timeframe(
                        event['created_at'],
                        months_number) and self.is_event_a_real_contribution(
                            event['type']):
                    contributions['total_events'] += 1
                    repo_name = event['repo']['name']
                    event_type = event['type']
                    if repo_name not in contributions['repos']:
                        contributions['repos'][repo_name] = {
                            'events': {},
                        #remove the comment to enable the tech_stack retrieval
                        #'tech_stack': self.get_repo_tech_stack(repo_name)
                        }
                    if event_type not in contributions['repos'][repo_name][
                            'events']:
                        contributions['repos'][repo_name]['events'][
                            event_type] = 0
                    contributions['repos'][repo_name]['events'][event_type] += 1
                else:
                    break

        return contributions
