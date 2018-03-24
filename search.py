import os
import pandas as pd
import numpy as np


class Search:

    cur_dir = os.getcwd()
    csv_dir = cur_dir + '\CSV'

    def __init__(self, csv_file, csv_data=None, street=None, maxrows=None):

        self.csv_file = csv_file
        self.street = street
        self.maxrows = maxrows
        self.csv_data = csv_data

        self.search()

    def dataframe(self):
        os.chdir(self.csv_dir)

        with open(self.csv_file, 'r') as _csv_file:
            self.csv_data = pd.read_csv(_csv_file, sep=',',
                                        converters={'Zip Code': lambda x: str(x),
                                                    'Address': lambda x: int(x)
                                                    })

            self.df = pd.DataFrame(self.csv_data, index=None)
            self.df.sort_values(by='Address')

            return self.df

    def dataframe_analysis(self):
        self.street_unique = self.df['Street'].unique()

        _data = {'Street': self.street_unique,
                 'Count': self.address_count(),
                 # 'Minumum': np.nan,
                 # 'Maximum': np.nan,
                 }

        df2 = pd.DataFrame(_data, index=None)

        df2.sort_values(by='Street')

        # self.df2['Count'] = self.df2['Street'].apply(self.count)

        pd.set_option('display.max_rows', -1)

        return df2

    def address_count(self):
        """
        Grabs main dataframe (self.df) and searches each row in the column ('Street')
        for specific a string and returns the count of each specific address.
        """

        for unique in self.street_unique:
            a = self.df[self.df['Street'].str.contains(unique)]
            # print('{} has a total of {}'.format(unique, a.count().sum()))
            return a.count().sum()

    def min_value(self, dataframe):
        for addr in self.street_unique:
            loc = self.df[self.df['Street'].str.contains(addr)]
            minimum = np.nanmin(self.df.iloc[:, 0].values)

            return minimum

    def max_value(self, dataframe):
        maximum = np.nanmax(dataframe.iloc[:, 0].values)
        return maximum

    def search(self):
        self.dataframe()
        self.dataframe_analysis()
        self.address_count()

        pd.set_option('display.max_rows', -1)

        if self.street is not None:
            df_street = self.df[self.df['Street'].str.contains(self.street)]
            df_street = df_street.sort_values(by='Address')

            # minimum = self.min_value(df_street)
            # maximum = self.max_value(df_street)
            #
            # print('Min for {} is... {}'.format(self.street, minimum))
            # print('Max for {} is... {}'.format(self.street, maximum))
            print(df_street)
        else:
            print(self.df)


if __name__ == '__main__':
    Search('Pleasantville.csv')

