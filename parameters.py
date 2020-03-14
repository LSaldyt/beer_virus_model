from read import read
from pprint import pprint

def estimate_parameters_by_region(regions, region_name):
    parameters = dict()

    count_dict = regions[region_name]
    confirmed  = count_dict['Confirmed']
    recovered  = count_dict['Recovered']
    dead       = count_dict['Deaths']

    parameters['confirmed_infection_rates'] = [(confirmed[i] - confirmed[i - 1]) / confirmed[i - 1] for i in range(1, len(confirmed))]
    parameters['time_delay_death_rates']    = [(dead[i] - dead[i - 1]) / confirmed[i - 14] for i in range(14, len(confirmed))]
    parameters['naive_death_rates']         = [(dead[i] - dead[i - 1]) / confirmed[i] for i in range(1, len(confirmed))]
    parameters['time_delay_recovery_rates'] = [(recovered[i] - recovered[i - 1]) / confirmed[i - 14] for i in range(14, len(confirmed))]
    
    length = len(confirmed)

    parameters['infection_rate'] = sum(parameters['confirmed_infection_rates']) / length
    parameters['recovery_rate']  = sum(parameters['time_delay_recovery_rates']) / length
    parameters['death_rate']     = sum(parameters['time_delay_death_rates'])    / length


    return parameters

def main():
    regions = read()
    pprint(estimate_parameters_by_region(regions, ('Hubei', 'China')))

if __name__ == '__main__':
    main()
