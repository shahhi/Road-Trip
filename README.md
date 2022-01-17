# Road-Trip
## Finding the shortest driving route between two distant places 

#### Road Trip : to find good driving directions between pairs of cities given by the user. Approach: Initially, approached the question by simply defining a fringe as PriorityQueue() with distance and start as values. And implemented modified BFS to find the shortest path to the end city, but the solution for total distance travelled was not the best route. Since we were not allowing to travel the same routes twice, we were missing out on these better routes. Added Visited city as a set to avoid this overhead.

Furthermore, to improve the results after googling around, we introduced the heuristic cost function Haversine to make use of latitude and longitude. This did make the computation speed better with respect to distance as cost parameter. Implemented the same for time, delivery time and segments as cost parameters.

Even after we added a heuristic function the route obtained to reach the end city was not optimal because the Haversine formula had a comparative high value range which was not reflecting the g(x) to its best. After analysing the behaviour used a weighted factor of 0.1 for distance and segment and factor of 0.01 for time and total delivery time. This yielded the best results.

#### State space : All cities that are available in the city-gps.txt file. Successor function : Set of all possible cities that have a route to travel to/from the current city. Edge weight : The number of segments, distance in miles , time in hours, total delivery hours Initial state : The given start city Goal state :The given end city Heuristic function:

### Haversine function as modified (used weighted) h(x) to calculate spherical distance between current city to end city. Source

f(x) = g(x) + h(x), where f(x) = total cost to travel from the start city to a any given end city, g(x) = total cost of travelling to a current city from the start city , where the cost could be number of segments, distance, time and delivery time with chances of a mistake (it could be depending on the cost parameter that user wants) . And, h(x) = total cost to travel to the end city from the current city considering the weights on the bases of cost parameter. The heuristic is optimal as it manages to find the shortest route between two cities for a selected cost function, and it is admissible as it will never overestimate the path to the goal by finding a longer route if a shorter route is available.

#### Code Explanation :

* The main function starts with calling get_route() with start city, end city and cost parameters, which then reads road-segments-txt (converted to a dictionary of dictionaries for easy accessibility) and city-gps.txt (converted to a dictionary).
* Initialize a fringe as PriorityQueue() with heuristic, distance, time, segments, delivery and start values.We set start and initialise an empty set named ‘visited_cities’ to track all the visited cities.
* Then we run the while loop till fringe is null to find the fastest and optimum path. By select all the cities that can be travelled and have not been travelled already.
* Once we find the end city, we break out of the while loop and construct the shortest route that is stored in routes_taken [].
* Finally, we call the ‘get_route’ function that calculates all the total costs according to the provided cost function. ( We could upgrade the current code by preferring the next cities to travel based on how close they are to the goal, by calculating modified Haversine distance using the gps coordinates of the cities. )
