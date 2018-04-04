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
        self.df = self.csv_to_dataframe()
        self.write_csv_files(*zip_dict.keys())

    @timefunc
    def parse_statewide(self, source_csv, *args):
        """
        Selects the main source csv file to parse all the data from and parses through it
        by specified zip codes to extract specified data.
        """

        print('Parsing {} with these specified arguments {}...'.format(source_csv, args))

        source_csv_path = os.path.join(csv_source_dir, source_csv)
        with open(source_csv_path, 'r') as source_csv_reader:
            readcsv = csv.reader(source_csv_reader, delimiter=',')

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

    def csv_to_dataframe(self):
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

    def write_csv_files(self, *args):
        print('Writing {} into CSV files...'.format(args))

        for keys, values in zip_dict.items():
            csv_file_path = os.path.join(csv_parsed_dir, values)
            write_path = open(csv_file_path + '.csv', 'w')

            df_by_city = self.df.loc[self.df['Zip Code'] == keys]
            df_by_city.to_csv(write_path, index=False)

        return


if __name__ == '__main__':
    res = Parser(source_csv='statewide.csv')
