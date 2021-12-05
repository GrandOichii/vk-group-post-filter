import requests
import json
from termcolor import colored

TOKEN = open('TOKEN', 'r').read()
banned_words = [word for word in open('banned_words.txt', 'r').read().split('\n')]
priority_words = [word for word in open('priority_words.txt', 'r').read().split('\n')]
blacklist_urls = [word for word in open('blacklist.txt', 'r').read().split('\n')]

def vk_get_request(METHOD, PARAMS):
    url = 'https://api.vk.com/method/{}?{}&access_token={}&v={}'.format(METHOD, PARAMS, TOKEN, 5.131)
    return requests.get(url).content

def check_for_banned_words(item):
    text = item['text'].lower()
    for word in banned_words:
        if word != '' and word in text:
            return True
    return False

def check_for_photos(item):
    result = 'attachments' in item
    return result

def check_priority(item):
    text = item['text'].lower()
    for word in priority_words:
        if word != '' and word in text:
            return True
    return False

def filter(items):
    texts = []
    ids = []
    for item in items:
        if check_for_banned_words(item):
            continue
        prioritized = check_priority(item) or check_for_photos(item)
        text = item['text']
        id = '{}_{}'.format(item['from_id'], item['id'])

        if prioritized:
            texts += [text]
            ids += [id]
        else:
            texts.insert(0, text)
            ids.insert(0, id)
    return [texts, ids]

group_id = 'sosed499'
count = 100
vk_url = f'https://vk.com/{group_id}?w=wall{{}}'

id = json.loads(vk_get_request('groups.getById', f'group_ids={group_id}'))['response'][0]['id']
items = json.loads(vk_get_request('wall.get', f'owner_id=-{id}&count={count}'))['response']['items']
items.reverse()
result = filter(items)
for i in range(len(result[0])):
    url = vk_url.format(result[1][i])
    if url in blacklist_urls:
        continue
    print(colored(result[0][i], 'white'))
    print(colored(url, 'blue'))
    if check_for_photos(items[i]):
        print(colored('\tHAS PHOTO(ES)', 'red'))
    print('-' * 20)