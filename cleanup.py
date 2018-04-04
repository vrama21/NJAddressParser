import os
import pandas as pd
import json
from constants import *
from search import *
from time_dec import *


class Cleanup:

    def __init__(self, city):
        self.city = city
        self.city_csv = city + '.csv'

        self.df = self.get_df(self.city_csv)

        self.json_string = self.load_json()
        self.prefix_dict = self.json_string['Prefix']
        self.suffix_dict = self.json_string['Suffix']
        self.edit_dict = self.json_string[city]['Edits']
        self.removal_dict = self.json_string[city]['Removals']

        self.main()

    def csv_write(self):
        """
        Writes csv file from initial data parsed from parser
        and commits all the edits
        """

        self.edit_df()
        self.df.sort_values(['Street', 'Address'], inplace=True)

        csv_write_path = os.path.join(csv_clean_dir, self.city_csv)

        try:
            write_path = open(csv_write_path, 'w')
            self.df.to_csv(write_path, index=False)
        except PermissionError:
            raise PermissionError("The file is currently open in another program. Please close"
                                  " that program and re-run the search.")

    def csv_update(self):
        """
        Updates the clean csv based on any changes made on the clean csv file
        """

        _df = self.get_df(self.city_csv)
        _df.sort_values(['Street', 'Address'], inplace=True)

        csv_write_path = os.path.join(csv_dir, self.city_csv)

        try:
            write_path = open(csv_write_path, 'w')
            _df.to_csv(write_path, index=False)
        except PermissionError:
            raise PermissionError("The file is currently open in another program. Please close"
                                  " that program and re-run the search.")

    def get_df(self, csv_file):
        csv_file_path = os.path.join(csv_parsed_dir, csv_file)

        with open(csv_file_path,  'r', encoding='utf-8') as _csv_file:
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

    def edit_df(self):
        # _search = Search(self)
        for key, value in self.prefix_dict.items():
            self.df['Street'] = self.df['Street'].str.replace('^{}\s\s'.format(key), value)

        for key, value in self.suffix_dict.items():
            self.df['Street'] = self.df['Street'].str.replace('{}$'.format(key), value)

        for key, value in self.edit_dict.items():
            self.df['Street'] = self.df['Street'].str.replace('^{}$'.format(key), value)

        for removals in self.removal_dict:
            self.df = self.df[self.df['Street'].str.contains(removals) == False]

        self.df['City'] = [x.title() for x in self.df['City']]

        self.df.drop_duplicates(subset=['Address', 'Unit', 'Street'], inplace=True)

        # _search.print_df_by_col_group('Street')

    def main(self):
        self.csv_write()
        # self.csv_update()


if __name__ == '__main__':
    Cleanup(city='Pleasantville')
