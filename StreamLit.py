import streamlit as st
import pandas as pd
import io
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
                next_state = copy.deepcopy(current_state)
                next_state[i]["current_location"], next_state[j]["current_location"] = next_state[j]["current_location"], next_state[i]["current_location"]
                next_state[i]["current_shelf_priority"], next_state[j]["current_shelf_priority"] = next_state[j]["current_shelf_priority"], next_state[i]["current_shelf_priority"]
                next_state_cost = evaluate_heuristic(next_state)
                next_states.append((i, j, next_state_cost))

    return next_states


def main():
    # Title of the app
    st.title("Simple Streamlit App")
    
    # Section 1: Input an integer number
    st.header("Step 1: Input an Integer")
    user_number = st.number_input("Enter an integer:", min_value=0, value=0, step=1)
    st.write(f"You entered: {user_number}")
    
    # Section 2: Upload a CSV file
    st.header("Step 2: Upload a CSV File")
    uploaded_file = st.file_uploader("Upload a CSV file:", type=["csv"])
    
    if uploaded_file:
        # Read the uploaded CSV
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded CSV file preview:")
        st.write(df)

        def greedy_search(initial_state, max_iterations=user_number):
            global moves_list
            current_state = copy.deepcopy(initial_state)
            iterations = 0  # Counter for iterations

            while not is_goal_state(current_state) and iterations < max_iterations:
                next_states = generate_next_states(current_state)

                best_next_state = min(next_states, key=lambda x: x[2])
                elem1 = best_next_state[0]
                elem2 = best_next_state[1]
                current_state[elem1]["current_location"], current_state[elem2]["current_location"] = current_state[elem2]["current_location"], current_state[elem1]["current_location"]
                current_state[elem1]["current_shelf_priority"], current_state[elem2]["current_shelf_priority"] = current_state[elem2]["current_shelf_priority"], current_state[elem1]["current_shelf_priority"]
                iterations += 1
                new_row = pd.DataFrame({
                    "Move Number": [iterations],
                    "First Item": [current_state[elem1]["id"]],
                    "Location of First Item": [current_state[elem1]["current_location"]],
                    "Second Item": [current_state[elem2]["id"]],
                    "Location of Second Item": [current_state[elem2]["current_location"]]
                })
                moves_list = pd.concat([moves_list, new_row], ignore_index=True)

            return current_state

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

        # Call the function to check for duplicate columns
        final_state = greedy_search(initial_state, max_iterations=user_number)

        
        # Modify the dataframe
        moves_list.to_csv('ABCresults.csv', index=False, header=True)
        
        # Section 3: Download the modified CSV file
        st.header("Step 3: Download the Modified CSV File")
        csv = moves_list.to_csv(index=False)
        b64 = io.BytesIO(csv.encode()).getvalue()
        
        st.download_button(
            label="ABCresults",
            data=b64,
            file_name="modified_file.csv",
            mime="text/csv",
        )

if __name__ == "__main__":
    main()
