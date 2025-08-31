# tsp_simulated_annealing.py
import math
import random

def calculate_distance(p1, p2):
    """Calculates Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_tour_distance(tour, cities):
    """Calculates the total distance of a tour."""
    dist = 0
    for i in range(len(tour)):
        dist += calculate_distance(cities[tour[i-1]], cities[tour[i]])
    return dist

def simulated_annealing(cities):
    """Solves TSP using Simulated Annealing."""
    num_cities = len(cities)
    
    # Parameters
    initial_temp = 1000.0
    cooling_rate = 0.995
    min_temp = 1.0
    
    # 1. Create an initial random tour
    current_tour = list(range(num_cities))
    random.shuffle(current_tour)
    
    best_tour = current_tour[:]
    best_distance = total_tour_distance(best_tour, cities)
    
    temp = initial_temp
    
    while temp > min_temp:
        # 2. Create a neighbor tour by swapping two cities (2-opt swap)
        new_tour = current_tour[:]
        i, j = random.sample(range(num_cities), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        
        # 3. Calculate costs
        current_distance = total_tour_distance(current_tour, cities)
        new_distance = total_tour_distance(new_tour, cities)
        
        # 4. Decide whether to accept the new tour
        delta = new_distance - current_distance
        
        if delta < 0 or random.uniform(0, 1) < math.exp(-delta / temp):
            current_tour = new_tour[:]
        
        # Update the best tour found so far
        if total_tour_distance(current_tour, cities) < best_distance:
            best_tour = current_tour[:]
            best_distance = total_tour_distance(best_tour, cities)
            
        # 5. Cool down
        temp *= cooling_rate
        
    return best_tour, best_distance

if __name__ == "__main__":
    # Example: 20 Cities in Rajasthan (latitude, longitude)
    # Using coordinates as (x, y) for simplicity in a 2D plane
    rajasthan_cities = {
        "Jaipur": (26.9124, 75.7873), "Jodhpur": (26.2389, 73.0243),
        "Udaipur": (24.5854, 73.7125), "Jaisalmer": (26.9157, 70.9083),
        "Bikaner": (28.0229, 73.3119), "Ajmer": (26.4499, 74.6399),
        "Pushkar": (26.4885, 74.5510), "Mount Abu": (24.5926, 72.7156),
        "Kota": (25.2138, 75.8648), "Bundi": (25.4413, 75.6457),
        "Chittorgarh": (24.8887, 74.6269), "Ranthambore": (26.0173, 76.5026),
        "Alwar": (27.5530, 76.6346), "Bharatpur": (27.2175, 77.4913),
        "Shekhawati": (27.9710, 75.1507), "Pali": (25.7720, 73.3250),
        "Barmer": (25.7490, 71.4162), "Nagaur": (27.2038, 73.7441),
        "Sikar": (27.6119, 75.1397), "Ranakpur": (25.1154, 73.4410)
    }

    city_names = list(rajasthan_cities.keys())
    city_coords = list(rajasthan_cities.values())

    print("Optimizing tour for Rajasthan cities...")
    best_tour_indices, best_distance = simulated_annealing(city_coords)
    
    best_tour_cities = [city_names[i] for i in best_tour_indices]
    
    print(f"\n🎉 Best tour found with total distance: {best_distance:.2f}")
    print(" -> ".join(best_tour_cities))