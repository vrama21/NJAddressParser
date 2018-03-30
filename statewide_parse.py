import os
import csv
import pandas as pd
import numpy as np
from config import *
from collections import OrderedDict


class StatewideParse:

    def __init__(self):

        self.long = []
        self.lati = []
        self.addr = []
        self.unit = []
        self.strt = []
        self.city = []
        self.zips = []

        self.parse_statewide(zip_dict.keys())
        self.df = self.create_dataframe()
        self.write_csv_files()

    def parse_statewide(self, *args):
        print("Function 'parse_statewide' args = {}".format(args))
        print('Parsing statewide.csv with zip code {}...'.format(args))

        statewide_file_path = os.path.join(csv_dir, 'statewide.csv')

        with open(statewide_file_path, 'r') as _statewide_csv:
            readcsv = csv.reader(_statewide_csv, delimiter=',')

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

        print('Parsing complete')

        return

    def create_dataframe(self):
        d = {'Address': self.addr,
             'Street': self.strt,
             'City': self.city,
             'Zip Code': self.zips,
             'Latitude': self.lati,
             'Longitude': self.long}

        df = pd.DataFrame(data=d)

        # Remove rows with empty City string and drop np.nan
        df['City'].replace('', np.nan, inplace=True)
        df.dropna(subset=['City'], inplace=True)

        # Clean up extra blank spaces between addresses
        df['Street'] = [' '.join(x.split()) for x in df['Street']]

        # Remove text after whitespace (e.g. '1/2', 'Unit A')
        df['Address'] = [(x.split(' ', 1)[0]) for x in df['Address']]

        # Lowercase everything after first letter in the city
        df['City'] = [x[0] + x[1:].lower() for x in df['City']]

        # Set the column order
        cols = ['Address', 'Street', 'City', 'Zip Code', 'Latitude', 'Longitude']
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


if __name__ == '__main__':
    StatewideParse()
