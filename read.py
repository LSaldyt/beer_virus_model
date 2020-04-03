from collections import defaultdict
from pprint import pprint

import csv

BASEDIR  = 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/'
BASEFILE = BASEDIR + 'time_series_covid19_{}.csv'
LABELS   = ['confirmed_global', 'confirmed_US', 'deaths_global', 'deaths_US', 'recovered_global']

def read_US(label):
    regions = dict()
    meta = dict()
    filename = BASEFILE.format(label)
    with open(filename, 'r') as infile:
        label_reader = csv.reader(infile, delimiter=',', quotechar='"')
        headers = next(label_reader)
        dates = headers[12:]
        for row in label_reader:
            _, _, _, _, fips, county, state, region, lat, lng, _, pop, *counts = row
            try:
                counts = list(map(int, counts))
            except ValueError:
                print(counts)
                print(headers)
                print(dates)
                print(row)
            regions[(county, state, region)] = counts
            meta[(county, state, region)] = dict(fips=fips, county=county, state=state, region=region, lat=lat, lng=lng, population=pop)
    return regions, dates, meta

def read_global(label):
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
    return regions, dates, None

def read():
    regions = defaultdict(dict)
    us      = defaultdict(dict)
    for label in LABELS:
        reader = read_US if 'US' in label else read_global
        output = us      if 'US' in label else regions
        
        label_regions, dates, meta = reader(label)
        for region_name, counts in label_regions.items():
            output[region_name][label] = counts
        if meta is not None:
            output['meta'] = meta
    return regions, us

def main():
    data = read()

if __name__ == '__main__':
    main()
