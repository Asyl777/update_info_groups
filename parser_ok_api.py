from ok_api import OkApi
from db import DB
import time
from datetime import datetime
import re
import get_owner_id

start_time = time.time()

access_token = "tkn1ofV21oJQ1aTc8bwpZhRtVfvutYSiM9bCNT7nAJR3Y35z718KFJoKmr19hu7uSbS7L"
application_key = "CJCENFLGDIHBABABA"
application_secret_key = "a0069b5790837c7b808075784e6ea42f"


class Parse_Api_Ok:
    def __init__(self, link):
        self.Db = DB()
        self.api = OkApi(access_token=access_token, application_key=application_key,
                         application_secret_key=application_secret_key)
        self.link = link
        id = self.Db.get_id(self.link)
        self.id = id[0][0]
        self.group_id = re.findall(r'\d+', link)

    def parse_info(self):
        data_info = self.api.group.getInfo(uids=self.group_id,
                                           fields=' NAME , PIC_AVATAR , members_count ,shortname, country, city')
        response = data_info.json()
        try:
            response = response[0]
        except:
            print("ERROR")
        try:
            resource_name = response['name']
        except:
            resource_name = '--'
        try:
            screen_name = response['shortname']
        except:
            screen_name = '--'
        try:
            city_id = response['city']
            ids = self.Db.get_city_id(city_id)
            city_id = ids[0][0]
            country_id = ids[0][1]
            region_id = ids[0][2]

        except:
            city_id = 0
            country_id = 0
            region_id = 0

        try:
            image_profile = response['picAvatar']
        except:
            image_profile = ''

        print(resource_name, screen_name, city_id, region_id, country_id, image_profile, sep='\n')

        try:
            members = response['members_count']
        except:
            members = 0

        print(members)
        current_datetime = datetime.now().strftime('%Y-%m-%d')
        current_datetime = datetime.strptime(current_datetime, '%Y-%m-%d').date()
        print(current_datetime)
        self.data_in_db = [(self.id, country_id, region_id, city_id, resource_name, self.link, screen_name,
                            image_profile, current_datetime, members)]

    def update_info_group(self):
        self.Db.update_groups(self.link, self.data_in_db)

    def start(self):
        self.parse_info()
        self.update_info_group()


links = get_owner_id.links_ok
for link in links:
    par = Parse_Api_Ok(link)
    par.start()
