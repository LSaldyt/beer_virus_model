from collections import defaultdict
from pprint import pprint

import csv

BASEDIR  = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
BASEFILE = BASEDIR + 'time_series_19-covid-{}.csv'
LABELS   = ['Confirmed', 'Deaths', 'Recovered']

def read_labeled(label):
    regions = dict()
    filename = BASEFILE.format(label)
    with open(filename, 'r') as infile:
        label_reader = csv.reader(infile, delimiter=',', quotechar='"')
        headers = next(label_reader)
        dates = headers[4:]
        for row in label_reader:
            province, country, _, _, *counts = row
            try:
                counts = list(map(int, counts))
            except ValueError:
                print(headers)
                print(row)
            regions[(province, country)] = counts
    return regions, dates

def read():
    regions = defaultdict(dict)
    for label in LABELS:
        label_regions, dates = read_labeled(label)
        for region_name, counts in label_regions.items():
            regions[region_name][label] = counts
    return regions

def main():
    pprint(read())

if __name__ == '__main__':
    main()
