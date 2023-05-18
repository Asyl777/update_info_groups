import re
import vk_api
import get_owner_id
from datetime import datetime
from main import DB


class vk_parser_api:
    def __init__(self, link):
        self.db = DB()
        self.access_token = '04d70d0604d70d0604d70d061707c4b3af004d704d70d06609097a872bcf54909115537'
        self.vk_session = vk_api.VkApi(token=self.access_token)
        self.link = link
        self.group_id = re.findall(r'\d+', link)
        id = self.db.get_id(self.link)
        self.id = id[0][0]

    '''Функция которая парсит инфорамцию'''

    def parse_vk_groups(self):
        vk = self.vk_session.get_api()
        try:
            self.group_info = vk.groups.getById(group_id=self.group_id, fields='members_count, photo_200, country, '
                                                                               'city, screen_name')[0]
            # Получаем нужную информацию о сообществе
            group_name = self.group_info["name"]
            group_members = self.group_info["members_count"]
            screen_name = self.group_info["screen_name"]
            try:
                city_name = self.group_info['city']['title']
                ids = self.db.get_city_id(city_name)
                city_id = ids[0][0]
                country_id = ids[0][1]
                region_id = ids[0][2]
            except:
                city_id = 0
                country_id = 0
                region_id = 0
            current_datetime = datetime.now().strftime('%Y-%m-%d')
            current_datetime = datetime.strptime(current_datetime, '%Y-%m-%d').date()
            try:
                image_profile = self.group_info["photo_200"]
            except:
                image_profile = 'None'
            print(current_datetime)
            print(self.id, group_name, city_id, region_id, country_id, group_members, screen_name, image_profile)

            self.data_update = [(self.id, country_id, region_id, city_id, group_name, link, screen_name, image_profile,
                                 current_datetime, group_members)]



        except Exception as e:
            print(f"Ошибка при парсинге и записи данных о сообществе {self.group_id}: {str(e)}")

    # Обновляем строку в таблице
    def update_table(self):
        self.db.update_groups(link, self.data_update)

    # запуск функций
    def start(self):
        self.parse_vk_groups()
        # self.update_table()


links = get_owner_id.links_vk
for link in links:
    par = vk_parser_api(link)
    par.start()
