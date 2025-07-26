import streamlit as st
import itertools
import numpy as np

st.title("🗺️ Route Optimizer: Shortest Path Between Cities")

st.markdown("This app calculates the shortest route between cities using a brute-force approach to the Traveling Salesman Problem (TSP).")

# Step 1: Input number of cities
num_cities = st.slider("Select number of cities (2 to 6)", min_value=2, max_value=6, value=3)

# Step 2: Input city names
city_names = []
st.subheader("Enter City Names")
for i in range(num_cities):
    city = st.text_input(f"City {i+1} name", value=f"City{i+1}")
    city_names.append(city)

# Step 3: Input distances between cities using sliders
st.subheader("Set Distances Between Cities (in km)")
distances = np.zeros((num_cities, num_cities))

for i in range(num_cities):
    for j in range(i+1, num_cities):
        dist = st.slider(f"Distance from {city_names[i]} to {city_names[j]}", min_value=1, max_value=1000, value=100)
        distances[i][j] = dist
        distances[j][i] = dist  # symmetric

# Step 4: Optimize route
if st.button("Optimize Route"):
    st.subheader("🔍 Optimizing...")
    
    # Generate all permutations of cities (excluding the first city to avoid duplicate cycles)
    city_indices = list(range(num_cities))
    start = city_indices[0]
    other_indices = city_indices[1:]
    min_distance = float('inf')
    best_route = []

    for perm in itertools.permutations(other_indices):
        route = [start] + list(perm) + [start]
        total_dist = sum(distances[route[i]][route[i+1]] for i in range(len(route)-1))
        if total_dist < min_distance:
            min_distance = total_dist
            best_route = route

    # Display result
    route_names = [city_names[i] for i in best_route]
    st.success(f"Shortest route: {' → '.join(route_names)}")
    st.info(f"Total distance: {min_distance:.2f} km")
