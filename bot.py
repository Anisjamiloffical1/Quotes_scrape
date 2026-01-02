import random
import json
import requests
from bs4 import BeautifulSoup


USER_AGENTS_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
]


def parse_json(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    parsed_data = {}

    # Parse Title
    title_tag = soup.find('title')
    parsed_data['title'] = title_tag.get_text(strip=True) if title_tag else ''

    # Parse Description
    desc_tag = soup.find('div', id='app-description-latest')
    parsed_data['description'] = desc_tag.get_text(strip=True) if desc_tag else ''

    # Parse Sidebar Popular Posts
    popular_posts_parsed = []
    container = soup.find('div', class_='sidebar-posts-container')
    if container:
        posts = container.find_all('div', class_='post-item')  # adjust class if different
        for post in posts:
            title = post.get_text(strip=True)
            img = post.find('img')
            if title and img:
                popular_posts_parsed.append({
                    'title': title,
                    'img': img.get('src')
                })
    parsed_data['popular_posts'] = popular_posts_parsed

    # Parse Versions
    versions_parsed = []
    versions_container = soup.find('div', class_='beta-version-container')
    if versions_container:
        version_items = versions_container.find_all('span')  # adjust tag if different
        for version in version_items:
            versions_parsed.append(version.get_text(strip=True))
    parsed_data['versions'] = versions_parsed

    # Parse Rating
    rating_el = soup.find('div', class_='scored')
    parsed_data['rating'] = rating_el.get_text(strip=True) if rating_el else ''

    # Parse additional info
    parsed_data['category'] = ''
    parsed_data['operating_system'] = ''
    parsed_data['price'] = ''
    additional_info = soup.find('div', class_='app-more-info-schema')
    if additional_info:
        category_el = additional_info.find('a')
        parsed_data['category'] = category_el.get_text(strip=True) if category_el else ''

        info_divs = additional_info.find_all('div')
        if len(info_divs) > 2:
            parsed_data['operating_system'] = info_divs[1].text.split(':', 1)[1].strip()
            parsed_data['price'] = info_divs[2].text.split(':', 1)[1].strip()

    # Parse Tags
    tags = []
    tag_el = soup.find('div', class_='tagcloud')
    if tag_el:
        for tag in tag_el.find_all('a'):
            tags.append(tag.get_text(strip=True))
    parsed_data['tags'] = tags

    return parsed_data


def scrape_single(url, save_as):
    # Define headers to mimic user agent
    headers = {
        'user-agent': random.choice(USER_AGENTS_LIST)
    }

    # Send HTTP GET request
    print(f'Scraping {url}')
    result = requests.get(url, headers=headers, timeout=5)

    if result.status_code == 200:
        print(f'Request successful. Saving as {save_as}')

        # Parse HTML as JSON
        json_data = parse_json(result.text)

        # Convert JSON to string
        json_str = json.dumps(json_data)

        with open(save_as, 'w') as f:
            f.write(json_str)

    else:
        print(f'Request failed with status code: {result.status_code}')


def do_scraping():
    urls_file = './urls_list.txt'
    print(f'Parsing URLs from {urls_file}')
    with open(urls_file) as f:
        urls = f.readlines()

    if len(urls) > 0:
        print(f'{len(urls)} URLs found!')
        for idx, url in enumerate(urls):
            save_as = f'data_{idx+1}.json'
            scrape_single(url.strip(), save_as)
    else:
        print('No URLs found!')


do_scraping()