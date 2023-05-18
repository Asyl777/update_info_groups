from clickhouse_driver import Client


class DB:
    def __init__(self):
        self.client = Client(host='localhost', port='9000', user='default', password='123', database='test_db')

    # Функция для взятия ссылок
    def get_link(self):
        result = self.client.execute('SELECT link FROM resource_social')
        return result

    # Функция для взятий айди по ссылке
    def get_id(self, link):
        result = self.client.execute("SELECT id FROM resource_social WHERE link = '{}'".format(link))
        return result

    # Функция взятия айди города, региона и страны
    def get_city_id(self, city):
        result = self.client.execute(
            "SELECT city_id, country_id, region_id FROM cities WHERE city_name = '{}';".format(city))
        return result

    # Функция обновления данных
    def update_groups(self, link, data):
        self.client.execute('''DELETE FROM resource_social WHERE link = '{}' '''.format(link))
        query = '''
             INSERT INTO resource_social
             (id, country_id, region_id, city_id, resource_name, link, screen_name, image_profile, start_date_imas, members)
             VALUES
         '''

        self.client.execute('INSERT INTO resource_social (id, country_id, region_id, city_id, resource_name, link, '
                            'screen_name, image_profile, start_date_imas, members)   VALUES', data)

