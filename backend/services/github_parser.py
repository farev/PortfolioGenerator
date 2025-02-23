import requests
import base64
import pprint
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO

def get_public_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch repositories (Status Code: {response.status_code})")
        return None

def get_user(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    else:
        print(f"Error: Unable to fetch user info (Status Code: {response.status_code})")
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

def extract_username(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    
    if len(path_parts) >= 1:
        return path_parts[0]  # First part of the path is the username
    return None

def get_image_if_not_default(user_data):
    url = user_data['avatar_url']
    try:
        response = requests.get(url)
        avatar = Image.open(BytesIO(response.content))
    except:
        return None
    colors = set()
    pixels = avatar.load()
    width, height = avatar.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            colors.add((r, g, b))
    if len(colors) > 100:
        return avatar
    else:
        return None

def get_user_data(username):
    user = get_user(username)
    if user is None:
        return None
    target_fields = [
        'bio',
        'email',
        'twitter_username',
        'avatar_url'
    ]
    user_data = {}
    for field in target_fields:
        if field in user and user[field]:
            user_data[field] = user[field]
    if not user_data:
        return None
    return user_data

def get_projects_with_description(username):
    repos = get_public_repos(username)
    if repos is None:
        return None
    
    projects = []
    for repo in repos:
        if not repo.get('description'):
            continue
            
        name = repo['name']
        description = repo['description']
        url = repo['html_url']
        project = {
            'name': name, 
            'description': description, 
            'url': url
        }
        
        if 'topics' in repo and repo['topics']:
            project['topics'] = repo['topics']
        if 'homepage' in repo and repo['homepage']:
            project['homepage'] = repo['homepage']
            
        projects.append(project)
    
    return projects
            

if __name__ == '__main__':
    username = input("Enter GitHub username: ")
    username = extract_username(username)
    user_data = get_user_data(username)
    img = get_image_if_not_default(user_data)
    if img is not None:
        img.show()
    # pprint.pp(get_user_data(username))

    # projects = get_projects_with_description(username)
    # for project in projects:
    #     pprint.pp(project)


    # repos = get_public_repos(username)
    
    # if repos:
    #     for repo in repos:
    #         name = repo['name']
    #         description = repo.get('description', 'No description provided')
    #         topics = ', '.join(repo.get('topics', [])) or "No topics"
    #         created_at = repo['created_at']
    #         updated_at = repo['updated_at']
            
    #         print(f"\nRepository: {name}")
    #         print(f"Description: {description}")
    #         print(f"Topics: {topics}")
    #         print(f"Created at: {created_at}")
    #         print(f"Last updated: {updated_at}")
            
    #         choice = input("Do you want to fetch the README? (yes/no): ").strip().lower()
    #         if choice == 'yes':
    #             readme = get_readme(username, name)
    #             if readme:
    #                 print(f"\nREADME for {name}:\n")
    #                 print(readme[:500])  # Print only the first 500 characters to keep output short
    #                 print("\n" + "="*80 + "\n")
