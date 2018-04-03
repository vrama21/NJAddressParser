import os
import csv
import pandas as pd
import numpy as np
from constants import *
from time_dec import *

"""
Source csv data is gathered from www.OpenAddresses.io
Parser creates a per-city csv from state-wide or county-wide csv files

"""


class Parser:

    def __init__(self, source_csv=None):

        self.long = []
        self.lati = []
        self.addr = []
        self.unit = []
        self.strt = []
        self.city = []
        self.zips = []

        self.parse_statewide(source_csv, *zip_dict.keys())
        self.df = self.create_dataframe()

        self.main()

    def parse_statewide(self, source_csv, *args):
        print("Function 'parse_statewide' args = {}".format(args))
        print('Parsing statewide.csv with zip code {}...'.format(args))

        with open(source_csv, 'r') as _source_csv_path:
            readcsv = csv.reader(_source_csv_path, delimiter=',')

            for row in readcsv:
                long_column = row[0]
                lati_column = row[1]
                addr_column = row[2]
                strt_column = row[3]
                city_column = row[5]
                zips_column = row[8]

                for _zip in args:
                    if _zip in zips_column:
                        self.long.append(long_column)
                        self.lati.append(lati_column)
                        self.addr.append(addr_column)
                        self.strt.append(strt_column)
                        self.city.append(city_column)
                        self.zips.append(zips_column)

        self.addr = [x.split() for x in self.addr]
        for i in self.addr:
            try:
                self.unit.append(i[1])
            except IndexError:
                self.unit.append('')
        self.addr = [''.join(x[0]) for x in self.addr]

        print('Parsing complete')

        return

    def create_dataframe(self):
        d = {'Address': self.addr,
             'Unit': self.unit,
             'Street': self.strt,
             'City': self.city,
             'Zip Code': self.zips,
             'Latitude': self.lati,
             'Longitude': self.long}

        df = pd.DataFrame(data=d)

        df['City'].replace('', np.nan, inplace=True)
        df.dropna(subset=['City'], inplace=True)

        cols = ['Address', 'Unit', 'Street', 'City', 'Zip Code', 'Latitude', 'Longitude']
        df = df[cols]

        return df

    def write_csv_files(self):
        print('Writing {} into CSV files...'.format(zip_dict.values()))

        for keys, values in zip_dict.items():
            csv_file_path = os.path.join(csv_dir, values)
            write_path = open(csv_file_path + '.csv', 'w')

            df_by_city = self.df.loc[self.df['Zip Code'] == keys]
            df_by_city.to_csv(write_path, index=False)

        return

    def main(self):
        self.write_csv_files()


if __name__ == '__main__':
    Parser(source_csv='statewide.csv')
