from db import DB

db= DB()
links = db.get_link()

links_vk = []
links_ok = []
for row in links:
    if 'vk.com' in row[0]:
        links_vk.append(row[0])

    elif 'ok.ru' in row[0]:
        links_ok.append(row[0])
