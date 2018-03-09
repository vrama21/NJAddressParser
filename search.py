import os
import pandas as pd


class Search:

    cur_dir = os.getcwd()
    csv_dir = cur_dir + '\CSV'

    def __init__(self, *args, **kwargs):
        self.search(*args, **kwargs)

    def dataframe(self, filename):
        os.chdir(self.csv_dir)

        with open(filename, 'r'):
            csv = pd.read_csv(filename, sep=',', converters={'Zip Code': lambda x: str(x)})
            df = pd.DataFrame(csv, index=None)

        return df

    def search(self, filename, street=None, sort=None, maxrows=None):
        df = self.dataframe(filename)

        if maxrows is True:
            pd.set_option('display.max_rows', len(df.index))

        if sort is True:
            df = df.sort_values(by='Address')

        if street is None:
            print(df)
        else:
            df_street = df[df['Street'].str.contains(street)]
            print(df_street)
            min = df_street.groupby('Street')['Address'].transform('min')
            max = df_street.groupby('Street')['Address'].transform('max')
            print(min)
            print(max)

if __name__ == '__main__':
    Search('Pleasantville.csv', street='Linden Ave', maxrows=True, sort=True)

