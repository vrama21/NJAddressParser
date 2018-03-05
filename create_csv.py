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

        self.nums = []
        self.addr = []
        self.city = []
        self.zips = []

        self.parse_statewide(*self.zip_dict.keys())

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

        self.create_dataframe()

    def create_dataframe(self):
        d = {'Address': self.nums,
             'Street': self.addr,
             'City': self.city,
             'Zip Code': self.zips}

        df = pd.DataFrame(data=d)

        # Remove rows with empty City string
        df['City'].replace('', np.nan, inplace=True)
        df.dropna(subset=['City'], inplace=True)

        self.delete_existing()

        cur_dir = os.getcwd()
        csv_dir = cur_dir + '\CSV'
        create_csv_dir = os.path.join(cur_dir, r'CSV')
        if not os.path.exists(create_csv_dir):
            os.makedirs(create_csv_dir)

        # df.style.set_properties(**{'text align': 'right'})

        print('Writing {} into CSV files...'.format(self.zip_dict.values()))

        os.chdir(csv_dir)
        for _zip, _city in self.zip_dict.items():
            write_path = open(_city + '.csv', 'w')
            df_by_city = df.loc[df['Zip Code'] == _zip]
            df_by_city.to_csv(write_path, index=False)

    def delete_existing(self):
        print('Deleting any pre-exisiting CSV Files...')

        for existing_file in self.zip_dict.values():
            if os.path.exists(existing_file + '.csv'):
                os.remove(existing_file + '.csv')


if __name__ == '__main__':
    CreateCSV()

