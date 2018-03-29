import os
import pandas as pd
import re
import json

cur_dir = os.getcwd()
csv_dir = cur_dir + '\CSV'
json_dir = cur_dir + '\JSON'


class Cleanup:

    def __init__(self, city):
        self.city = city
        self.df = self.get_df(city)
        self.json_string = self.load_json()

        # print(self.json_string[city].items())
        self.edit_df(city)

    def csv_dir_write(self, city):
        csv_write = os.path.join(csv_dir, '_' + city + '.csv')
        return csv_write

    def get_df(self, city):
        csv_file_path = os.path.join(csv_dir, city)

        with open(csv_file_path + '.csv', 'r', encoding='utf-8') as _csv_file:
            df = pd.read_csv(_csv_file, converters={'Zip Code': lambda x: str(x),
                                                    'Address': lambda x: int(x)
                                                    })
        return df

    def print_df(self):
        street_group = self.df.groupby('Street')
        for name, group in street_group:
            print('\n', name)
            print(group)

    def load_json(self):
        json_file_path = os.path.join(json_dir, 'general_edits.json')
        json_data = open(json_file_path, 'r').read()
        json_string = json.loads(json_data)

        return json_string

    def edit_df(self, city):
        for edits in self.json_string[city]['Edits']:
            print(edits)
            for key, value in edits.items():
                self.df['Street'] = [x.replace(key, value) for x in self.df['Street']]

        for removals in self.json_string[city]['Removals']:
            self.df = self.df[self.df['Street'].str.contains(removals) == False]

        pd.set_option('display.max_rows', None)
        self.df.sort_values(['Street'], inplace=True)

        write_path = open(self.csv_dir_write(city), 'w')

        street_unique = self.df['Street'].unique()

        # Sort numerically for each sorted address
        for unique in street_unique:
            a = self.df[self.df['Street'].str.contains(unique)]
            a.sort_values('Address', inplace=True)
            a.to_csv(write_path, index=False)

        self.print_df()
        # street_group = df.groupby('Street')
        # for group in street_group:
            # group.to_csv(write_path, index=False)


if __name__ == '__main__':
    Cleanup('Absecon')
