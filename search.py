import os
import pandas as pd


cur_dir = os.getcwd()
csv_dir = cur_dir + '\CSV'
street_list = []


def search(filename, sort=None, maxrows=None):
    os.chdir(csv_dir)

    with open(filename, 'r'):
        csv = pd.read_csv(filename, sep=',')
        df = pd.DataFrame(csv)

        street_list.append(set(df['Street']))

        if maxrows is True:
            pd.set_option('display.max_rows', len(df.index))

        if sort is True:
            add_data = df['Address']
            add_data.astype('int')
            df.sort_values(by='Address', axis=1)
            # pass

        # print(df)

        return df


def locate_min_max():
    for i in street_list:
        print(i['Address'])


if __name__ == '__main__':
    search('Pleasantville.csv', maxrows=True)
    # locate_min_max()
