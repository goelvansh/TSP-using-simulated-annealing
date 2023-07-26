import random
import math
import matplotlib.pyplot as plt

# Function to calculate the distance between two cities
def distance(city1, city2):
    lat1, lon1 = city1
    lat2, lon2 = city2
    R = 6371  # Earth radius in kilometers

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    distance = R * c
    return distance

# Function to calculate the total cost of a tour
def cost(cities, tour):
    total = 0
    for i in range(len(tour)):
        total += distance(cities[tour[i]], cities[tour[i-1]])
    total += distance(cities[tour[-1]], cities[tour[0]])
    return total

# Function to generate a random tour
def random_tour(cities):
    tour = list(range(len(cities)))
    random.shuffle(tour)
    return tour

# Simulated Annealing function with dynamic cooling schedule
def simulated_annealing(cities, current_tour, temperature, cooling_rate):
    best_tour = current_tour
    best_cost = cost(cities, current_tour)
    acceptance_rate = 0.5

    while temperature > 1:
        # Generate a new path
        new_tour = random_tour(current_tour)
        new_cost = cost(cities, new_tour)

        # Determine if we should accept
        delta = new_cost - best_cost

        if delta < 0:
            best_tour = new_tour
            best_cost = new_cost
            acceptance_rate = 1
        elif math.exp(-delta / temperature) < random.random():
            current_tour = new_tour
            acceptance_rate += (1 - acceptance_rate) * 0.01
        else:
            acceptance_rate -= acceptance_rate * 0.01

        # Adjust the cooling rate based on the acceptance rate
        if acceptance_rate < 0.3:
            cooling_rate -= 0.01
        elif acceptance_rate > 0.6:
            cooling_rate += 0.01

        # Cool the temperature
        temperature *= cooling_rate

    return best_tour, best_cost

def plot_tour(cities, tour):
    x = [cities[i][0] for i in tour]
    y = [cities[i][1] for i in tour]

    x.append(cities[tour[0]][0]) # add the first city to the end of the list
    y.append(cities[tour[0]][1])

    plt.scatter(x, y)
    plt.plot(x, y, '-o')

    # Add labels and title
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Best Tour')

# 20 cities
#Mt.Abu, Rajsamand, Jaisalmer, Ajmer, Alwar, Bikaner, Bundi, Chittorgarh, Jaipur
#Jhalawar, Jodhpur, Kota, Pushkar, Udaipur, Bharatpur, Sawai Madhopur, Nagaur,
#Jalore, Pali, Dausa
cities = [
    (24.531445, 72.733360),
    # Add other city coordinates here...
]

tour = random_tour(cities)
best_tour, best_cost = simulated_annealing(cities, tour, 100, 0.9995)

print("Best tour:", best_tour)
print("Best cost:", best_cost)

plot_tour(cities, best_tour)
plt.show()
