import os.path
from collections import OrderedDict

base_dir = os.path.dirname(os.path.realpath(__file__))
csv_dir = base_dir + '\csv'
csv_source_dir = csv_dir + '\source'
csv_parsed_dir = csv_dir + '\parsed'
csv_clean_dir = csv_dir + '\clean'
csv_updated_dir = csv_dir + r'\updated'
json_dir = base_dir + '\json'

zip_dict = OrderedDict([
    ('08232', 'Pleasantville'),
    ('08234', 'Egg Harbor Township'),
    ('08201', 'Absecon'),
    ('08205', 'Galloway'),
    ('08225', 'Northfield')])