import snowfall
from traffic import traffic_data
import ast

import pandas as pd
snow_df = pd.read_csv("Ski-Search/3-21-snowreport.csv")

ski_resorts = snowfall.df['title_short'].tolist()

def get_crashes():
    return ['I-70mm_50', 'I-70mm_70']

def get_traffic_cost(location):
    location_df = traffic_data[traffic_data['location'] == location]
    delay = location_df['delay'].astype(int).iloc[0]

    cost = 0

    if location in get_crashes():
        cost += 100

    if delay < 5:
        cost += 0
    elif delay < 15:
        cost += 4
    elif delay < 30:
        cost += 12
    elif delay < 60:
        cost += 20
    elif delay < 90:
        cost += 30
    else:
        cost += 50
    
    return cost

def get_snowfall_cost(resort):
    df = snow_df[snow_df['title_short'] == resort]
    snowfall_24hr = df['snow'][0]
    snowfall_24hr = ast.literal_eval(snowfall_24hr)['last24']

    cost = 0
    
    if snowfall_24hr == 0:
        cost += 50
    elif snowfall_24hr < 2:
        cost += 20
    elif snowfall_24hr < 4:
        cost += 10
    elif snowfall_24hr < 6:
        cost += 5
    elif snowfall_24hr < 10:
        cost += 2
    else:
        cost += 0

    return cost

def get_heuristic(x, y):
    if x in ski_resorts:
        x_cost = get_snowfall_cost(x)
    else:
        x_cost = get_traffic_cost(x)
    
    if y in ski_resorts:
        y_cost = get_snowfall_cost(y)
    else:
        y_cost = get_traffic_cost(y)
    
    return x_cost + y_cost


def get_cost(x):
    if x == 'Colorado State University':
        x_cost = 0
    elif x in ski_resorts:
        x_cost = get_snowfall_cost(x)
    else:
        x_cost = get_traffic_cost(x)
    return x_cost

print('the heuristic of to Arapahoe Basin from I-70mm_10 is', get_heuristic('Arapahoe Basin', 'I-70mm_10'))
print('the cost of I-25mm_50 is', get_cost('I-25mm_50'))
print('the cost of Colorado State University is', get_cost('Colorado State University'))