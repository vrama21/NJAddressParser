import os.path
from collections import OrderedDict

base_dir = os.path.dirname(os.path.realpath(__file__))
csv_dir = base_dir + '\CSV'
json_dir = base_dir + '\JSON'

zip_dict = OrderedDict([
    ('08232', 'Pleasantville'),
    ('08234', 'Egg Harbor Township'),
    ('08201', 'Absecon'),
    ('08205', 'Galloway'),
    ('08225', 'Northfield')])