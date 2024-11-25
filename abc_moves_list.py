# -*- coding: utf-8 -*-
"""ABC Moves List.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1uVyBL0e3DaLZbhAwHgTOKDojI_--lGSo
"""

pip install streamlit

import pandas as pd
import streamlit as st

df = pd.read_csv("ABCearings.csv", sep= ',')

df.head()

df = df.rename(columns={
    'ItemID': 'id',
    'Item Ranking': 'ranking',
    'DesiredLocation': 'desired_location',
    'DesiredShelfPriority': 'desired_shelf_priority',
    'CurrentLocation': 'current_location',
    'CurrentShelfPriority': 'current_shelf_priority',
    'PriorityMove': 'priority_direction'
})

# Create a list of dictionaries
initial_state = df[['id', 'ranking', 'desired_location', 'desired_shelf_priority', 'current_location', 'current_shelf_priority', 'priority_direction']].to_dict(orient='records')

#print(initial_state)

import copy

# Create an empty DataFrame
moves_list = pd.DataFrame(columns=[
    "Move Number",
    "First Item",
    "Location of First Item",
    "Second Item",
    "Location of Second Item"
])

def is_goal_state(state):
    for item in state:
        if (
            item["current_location"] != item["desired_location"] or
            item["current_shelf_priority"] != item["desired_shelf_priority"]
        ):
            return False
    return True

def evaluate_heuristic(state):
    total_cost = 0
    for item in state:
        if item["current_location"] == item["desired_location"]:
            ranking_cost = 0
        else:
            ranking_cost = item["ranking"]

        shelf_priority_difference = abs(item["desired_shelf_priority"] - item["current_shelf_priority"])
        shelf_priority_cost = 2000 * shelf_priority_difference
        total_cost += ranking_cost + shelf_priority_cost

    return total_cost

def generate_next_states(current_state):
    next_states = []

    for i in range(len(current_state)):
        for j in range(i + 1, len(current_state)):
            item1 = current_state[i]
            item2 = current_state[j]
            #print("Avaliando items:")
            #print(item1)
            #print(item2)

            # Check the conditions for swapping
            if (
                item1["current_location"] != item1["desired_location"]
                and item2["current_location"] != item2["desired_location"]
                and (
                    item1["current_shelf_priority"] == item2["current_shelf_priority"]
                    or (
                        item1["priority_direction"] > 0
                        and (item2["current_shelf_priority"] - item1["current_shelf_priority"]) > 0
                        and item2["priority_direction"] < 0
                        and item2["desired_shelf_priority"] <= item1["current_shelf_priority"]
                        and item1["desired_shelf_priority"] >= item2["current_shelf_priority"]
                    )
                    or (
                        item1["priority_direction"] < 0
                        and (item2["current_shelf_priority"] - item1["current_shelf_priority"]) < 0
                        and item2["priority_direction"] > 0
                        and item2["desired_shelf_priority"] >= item1["current_shelf_priority"]
                        and item1["desired_shelf_priority"] <= item2["current_shelf_priority"]
                    )
                )
            ):
                # Create a new state with the items swapped
                #print("Conditions met")
                next_state = copy.deepcopy(current_state)
                next_state[i]["current_location"], next_state[j]["current_location"] = next_state[j]["current_location"], next_state[i]["current_location"]
                next_state[i]["current_shelf_priority"], next_state[j]["current_shelf_priority"] = next_state[j]["current_shelf_priority"], next_state[i]["current_shelf_priority"]
                #print("New locations:")
                #print(next_state[i])
                #print(next_state[j])
                next_state_cost = evaluate_heuristic(next_state)
                next_states.append((i, j, next_state_cost))

    return next_states

def greedy_search(initial_state, max_iterations=300):
    global moves_list
    current_state = copy.deepcopy(initial_state)
    iterations = 0  # Counter for iterations
    #print("Starting Greedy")

    while not is_goal_state(current_state) and iterations < max_iterations:
        next_states = generate_next_states(current_state)
       # print("Loop")
        #print(next_states)

        best_next_state = min(next_states, key=lambda x: x[2])
        #print(best_next_state)
        elem1 = best_next_state[0]
        elem2 = best_next_state[1]
        current_state[elem1]["current_location"], current_state[elem2]["current_location"] = current_state[elem2]["current_location"], current_state[elem1]["current_location"]
        current_state[elem1]["current_shelf_priority"], current_state[elem2]["current_shelf_priority"] = current_state[elem2]["current_shelf_priority"], current_state[elem1]["current_shelf_priority"]
 #       print("Swapping items:")
  #      print(current_state[elem1]["id"])
   #     print(current_state[elem1]["current_location"])
    #    print(current_state[elem2]["id"])
     #   print(current_state[elem2]["current_location"])
        iterations += 1
        new_row = pd.DataFrame({
            "Move Number": [iterations],
            "First Item": [current_state[elem1]["id"]],
            "Location of First Item": [current_state[elem1]["current_location"]],
            "Second Item": [current_state[elem2]["id"]],
            "Location of Second Item": [current_state[elem2]["current_location"]]
        })
        moves_list = pd.concat([moves_list, new_row], ignore_index=True)
        #print(iterations)

    return current_state

# Example usage:
#initial_state =

final_state = greedy_search(initial_state, max_iterations=300)
#print("Final State:", final_state)

moves_list.head()

moves_list.to_csv('ABCresults.csv', index=False, header=True)

st.title("ABC Bearings Optimization")
   if st.button("Run Greedy Search"):
       run_greedy_search()
