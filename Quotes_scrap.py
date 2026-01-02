import requests
import json
from bs4 import BeautifulSoup

Results = []
url = "https://quotes.toscrape.com/"

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
quotes = soup.find_all('div', class_='quote')
for quote in quotes:
    single_result_data = {}
    quote_text = quote.find('span', class_='text').get_text()
    if quote_text:
        single_result_data['quote'] = quote_text
    else :
        single_result_data['quote'] = 'Quote not found'
    
    author = quote.find('small', class_='author')
    if author:
        single_result_data['author'] = author.get_text()
    else :
        single_result_data['author'] = 'Author not found'
    
    tags = quote.find_all('a', class_='tag')
    if tags:
        single_result_data['tags'] = [tag.text for tag in tags]
    else :
        single_result_data['tags'] = 'Tags not found'

    Results.append(single_result_data)
    
    with open('quotes.json', 'w') as f:
        json.dump(Results, f, indent=4)

        print("Data has been written to quotes.json")
