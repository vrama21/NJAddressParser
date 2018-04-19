import requests
import re
from collections import defaultdict
from bs4 import BeautifulSoup


class Main:
    nj_parcels_url = 'http://njparcels.com/property/'

    def __init__(self):
        html_data = requests.get(self.nj_parcels_url)
        content = html_data.content
        self.soup = BeautifulSoup(content, 'html.parser')

        self.counties = []
        self.cities = []
        self.city_nums = []
        self.block_num = []

    def build_county_list(self):
        counties_html = self.soup.find_all('h2')
        for element in counties_html:
            self.counties.append(element.get_text())

    def build_city_list(self):
        cities_html = self.soup.find_all('span', class_='muniname')
        for element in cities_html:
            self.cities.append(element.get_text())

    def build_city_num_list(self):
        # TODO: Split list per county
        city_num_html = self.soup.find_all('span', class_='muniname')
        for i in city_num_html:
            city_num = re.findall('/property/(.+)/"', str(i))
            for j in city_num:
                self.city_nums.append(j)

    def build_block_list(self):
        url = self.nj_parcels_url + self.city_nums[18]
        _html_data = requests.get(url)
        _content = _html_data.content
        _soup = BeautifulSoup(_content, 'html.parser')

        block_list = _soup.find_all('a', class_=None)
        for j in block_list:
            block = re.findall('>([^A-Za-z]+)<', str(j))
            for k in block:
                self.block_num.append(k)

    def build_address_list(self):
        for i in self.block_num:
            print(i[0])
            url = self.nj_parcels_url + self.city_nums[18] + '/' + i[0]
            print(url)
            _html_data = requests.get(url)
            _content = _html_data.content
            _soup = BeautifulSoup(_content, 'html.parser')

            addr_list = _soup.find_all('tr')
            info = re.findall('<td>(.+)</td+', str(addr_list))

    def nested_dict(self):
        # main_dict = OrderedDict([])
        for k in self.counties:
            main_dict = defaultdict(list)
            for v in self.cities:
                main_dict.setdefault(k, []).append(v)
            print(main_dict['Atlantic County'])



if __name__ == '__main__':
    main = Main()

    main.build_county_list()
    main.build_city_list()
    main.build_city_num_list()
    main.build_block_list()
    # main.build_address_list()
    main.nested_dict()

    # print('\nCounties:\n', main.counties)
    # print('\nCities:\n', main.cities)
    # print('\nCity Numbers:\n', main.city_nums)
    # print('\nBlock Numbers:\n', main.block_num)
    # print('\nNested Dict:\n', main.nested_dict())
