import requests
import os

# Ваш GitHub username
USERNAME = "ваш_username"  # ЗАМЕНИТЕ НА ВАШ USERNAME!
TOKEN = os.getenv('GITHUB_TOKEN')  # Токен будет доступен автоматически

def get_user_repos():
    """Получает все репозитории пользователя"""
    repos = []
    page = 1
    
    headers = {}
    if TOKEN:
        headers['Authorization'] = f'token {TOKEN}'
    
    while True:
        url = f'https://api.github.com/users/{USERNAME}/repos?page={page}&per_page=100&sort=updated'
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Ошибка: {response.status_code}")
            break
            
        data = response.json()
        if not data:
            break
            
        repos.extend(data)
        page += 1
    
    return repos

def group_by_language(repos):
    """Группирует репозитории по языкам"""
    groups = {}
    
    for repo in repos:
        # Пропускаем fork'и и репозиторий с профилем (если хотите)
        if repo['fork']:
            continue
            
        lang = repo['language'] or 'Other'
        
        if lang not in groups:
            groups[lang] = []
        
        groups[lang].append({
            'name': repo['name'],
            'description': repo['description'] or 'Нет описания',
            'url': repo['html_url'],
            'stars': repo['stargazers_count'],
            'updated': repo['updated_at'][:10]
        })
    
    # Сортируем группы по количеству репозиториев
    return dict(sorted(groups.items(), key=lambda x: len(x[1]), reverse=True))

def generate_markdown(groups):
    """Генерирует markdown для README"""
    markdown = """# Мои проекты на GitHub

Проекты автоматически сгруппированы по языкам программирования и обновляются каждый день.

## 📊 Статистика

"""
    
    # Добавляем общую статистику
    total_projects = sum(len(repos) for repos in groups.values())
    markdown += f"- **Всего проектов:** {total_projects}\n"
    markdown += f"- **Языков:** {len(groups)}\n\n"
    
    markdown += "---\n\n"
    
    # Группируем по языкам
    for language, repos in groups.items():
        # Иконки для популярных языков
        icon = get_language_icon(language)
        markdown += f"## {icon} {language}\n\n"
        
        for repo in repos:
            markdown += f"### • [{repo['name']}]({repo['url']})\n"
            markdown += f"  📝 {repo['description']}\n"
            markdown += f"  ⭐ {repo['stars']} stars | 🕐 Обновлено: {repo['updated']}\n\n"
        
        markdown += "---\n\n"
    
    markdown += "\n---\n"
    markdown += f"*Автоматически обновлено: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
    markdown += "*Данные берутся напрямую из GitHub API*"
    
    return markdown

def get_language_icon(language):
    """Возвращает иконку для языка"""
    icons = {
        'Python': '🐍',
        'JavaScript': '⚡',
        'TypeScript': '📘',
        'Java': '☕',
        'Go': '🐹',
        'Rust': '🦀',
        'C++': '⚙️',
        'C#': '🎯',
        'PHP': '🐘',
        'Ruby': '💎',
        'Swift': '🍎',
        'Kotlin': '📱',
        'HTML': '🌐',
        'CSS': '🎨',
        'Shell': '🐚',
        'SQL': '🗄️',
    }
    return icons.get(language, '📁')

def update_readme():
    """Основная функция"""
    print("Получаем репозитории...")
    repos = get_user_repos()
    
    print(f"Найдено {len(repos)} репозиториев")
    
    print("Группируем по языкам...")
    groups = group_by_language(repos)
    
    print("Генерируем README...")
    new_content = generate_markdown(groups)
    
    # Обновляем README.md
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("Готово! README.md обновлен.")

if __name__ == "__main__":
    update_readme()
