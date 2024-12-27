import requests
import os
from typing import Dict, List
from datetime import datetime, timedelta

class GitHubApiClient:
    def __init__(self):
        self.base_url = "https://api.github.com"

    def fetch_events(self, username: str) -> List[Dict]:
        events = []
        page = 1
        while True:
            url = f"{self.base_url}/users/{username}/events?page={page}"
            response = requests.get(url)
            page_events = response.json()
            if not page_events:
                break
            events.extend(page_events)
            page += 1
        return events

    def get_repo_tech_stack(self, repo_name: str) -> List[str]:
        url = f"{self.base_url}/repos/{repo_name}/languages"
        response = requests.get(url)
        return list(response.json().keys())

    def is_event_within_the_timeframe(self, event_date: str,  months_number: int ) -> bool:
        event_datetime = datetime.strptime(event_date, "%Y-%m-%dT%H:%M:%SZ")
        three_months_ago = datetime.now() - timedelta(days=30*months_number)
        return event_datetime >= three_months_ago

    def get_user_contributions(self, username: str,months_number: int) -> Dict:
        events = self.fetch_events(username)
        contributions = {}

        for event in events:
            if 'repo' in event and 'name' in event['repo'] and 'created_at' in event:
                if self.is_event_within_the_timeframe(event['created_at'], months_number):
                    repo_name = event['repo']['name']
                    event_type = event['type']
                    if repo_name not in contributions:
                        contributions[repo_name] = {
                            'events': {},
                            'tech_stack': self.get_repo_tech_stack(repo_name)
                        }
                    if event_type not in contributions[repo_name]['events']:
                        contributions[repo_name]['events'][event_type] = 0
                    contributions[repo_name]['events'][event_type] += 1
                else:
                    break

        return contributions