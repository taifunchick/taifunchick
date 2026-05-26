#!/usr/bin/env python3
"""
GitHub Projects README Generator
Fetches user repositories and generates a formatted README with project tables
"""

import requests
import os
from datetime import datetime

# GitHub username
USERNAME = "taifunchick"
TOKEN = os.getenv('GITHUB_TOKEN')

def get_user_repos():
    """Fetch all user repositories from GitHub API"""
    repos = []
    page = 1
    
    headers = {}
    if TOKEN:
        headers['Authorization'] = f'token {TOKEN}'
    
    while True:
        url = f'https://api.github.com/users/{USERNAME}/repos?page={page}&per_page=100&sort=updated'
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
            
        data = response.json()
        if not data:
            break
            
        repos.extend(data)
        page += 1
    
    return repos

def group_by_language(repos):
    """Group repositories by programming language"""
    groups = {}
    
    for repo in repos:
        # Skip forks and the profile README repo itself
        if repo['fork']:
            continue
            
        lang = repo['language'] or 'Other'
        
        if lang not in groups:
            groups[lang] = []
        
        groups[lang].append({
            'name': repo['name'],
            'description': repo['description'] or 'No description',
            'url': repo['html_url'],
            'stars': repo['stargazers_count'],
            'updated': repo['updated_at'][:10]
        })
    
    # Sort groups by number of repositories (descending)
    return dict(sorted(groups.items(), key=lambda x: len(x[1]), reverse=True))

def get_language_emoji(language):
    """Return emoji for programming language"""
    emojis = {
        'C#': '🎯',
        'JavaScript': '⚡',
        'TypeScript': '📘',
        'Python': '🐍',
        'Java': '☕',
        'Go': '🐹',
        'Rust': '🦀',
        'C++': '⚙️',
        'HTML': '🌐',
        'CSS': '🎨',
        'Vue': '📁',
        'Other': '📄'
    }
    return emojis.get(language, '📁')

def generate_projects_table(repos):
    """Generate markdown table for a language group"""
    if not repos:
        return ""
    
    table = "| Project | Description | ⭐ Stars | Updated |\n"
    table += "|---------|-------------|----------|---------|\n"
    
    for repo in repos:
        # Truncate description if too long
        desc = repo['description'][:50] + "..." if len(repo['description']) > 50 else repo['description']
        table += f"| [{repo['name']}]({repo['url']}) | {desc} | {repo['stars']} | {repo['updated']} |\n"
    
    return table

def generate_markdown(groups):
    """Generate the complete README markdown"""
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    markdown = """# 👋 Hi, I'm Taifunchick

## 🚀 About Me

Passionate developer from Russia building web applications, games, and backend systems. I love exploring different technologies and creating projects that solve real problems.

- 🔭 Currently working on various full-stack and game development projects
- 🌱 Learning: Advanced Unity optimization, DOTS, and cloud architecture
- 💬 Ask me about: C#, Unity, .NET, React, Python
- ⚡ Fun fact: I build projects across multiple stacks — from console apps to multiplayer games

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Languages** | C#, JavaScript, TypeScript, Python, HTML/CSS |
| **Frameworks & Libraries** | .NET, ASP.NET Core, React, Django, Vue |
| **Game Development** | Unity (DOTS, Mirror networking, Shaders) |
| **Databases** | SQL, Entity Framework |
| **Tools** | Git, GitHub Actions, REST APIs |

---

## 📊 GitHub Stats

<div align="center">

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=taifunchick&show_icons=true&theme=default&hide_border=true&hide_title=true)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=taifunchick&layout=compact&hide_border=true)

</div>

---

## 📁 My Projects

Below are my repositories automatically grouped by language and updated daily.

"""
    
    # Add project tables for each language
    for language, repos in groups.items():
        emoji = get_language_emoji(language)
        markdown += f"\n### {emoji} {language}\n\n"
        markdown += generate_projects_table(repos)
        markdown += "\n"
    
    markdown += f"""---

## 🌐 Connect With Me

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/taifunblade)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/taifunchick)

---

*📅 Automatically updated: {current_time}*  
*📊 Data fetched directly from GitHub API*
"""
    
    return markdown

def update_readme():
    """Main function to update README.md"""
    print("Fetching repositories from GitHub...")
    repos = get_user_repos()
    
    print(f"Found {len(repos)} repositories")
    
    print("Grouping by language...")
    groups = group_by_language(repos)
    
    print("Generating README...")
    new_content = generate_markdown(groups)
    
    # Update README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ Done! README.md has been updated.")

if __name__ == "__main__":
    update_readme()
