import os
import pandas as pd
import re
import json
from config import *
from search import Search


class Cleanup:

    def __init__(self, city):
        self.city = city
        self.df = self.get_df(city)
        self.json_string = self.load_json()
        self.edit_df(city)

    def csv_dir_write(self, city):
        csv_write = os.path.join(csv_dir, city + '_Clean.csv')
        return csv_write

    def get_df(self, city):
        csv_file_path = os.path.join(csv_dir, city)

        with open(csv_file_path + '.csv', 'r', encoding='utf-8') as _csv_file:
            df = pd.read_csv(_csv_file, converters={'Zip Code': lambda x: str(x),
                                                    'Address': lambda x: int(x),
                                                    'Latitude': lambda x: float(x),
                                                    'Longitude': lambda x: float(x)
                                                    })
        return df

    def load_json(self):
        json_file_path = os.path.join(json_dir, 'general_edits.json')
        json_data = open(json_file_path, 'r').read()
        json_string = json.loads(json_data)

        return json_string


    def print_df_by_col_group(self, col):
        col_group = self.df.groupby(col)
        for name, group in col_group:
            print('\n', name)
            print(group)

    def edit_df(self, city):
        prefix_dict = self.json_string['Prefix']
        suffix_dict = self.json_string['Suffix']
        edit_dict = self.json_string[city]['Edits']
        removal_dict = self.json_string[city]['Removals']

        # Selects first word in the selected column
        first_elem = self.df['Street'].str.split().str[0]
        # Selects last word in the selected column
        last_elem = self.df['Street'].str.split().str[-1]
        # Selects every word in between in the selected column
        between_elems = self.df['Street'].str.split().str[1:-1]
        between_elems = [' '.join(x) for x in between_elems]

        # Replace all first words with corresponding prefix
        for key, value in prefix_dict.items():
            first_elem = [x.replace(key, value) for x in first_elem]

        # Replace all last words with corresponding suffix
        for key, value in suffix_dict.items():
            last_elem = [x.replace(key, value) for x in last_elem]

        # Combines the edited first and last words with the words in between
        # and joins them for the selected column
        combine = [x for x in zip(first_elem, between_elems, last_elem)]
        combine = [filter(None, x) for x in combine]
        self.df['Street'] = [' '.join(x) for x in combine]

        for key, value in edit_dict.items():
            self.df['Street'] = [x.replace(key, value) for x in self.df['Street']]

        for removals in removal_dict:
            self.df = self.df[self.df['Street'].str.contains(removals) == False]

        pd.set_option('display.max_rows', None)

        write_path = open(self.csv_dir_write(city), 'w')

        self.df.sort_values(['Street', 'Address'], inplace=True)
        self.df.to_csv(write_path, index=False)
        self.print_df_by_col_group('Street')

        # street_group = df.groupby('Street')
        # for group in street_group:
            # group.to_csv(write_path, index=False)


if __name__ == '__main__':
    Cleanup('Pleasantville')
