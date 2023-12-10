import pandas as pd
df = pd.read_csv('dataset-3.csv')

#Task2-Question1
def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Create a graph to represent the network of toll locations
    G = nx.Graph()

    # Add edges and their distances to the graph
    for index, row in df.iterrows():
        G.add_edge(row['id_start'], row['id_end'], distance=row['distance'])

    # Create a dictionary to store the cumulative distances
    distance_matrix = {}

    # Iterate through all toll locations
    for id_start in df['id_start'].unique():
        distance_matrix[id_start] = {}

        for id_end in df['id_end'].unique():
            if id_start == id_end:
                distance_matrix[id_start][id_end] = 0  # Diagonal values are set to 0
            else:
                try:
                    # Compute the shortest path distance between source and destination
                    distance = nx.shortest_path_length(G,source=id_start, target=id_end, weight='distance')
                    distance_matrix[id_start][id_end] = distance
                except nx.NetworkXNoPath:
                    distance_matrix[id_start][id_end] = float('inf')  # No direct path, set to infinity

    # Create a DataFrame from the distance matrix
    distance_df = pd.DataFrame.from_dict(distance_matrix, orient='index')

    return distance_df
calculate_distance_matrix(df)


#Task2-Question2
def unroll_distance_matrix(distance_df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # If distance_df is not defined then we have to write the Question1 code again
    # Create an empty DataFrame to store the unrolled distances
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate through the rows of the distance DataFrame
    for i, row in distance_df.iterrows():
        id_start = i
        for id_end, distance in row.items():
            if id_start != id_end:
                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance},
                                                 ignore_index=True)

    return unrolled_df
unroll_distance_matrix(distance_df)

#Task2-Question3
def find_ids_within_ten_percentage_threshold(unrolled_df, reference_ID)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Filter rows based on the reference_value
    reference_rows = unrolled_df[unrolled_df['id_start'] == reference_ID]

    # Calculate the average distance for the reference value
    reference_average_distance = reference_rows['distance'].mean()

    # Calculate the threshold range (10% of the average distance)
    threshold = 0.1 * reference_average_distance

    # Find IDs within the threshold range
    within_threshold_df = reference_rows[
        (reference_rows['distance'] >= reference_average_distance - threshold) &
        (reference_rows['distance'] <= reference_average_distance + threshold)
    ]

    # Extract and sort the unique values from the 'id_start' column
    within_threshold_ids = sorted(within_threshold_df['id_start'])

    return within_threshold_ids
find_ids_within_ten_percentage_threshold(unrolled_df,reference_ID)
#example
find_ids_within_ten_percentage_threshold(unrolled_df, 1001400)

#Task2-Question4
def calculate_toll_rate(unrolled_df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Create new columns for each vehicle type with initial values set to NaN
    for vehicle_type in rate_coefficients.keys():
        unrolled_df[vehicle_type] = float('nan')

    # Iterate through the rows of the DataFrame and calculate toll rates
    for i, row in unrolled_df.iterrows():
        for vehicle_type, rate_coefficient in rate_coefficients.items():
            unrolled_df.at[i, vehicle_type] = row['distance'] * rate_coefficient

    return unrolled_df
calulate_toll_rate(unrolled_df)

#Task2-Question5
from datetime import datetime, time, timedelta
def calculate_time_based_toll_rates(unrolled_df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Define time ranges and discount factors
    time_ranges_weekdays = [
        (time(0, 0, 0), time(10, 0, 0), 0.8),
        (time(10, 0, 0), time(18, 0, 0), 1.2),
        (time(18, 0, 0), time(23, 59, 59), 0.8)
    ]
    
    time_ranges_weekends = [
        (time(0, 0, 0), time(23, 59, 59), 0.7)
    ]

    # Create new columns for start_day, start_time, end_day, and end_time
    unrolled_df['start_day'] = unrolled_df['end_day'] = unrolled_df['start_time'] = unrolled_df['end_time'] = None

    # Iterate through the rows of the DataFrame and calculate time-based toll rates
    for i, row in unrolled_df.iterrows():
        # Extract id_start, id_end, and distance values
        id_start = row['id_start']
        id_end = row['id_end']
        distance = row['distance']

        # Initialize datetime objects for each day of the week
        start_datetime = datetime.combine(datetime.today(), time(0, 0, 0))
        end_datetime = start_datetime + timedelta(days=3) - timedelta(seconds=1)

        # Iterate through the days of the week
        for day_offset in range(7):
            start_day = (start_datetime + timedelta(days=day_offset)).strftime('%A')
            end_day = start_day  # Same day for each (id_start, id_end) pair

            # Iterate through the time ranges and apply discount factors
            for start_time, end_time, discount_factor in (time_ranges_weekdays if day_offset < 5 else time_ranges_weekends):
                unrolled_df.at[i, 'start_day'] = start_day
                unrolled_df.at[i, 'start_time'] = start_time
                unrolled_df.at[i, 'end_day'] = end_day
                unrolled_df.at[i, 'end_time'] = end_time
                unrolled_df.at[i, 'moto'] = distance * discount_factor * 0.8
                unrolled_df.at[i, 'car'] = distance * discount_factor * 1.2
                unrolled_df.at[i, 'rv'] = distance * discount_factor * 1.5
                unrolled_df.at[i, 'bus'] = distance * discount_factor * 2.2
                unrolled_df.at[i, 'truck'] = distance * discount_factor * 3.6

    return unrolled_df
calculate_time_based_toll_rates(unrolled_df)
