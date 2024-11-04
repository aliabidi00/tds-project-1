import requests
import csv
import os

# Set up your GitHub API token
GITHUB_TOKEN = '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'
HEADERS = {'Authorization': f'token {GITHUB_TOKEN}'}

# Define the base URL for the GitHub API
BASE_URL = 'https://api.github.com'

# Fetch users from Melbourne with more than 100 followers
def get_users():
    users = []
    url = f"{BASE_URL}/search/users?q=location:Melbourne+followers:>100"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code == 200:
        data = response.json()
        for user in data['items']:
            user_details = requests.get(user['url'], headers=HEADERS).json()
            users.append({
                'login': user_details['login'],
                'name': user_details['name'] or '',
                'company': user_details['company'] or '',
                'location': user_details['location'] or '',
                'email': user_details['email'] or '',
                'hireable': user_details['hireable'],
                'bio': user_details['bio'] or '',
                'public_repos': user_details['public_repos'],
                'followers': user_details['followers'],
                'following': user_details['following'],
                'created_at': user_details['created_at']
            })
    return users

# Write users data to CSV
def write_users_csv(users):
    with open('users.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['login', 'name', 'company', 'location', 'email', 'hireable', 'bio',
                      'public_repos', 'followers', 'following', 'created_at']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user in users:
            writer.writerow(user)

# Fetch repositories for each user and write to CSV
def get_repositories(users):
    repositories = []
    for user in users:
        repos_url = f"{BASE_URL}/users/{user['login']}/repos"
        response = requests.get(repos_url, headers=HEADERS)
        if response.status_code == 200:
            repos_data = response.json()
            for repo in repos_data[:500]:  # Limit to 500 repositories
                repositories.append({
                    'login': user['login'],
                    'full_name': repo['full_name'],
                    'created_at': repo['created_at'],
                    'stargazers_count': repo['stargazers_count'],
                    'watchers_count': repo['watchers_count'],
                    'language': repo['language'] or '',
                    'has_projects': repo['has_projects'],
                    'has_wiki': repo['has_wiki'],
                    'license_name': repo['license']['name'] if repo['license'] else ''
                })
    return repositories

# Write repositories data to CSV
def write_repositories_csv(repositories):
    with open('repositories.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['login', 'full_name', 'created_at', 'stargazers_count', 'watchers_count',
                      'language', 'has_projects', 'has_wiki', 'license_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for repo in repositories:
            writer.writerow(repo)

# Main script execution
if __name__ == "__main__":
    users = get_users()
    write_users_csv(users)
    repositories = get_repositories(users)
    write_repositories_csv(repositories)
