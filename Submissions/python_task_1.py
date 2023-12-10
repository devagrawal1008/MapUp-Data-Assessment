import pandas as pd
df = pd.read_csv('dataset-1.csv')
#Task1-Question1
def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.
    Args:
        df (pandas.DataFrame)
    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
   # Pivot the DataFrame to get the desired matrix
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    # Set diagonal values to 0
    car_matrix.values[[range(len(car_matrix))]*2] = 0
    return car_matrix
generate_car_matrix(df)
#Task1-Question2
def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.
    Args:
        df (pandas.DataFrame)
    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Add a new column 'car_type' based on the conditions
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                                   labels=['low', 'medium', 'high'], right=False)
    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()
    # Sort the dictionary alphabetically based on keys
    sorted_type_counts = dict(sorted(type_counts.items()))
    return sorted_type_counts
get_type_count(df)
#Task1-Question3        
def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.
    Args:
        df (pandas.DataFrame)
    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Calculate the mean value of the 'bus' column
    mean_bus_value = df['bus'].mean()
    # Identify indices where the 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * mean_bus_value].index.tolist()
    # Sort the indices in ascending order
    bus_indexes.sort()
    return bus_indexes
get_bus_indexes(df)  
#Task1-Question4
def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.
    Args:
        df (pandas.DataFrame)
    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Filter rows where the average of the 'truck' column is greater than 7
    filtered_data = df.groupby('route')['truck'].mean().reset_index()
    filtered_data = filtered_data[filtered_data['truck'] > 7]
    # Sort the routes
    sorted_routes = filtered_data['route'].sort_values().tolist()
    return sorted_routes
filter_routes(df)


#Task1-Question5
def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.
@@ -101,11 +101,18 @@ def multiply_matrix(matrix)->pd.DataFrame:
    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_df = matrix.copy()  # Create a copy to avoid modifying the original DataFrame

    # Apply the specified logic to each value in the DataFrame
    modified_df = modified_df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)

    return matrix
    # Round the values to 1 decimal place
    modified_df = modified_df.round(1)

    return modified_df
multiply_matrix(matrix)

#Task1-Question6
def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period
@@ -116,6 +123,18 @@ def time_check(df)->pd.Series:
    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    # Convert timestamp columns to datetime objects
    df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])

    # Calculate the time difference
    df['time_diff'] = df['end_datetime'] - df['start_datetime']

    # Create a mask for incorrect timestamps
    mask = (df['time_diff'] < pd.Timedelta(24, 'h')) | (df['start_datetime'].dt.weekday < 0) | (df['end_datetime'].dt.weekday < 0)

    # Group by (id, id_2) and check if any entry in the group has incorrect timestamps
    result = df.groupby(['id', 'id_2'])['time_diff'].apply(lambda x: x.any() or mask.any())

    return pd.Series()
    return result
time_check(df)
