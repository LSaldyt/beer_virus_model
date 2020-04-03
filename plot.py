from read import read
from pprint import pprint

from pandas import DataFrame
from collections import defaultdict

from urllib.request import urlopen

import plotly.express as px

import json, os, pickle

from math import log, copysign

def load_counties(filename='fips.json.cache', source='https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json'):
    if not os.path.isfile(filename):
        with urlopen(source) as response:
            counties = json.load(response)
        with open(filename, 'wb') as outfile:
            pickle.dump(counties, outfile)
    else:
        with open(filename, 'rb') as infile:
            counties = pickle.load(infile)
    return counties


def transform():
    regions, us = read()
    meta = us['meta']

    long_form = defaultdict(list)

    for key, data in us.items():
        if key in meta:
            metadata = meta[key]
            fips = metadata['fips']
            population = int(metadata['population'])

            if fips.strip() == '':
                continue
            if population == 0:
                continue

            county, state, *rest = key
            data = us[key]

            confirmed = data['confirmed_US']
            dead      = data['deaths_US']

            today     = confirmed[-1]
            yesterday = confirmed[-2]
            two_days  = confirmed[-3]

            delta   = today - yesterday
            d_delta = yesterday - two_days

            if d_delta == 0:
                change_ratio = 0.0
            else:
                change_ratio = delta / d_delta

            percent           = today / population
            percent_yesterday = yesterday / population
            percent_delta     = percent - percent_yesterday

            custom = change_ratio / log(population, 10)
            
            fips = str(int(float(fips)))
            if len(fips) == 4:
                fips = '0' + fips
            long_form['county'].append(county)
            long_form['state'].append(state)
            long_form['fips'].append(fips)
            long_form['today'].append(today)
            long_form['yesterday'].append(yesterday)
            long_form['two_days'].append(two_days)
            long_form['dead'].append(dead[-1])
            long_form['delta'].append(delta)
            long_form['change_ratio'].append(change_ratio)
            long_form['percent'].append(percent)
            long_form['percent_yesterday'].append(percent_yesterday)
            long_form['percent_delta'].append(percent_yesterday)
            long_form['custom'].append(custom)
    return DataFrame(long_form)

def plot(df):
    counties = load_counties()
    fig = px.choropleth_mapbox(df, geojson=counties, locations='fips', color='change_ratio',
                               color_continuous_scale="Viridis",
                               range_color=(0, 2.0),
                               mapbox_style="carto-positron",
                               zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                               opacity=0.4,
                               hover_data=['county', 'state', 'today', 'yesterday', 'two_days', 'delta', 'change_ratio', 'percent', 'percent_yesterday', 'percent_delta']
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.write_html('map.html', auto_open=True)
    fig.show()

def main():
    df = transform()
    print(df)
    plot(df)

if __name__ == '__main__':
    main()

