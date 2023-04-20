import requests
from bs4 import BeautifulSoup

url = 'https://itexamanswers.net/network-security-version1-0-final-exam-answers-full.html'

response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find the div with class "main-container"
main_container = soup.find('div', class_='main-container')

# Find the article with class "article"
article = main_container.find('article', class_='article')

# Find the div with class "post-single-content"
post_content = article.find('div', class_='post-single-content')

# Find all <p> and <ul> tags within the "post-single-content" div
elements = post_content.find_all(['p', 'ul'])

for element in elements:
    # Check if the current element is a <p> tag
    if element.name == 'p':
        # If the next element is a <ul> tag, remove the newline between the <p> and <ul> tags
        next_element = element.find_next_sibling()
        if next_element and next_element.name == 'ul':
            text = element.text.strip()
            if text.startswith('Explanation:'):
                continue
            print(text, end='')
        else:
            text = element.text.strip()
            if text.startswith('Explanation:'):
                continue
            print(text)
    # If the current element is a <ul> tag
    elif element.name == 'ul':
        li_tags = element.find_all('li')
        answer_indexes = []
        for i, li in enumerate(li_tags):
            if li.find('span', style=True):
                answer_indexes.append(str(i + 1))
        num_answers = len(answer_indexes)
        if num_answers == 1:
            s_or_m = "single"
        else:
            s_or_m = "multiple"
        for li in li_tags:
            text = li.text.strip()
            if text.startswith('Explanation:'):
                continue
            print(text)
        print('.')
        print(s_or_m)
        if answer_indexes:
            answer_str = ', '.join(answer_indexes)
            print(answer_str)
        else:
            print('None')
        print('\n\n!')
