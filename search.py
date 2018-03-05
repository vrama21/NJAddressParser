import os
import pandas as pd

cur_dir = os.getcwd()


def search(filename, sort=None, maxrows=None):
    with open(filename, 'r'):
        # csv = pd.read_csv(filename, sep=',')
        df = pd.DataFrame.from_csv(filename)

        if maxrows is True:
            pd.set_option('display.max_rows', len(df.index))

        if sort is True:
            # df.sort_values(df, axis=1)
            pass

        print(df.columns.values)
        print(df)


if __name__ == '__main__':
    search('Pleasantville.csv', sort=True)
