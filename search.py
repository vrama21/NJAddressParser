import os
import pandas as pd
import numpy as np


class Search:

    cur_dir = os.getcwd()
    csv_dir = cur_dir + '\CSV'

    def __init__(self, csv_file, street=None):

        self.csv_file = csv_file
        self.street = street
        self.df = self.csv_to_df()
        self.street_unique= self.df['Street'].unique()

        self.search()

    def csv_to_df(self):
        """
        Parse the selected .csv file and return a dataframe to use
        for analysis.
        """
        csv_file_path = os.path.join(self.csv_dir, self.csv_file)

        with open(csv_file_path, 'r', encoding='utf-8') as _csv_file:
            self.df = pd.read_csv(_csv_file, header=0,
                                  converters={'Zip Code': lambda x: str(x),
                                              'Address': lambda x: int(x)
                                              })

            pd.set_option('display.max_rows', None)

            return self.df

    def dataframe_analysis(self):
        """
        Using the main dataframe, returns a new dataframe with:
        (Unique Street, Total Addresses, Min, Max)
        """

        _count = self.address_count()
        _min = self.min_value()
        _max = self.max_value()

        _data = {'Street': self.street_unique,
                 'Count': _count,
                 'Minimum': _min,
                 'Maximum': _max,
                 }

        df2 = pd.DataFrame(_data, index=None)
        df2.sort_values(by='Street', inplace=True)

        # Reorder columns
        cols = ['Street', 'Count', 'Minimum', 'Maximum']
        pd.set_option('display.max_rows', None)
        print(df2[cols])

    def address_count(self):
        """
        Grabs main dataframe (self.df) and searches each row in the column ('Street')
        for specific a string and returns the count of each specific address.
        """
        _count = []

        for unique in self.street_unique:
            a = self.df['Street'[self.df['Street'].str.contains(unique)].count().sum()]
            _count.append(a)
        return _count

    def min_value(self):
        """
        Returns the minimum value of a range of addresses
        """

        _minimum = []
        for addr in self.street_unique:
            loc = self.df[self.df['Street'].str.contains(addr)]
            _min = np.nanmin(loc.iloc[:, 0].values)
            _minimum.append(_min)

        return _minimum

    def max_value(self):
        """
        Returns the maximum value of a range of addresses
        """

        _minimum = []

        for addr in self.street_unique:
            loc = self.df[self.df['Street'].str.contains(addr)]
            _max = np.nanmax(loc.iloc[:, 0].values)
            _minimum.append(_max)

        return _minimum

    def search(self):
        self.dataframe_analysis()

        if self.street is not None:
            df_street = self.df[self.df['Street'].str.contains(self.street)]
            df_street = df_street.sort_values(by='Address')

            print(df_street)
        else:
            # print(self.df)
            pass


if __name__ == '__main__':
    result = Search(csv_file='_Pleasantville.csv')
