# Credit: https://github.com/MiladNooraei/Orienteering-Problem
__name__ = "Ali Etemadfard, Milad Nooraei" 
__email__ = "alietemadfard@gmail.com, miladnooraiy0@gmail.com"

import argparse
import math

import matplotlib.pyplot as plt
import yaml

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", required=True, help="file defining map")
args = parser.parse_args()

# Finding node number for output
def find_index_2d(lst, target):
    for i, sublist in enumerate(lst):
        if sublist == target:
            return i

# Finding distance of next node
def distance_node(node, data_array):
    global T_max
    global sum_distance
    global full_data_array
    global path
    global sum_score

    distance_list = []
    current_node = [node[0], node[1]]

    for i in data_array:
        next_node = [i[0], i[1]]
        try:
            distance_list += [i[2] / math.dist(current_node, next_node)]
        except ZeroDivisionError:
            distance_list += [9999999]

    for i in range(len(data_array)):
        if distance_list[i] == max(distance_list):
            index = i
            break
    
    next_node = data_array[index]
    sum_distance += math.dist(current_node, [next_node[0], next_node[1]])

    if sum_distance > T_max:
        sum_distance -= math.dist(current_node, [next_node[0], next_node[1]])
        return
    
    sum_score += next_node[2]
    path += str(find_index_2d(full_data_array, next_node)) + " "

    new_node = data_array[index]
    data_array.pop(index)
    
    distance_node(new_node, data_array)

# Example instance data
data_array = []
control_lookup = {}
control_idx = 2
T_max = 0

with open(args.file, "r") as file:
    config = yaml.safe_load(file)
    T_max = config["max_distance"]

    data_array.append([config["start_x_coord"], config["start_y_coord"], 0, 0])
    data_array.append([config["start_x_coord"], config["start_y_coord"], 0, 0])
    control_lookup[0] = "HH"
    control_lookup[1] = "HH"

    for control_info in config["controls"]:
        value = (control_info["id"] // 10) * 10
        name = control_info["id"]
        values = [control_info["x_coord"], control_info["y_coord"], value, name]
        data_array.append(values)

        control_lookup[control_idx] = str(name)
        control_idx += 1
nodes = data_array.copy()

# Initialize
sum_distance = 0
sum_score = 0
path = ""
full_data_array = data_array.copy()

# Action
distance_node(data_array[0], data_array[1:])

# Printing result
print(f"Distance: {sum_distance:.2f}")
print(f"Maximum Score: {sum_score}")
path_list = [int(item) for item in path.split()]
# append start location to end to make closed loop
path_list.append(path_list[0])
path_str = ""
for item in path.split():
    path_str += control_lookup[int(item)] + " "
print("Optimal Path:")
print(path_str.lstrip())

# PLOT
result = [[sublist[0], sublist[1]] for sublist in nodes]
x_axis_numbers, y_axis_numbers = [], []
for i in result:
    x_axis_numbers += [i[0]]
    y_axis_numbers += [i[1]]

plot_1_x, plot_1_y = [], []
for i in path_list:
    plot_1_x += [x_axis_numbers[i]]
    plot_1_y += [y_axis_numbers[i]]

for control_x, control_y, _points, control_name in data_array:
    plt.plot(control_x, control_y, color = "red", marker = "o", markerfacecolor = "red", markersize = 12)
    plt.text(control_x, control_y, control_name, ha = "center", va = "bottom", color = "Black", weight="bold")

for i in range(len(path_list)):
    control_name = str(control_lookup[path_list[i]])
    plt.text(plot_1_x[i], plot_1_y[i], control_name, ha = "center", va = "bottom", color = "Black", weight="bold")

plt.plot(plot_1_x, plot_1_y, color = "green", linestyle = "dashed", linewidth = 3, marker = "o", markerfacecolor = "blue", markersize = 12)
plt.xlabel("x - axis")
plt.ylabel("y - axis")
ax = plt.gca()
ax.set_aspect("equal", "box")
plt.title(f"Solution for {args.file} with Maximum Distance of {T_max}")
plt.show()
