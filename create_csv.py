"""
TODO: Create 'City'.csv files for each city to parse faster
"""

import os
import csv
import pandas as pd
import numpy as np
from collections import OrderedDict


class CreateCSV:

    def __init__(self):
        self.zip_dict = OrderedDict([
            ("08232", 'Pleasantville'),
            ("08234", 'Egg Harbor Township'),
            ("08201", 'Absecon'),
            ("08205", 'Galloway'),
            ("08225", 'Northfield')])

        self.zip_code_keys = list(self.zip_dict.keys())
        self.zip_code_values = list(self.zip_dict.values())

        self.nums = []
        self.addr = []
        self.city = []
        self.zips = []

        self.parse_statewide(*self.zip_code_keys)

    def parse_statewide(self, *args):
        print("Function 'parse_statewide' args = {}".format(args))
        print('Parsing statewide.csv with zip code {}...'.format(args))

        with open('statewide.csv', 'r') as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')

            for row in readcsv:
                nums_column = row[2]
                addr_column = row[3]
                city_column = row[5]
                zips_column = row[8]

                for _zip in args:
                    if _zip in zips_column:
                        self.nums.append(nums_column)
                        self.addr.append(addr_column)
                        self.city.append(city_column)
                        self.zips.append(zips_column)

        print('Parsing complete')
        print('Writing {} file...'.format(self.zip_code_values))

        self.create_dataframe()

    def create_dataframe(self):
        df = pd.DataFrame({'Address': self.nums,
                           'Street': self.addr,
                           'City': self.city,
                           'Zip Code': self.zips})

        # Remove rows with empty City string
        df['City'].replace('', np.nan, inplace=True)
        df.dropna(subset=['City'], inplace=True)

        # df.sort_values('Address', inplace=True)
        # pd.set_option('display.max_rows', len(self.addr))

        for _city in self.zip_dict.values():
            if os.path.exists(_city):
                os.remove(_city)

            for _zip_match in self.zip_dict.keys():
                path = open(_city + '.csv', 'w')
                match = df['Zip Code'] == _zip_match
                match.to_csv(path, index=False)

        # for _city in self.zip_code_values:
        #     if os.path.exists(_city):
        #         os.remove(_city)
        #
        #     for _zip in self.zip_code_keys:
        #         path = open(_city + '.csv', 'w')
        #         df.to_csv(path, index=False)


if __name__ == '__main__':
    CreateCSV()

