import requests
import base64

def get_public_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch repositories (Status Code: {response.status_code})")
        return None

def get_readme(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/readme"
    response = requests.get(url)
    
    if response.status_code == 200:
        readme_data = response.json()
        readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
        return readme_content
    else:
        print(f"No README found for {repo}.")
        return None

if __name__ == '__main__':
    username = input("Enter GitHub username: ")
    repos = get_public_repos(username)
    
    if repos:
        for repo in repos:
            name = repo['name']
            description = repo.get('description', 'No description provided')
            topics = ', '.join(repo.get('topics', [])) or "No topics"
            created_at = repo['created_at']
            updated_at = repo['updated_at']
            
            print(f"\nRepository: {name}")
            print(f"Description: {description}")
            print(f"Topics: {topics}")
            print(f"Created at: {created_at}")
            print(f"Last updated: {updated_at}")
            
            choice = input("Do you want to fetch the README? (yes/no): ").strip().lower()
            if choice == 'yes':
                readme = get_readme(username, name)
                if readme:
                    print(f"\nREADME for {name}:\n")
                    print(readme[:500])  # Print only the first 500 characters to keep output short
                    print("\n" + "="*80 + "\n")
