import os
import csv
import pandas as pd
import numpy as np
from collections import OrderedDict


class CreateCSV:

    cur_dir = os.getcwd()
    csv_dir = cur_dir + '\CSV'
    csv_file_dir = os.path.join(csv_dir, )

    zip_dict = OrderedDict([
        ('08232', 'Pleasantville'),
        ('08234', 'Egg Harbor Township'),
        ('08201', 'Absecon'),
        ('08205', 'Galloway'),
        ('08225', 'Northfield')])

    def __init__(self):

        self.addr = []
        self.unit = []
        self.strt = []
        self.city = []
        self.zips = []

        self.parse_statewide(*self.zip_dict.keys())

    def parse_statewide(self, *args):
        print("Function 'parse_statewide' args = {}".format(args))
        print('Parsing statewide.csv with zip code {}...'.format(args))

        statewide_file_path = self.csv_file_path('statewide.csv')

        with open(statewide_file_path, 'r') as _statewide_csv:
            readcsv = csv.reader(_statewide_csv, delimiter=',')

            for row in readcsv:
                addr_column = row[2]
                strt_column = row[3]
                city_column = row[5]
                zips_column = row[8]

                for _zip in args:
                    if _zip in zips_column:
                        self.addr.append(addr_column)
                        self.strt.append(strt_column)
                        self.city.append(city_column)
                        self.zips.append(zips_column)

        # Clean up extra blank spaces between addresses
        self.strt = [' '.join(x.split()) for x in self.strt]
        # Remove text after whitespace (e.g. '1/2', 'Unit A')
        self.addr = [(x.split(' ', 1)[0]) for x in self.addr]

        print('Parsing complete')
        self.create_dataframe()

    def create_dataframe(self):
        d = {'Address': self.addr,
             # 'Unit': self.unit
             'Street': self.strt,
             'City': self.city,
             'Zip Code': self.zips}

        self.df = pd.DataFrame(data=d)

        # Remove rows with empty City string
        self.df['City'].replace('', np.nan, inplace=True)
        self.df.dropna(subset=['City'], inplace=True)

        print(self.df)

        self.delete_existing()

        self.write_csv_files()

    def csv_file_path(self, csv_file):
        return os.path.join(self.csv_dir, csv_file)

    def write_csv_files(self):
        # Create CSV Folder
        create_csv_dir = os.path.join(self.cur_dir, r'CSV')
        if not os.path.exists(create_csv_dir):
            os.makedirs(create_csv_dir)

        # df.style.set_properties(**{'text align': 'right'})

        print('Writing {} into CSV files...'.format(self.zip_dict.values()))

        os.chdir(self.csv_dir)
        for _zip, _city in self.zip_dict.items():
            write_path = open(_city + '.csv', 'w')
            df_by_city = self.df.loc[self.df['Zip Code'] == _zip]
            df_by_city.to_csv(write_path, index=False)

    def delete_existing(self):
        os.chdir(self.csv_dir)
        print('Deleting any pre-exisiting CSV Files...')

        for existing_file in self.zip_dict.values():
            if os.path.exists(existing_file + '.csv'):
                os.remove(existing_file + '.csv')


if __name__ == '__main__':
    CreateCSV()

