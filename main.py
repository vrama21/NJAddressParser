"""
TODO: Create a City:Zip dict for parameters to pass
TODO: Create 'City'.csv files for each city to parse faster
"""

import csv
import pandas as pd
import numpy as np
import collections


class Main:

    def __init__(self, *args):
        # self.zip_codes = collections.OrderedDict(
        #     {'Pleasantville': '08232',
        #       'Absecon': '08201',
        #       'Egg Harbor Township': '08234',
        #       'Galloway': '08205',
        #       'Northfield': '08225'
        #     })

        self.zip_codes = ['08232', '08201', '08205', '08234', '08225']
        self.num = []
        self.addr = []
        self.city = []
        self.zips = []

        # self.zip_list = list(self.zip_codes)
        self.parse_statewide(str(self.zip_codes[0]), *args)
        # self.parse_statewide(iter(self.zip_codes.values()[0]))

    def parse_statewide(self, zip_code, *args):
        print('Parsing statewide.csv ...')

        with open('statewide.csv', 'r') as csvfile:
            readcsv = csv.reader(csvfile, delimiter=',')

            for row in readcsv:
                num_column = row[2]
                add_column = row[3]
                city_column = row[5]
                zip_code_column = row[8]

                if zip_code in zip_code_column:
                    self.num.append(num_column)
                    self.addr.append(add_column)
                    self.city.append(city_column)
                    self.zips.append(zip_code_column)

        print('Parsing complete')
        # self.write_csv_file('Pleasantville.csv')
        self.create_dataframe(*args)

    def create_dataframe(self, *args):
        df = pd.DataFrame({'Address': self.num,
                           'Street': self.addr,
                           'City': self.city,
                           'Zip Code': self.zips})

        # Remove rows with empty City string
        df['City'].replace('', np.nan, inplace=True)
        df.dropna(subset=['City'], inplace=True)

        df.sort_values('Address', inplace=True)
        pd.set_option('display.max_rows', 10000)

        print(df)
        # TODO: Find why args isn't being passed in
        # if args == '':
        #     print(df)
        # else:
        #     print(df[df['Street'].str.contains(str(args))])
        # if args is not None:
        #     print(df[df['Street'].str.contains(str(args))])
        # else:
        #     print(df)

    def write_csv_file(self, csvfilename):
        with open(csvfilename, 'w') as csvfile:
            writecsv = csv.writer(csvfile, delimiter=' ')
            writecsv.writerows(self.add_num)


if __name__ == '__main__':
    Main()
