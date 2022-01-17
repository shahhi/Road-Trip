#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name : Himani Shah # IU ID : shahhi@iu.edu
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#
# !/usr/bin/env python3
import pandas as pd
import sys
from queue import PriorityQueue
import pdb

from math import dist, radians, cos, sin, asin, sqrt, tan, tanh
import numpy as np
#### Source : https://towardsdatascience.com/heres-how-to-calculate-distance-between-2-geolocations-in-python-93ecab5bbba4
def haversine_distance(lat1, lon1, lat2, lon2):
   r = 6371
   phi1 = np.radians(lat1)
   phi2 = np.radians(lat2)
   delta_phi = np.radians(lat2 - lat1)
   delta_lambda = np.radians(lon2 - lon1)
   a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) *   np.sin(delta_lambda / 2)**2
   res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))
   
   return np.round(res, 2)
#### From line 18 to 29 have taken from Source link

def heuristic_cost(city,end_city,r_dict,cost,distance,curr_distance,time,distances,speed,delivery,segments):
    if city not in r_dict.keys():
        lat1 = 40.367484
        lon1 = -90.193849
    else:
        lat1 = r_dict[city][0]
        lon1 = r_dict[city][1]
    lat2 = r_dict[end_city][0]
    lon2 = r_dict[end_city][1]

    heuristic_function= haversine_distance(lat1, lon1, lat2, lon2) 
    if cost == "segments":
        # print("inside segments")
        cost_function = segments_cal(segments)
        heuristic = heuristic_function*(0.01) + cost_function

    elif cost == "distance":
        # print("inside distance")
        cost_function =dictance_cal(distance,curr_distance)
        heuristic = heuristic_function*(0.01) + cost_function

    elif cost == "time":
        # print("inside time")
        cost_function =time_cal(time,distances,speed)
        heuristic = heuristic_function*(0.001) + cost_function

    elif cost == "delivery":
        # print("inside delivery")
        cost_function = delivery_time(time,delivery,distances,speed)
        heuristic = heuristic_function*(0.001) + cost_function

    
    return heuristic
    
def dictance_cal(distance,curr_distance):
    return distance + curr_distance 

def segments_cal(segments):
    return segments + 1

def time_cal(time,distances,speeds):
    return time + (distances/speeds)

def delivery_time(time,delivery,distances,speeds):
    if speeds >= 50:
        p = np.tanh(distances/1000)
    else:
        p = 0
    return  delivery + distances/speeds + (p*2*time) +(p*2*distances)/speeds

def get_route(start, end, cost):
    gps = pd.read_csv("city-gps.txt",sep=" ",header= None, names = ["city", "latitude", "longitude"])
    df = pd.read_csv("road-segments.txt",sep=" ", header= None, names = ["firstCity", "secondCity", "length","speedLimit", "nameOfHighway"])
    # print("**********************",gps.median(axis=0))
    records = gps.to_dict(orient="records")
    col1='firstCity'
    col2='secondCity'
    df1 = df[[col1 if col == col2 else col2 if col == col1 else col for col in df.columns]]
    df1 = df1.rename({'secondCity': 'firstCity', 'firstCity': 'secondCity'}, axis=1)  
    roadSegments = df1.append(df, ignore_index=True, sort=False)
    recs = roadSegments.to_dict(orient="records")
    r_dictionary = {}
    r_dict = {}
    for i in recs:
        if i['firstCity'] in r_dictionary.keys():
            r_dictionary[i['firstCity']][i['secondCity']]= [i['length'],i['speedLimit'], i['nameOfHighway']]
        else:
            r_dictionary[i['firstCity']]= {i['secondCity']:[i['length'],i['speedLimit'], i['nameOfHighway']] }
       
    for j in records:
        r_dict[j['city']] = [j['latitude'],j['longitude']]
        
    distance=0
    time=0
    segments=0
    delivery = 0
    heuristic = 0
    fringe = PriorityQueue()
    route_list = {}
    fringe.put((heuristic,distance,time,segments,delivery,start))
    route_cal = []
    visitedCity= set()
    visitedCity.add(start)
    while fringe:
        (heuristic,distance,time,segments,delivery,curr_city)=fringe.get()
        if curr_city == end :
            
            visitedCity.add(curr_city)          
            k = end
            while(k != start):
                route_cal.append(k)
                k = route_list[k]
            route_cal.reverse()
            route_taken = []
            for i in route_cal:
                route_taken.append(( i, str(r_dictionary[i][route_list[i]][2]) +" for "+ str(r_dictionary[i][route_list[i]][0]) + " miles"))
            return {"total-segments" : segments, 
                        "total-miles" : float(distance), 
                        "total-hours" : float(time), 
                        "total-delivery-hours" : delivery, 
                        "route-taken" : route_taken}
        else:
                for key in r_dictionary[curr_city].keys():   
                    if key not in visitedCity:
                        fringe.put((heuristic_cost(key,end,r_dict,cost,distance,r_dictionary[curr_city][key][0],time,r_dictionary[curr_city][key][0],r_dictionary[curr_city][key][1],delivery,segments ),dictance_cal(distance,r_dictionary[curr_city][key][0]) ,time_cal(time,r_dictionary[curr_city][key][0],r_dictionary[curr_city][key][1]) ,segments_cal(segments),delivery_time(time,delivery,r_dictionary[curr_city][key][0],r_dictionary[curr_city][key][1]), key))
                        visitedCity.add(curr_city)
                        route_list[key]= curr_city
    """"
    Find shortest driving route between start city and end city
    based on a cost function.

    
    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-delivery-hours": a float indicating the expected (average) time 
                                   it will take a delivery driver who may need to return to get a new package
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function )

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.2f" % result["total-miles"])
    print("             Total hours: %8.5f" % result["total-hours"])
    print("Total hours for delivery: %8.4f" % result["total-delivery-hours"])


