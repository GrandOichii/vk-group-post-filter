import requests
import json

TOKEN = open('TOKEN', 'r').read()
banned_words = [word for word in open('banned_words.txt', 'r').read().split('\n')]

def vk_get_request(METHOD, PARAMS):
    url = 'https://api.vk.com/method/{}?{}&access_token={}&v={}'.format(METHOD, PARAMS, TOKEN, 5.131)
    return requests.get(url).content

def check_for_banned_words(item):
    text = item['text'].lower()
    _=1
    for word in banned_words:
        if word in text:
            return True
    return False

def filter(items):
    texts = []
    ids = []
    for item in items:
        if check_for_banned_words(item):
            continue
        texts += [item['text']]
        ids += ['{}_{}'.format(item['from_id'], item['id'])]
    return [texts, ids]

group_id = 'find_you_saratov'
count = 100
vk_url = f'https://vk.com/{group_id}?w=wall{{}}'

id = json.loads(vk_get_request('groups.getById', f'group_ids={group_id}'))['response'][0]['id']
items = json.loads(vk_get_request('wall.get', f'owner_id=-{id}&count={count}'))['response']['items']
result = filter(items)
for i in range(len(result[0])):
    print(result[0][i])
    print(vk_url.format(result[1][i]))
    print('-' * 20)