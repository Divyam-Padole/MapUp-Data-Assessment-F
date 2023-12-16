import pandas as pd



def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
            
    # Write your logic here
    # Extract unique values from id_1 and id_2 columns
    id_1_values = df['id_1'].unique()
    id_2_values = df['id_2'].unique()

    # Create an empty DataFrame with id_1 as index and id_2 as columns
    result_df = pd.DataFrame(index=id_1_values, columns=id_2_values)

    # Iterate through the common elements of id_1 and id_2
    common_values = set(id_1_values).intersection(id_2_values)
    for val in common_values:
        result_df.at[val, val] = 0

    # Use the 'intersect' method to fill the DataFrame
    for val in common_values:
        rows = df[df['id_1'] == val]
        cols = df[df['id_2'] == val]
        common_rows_cols = rows['id_2'].values.tolist() + cols['id_1'].values.tolist()

        # Use groupby to sum 'car' values for duplicate entries
        grouped_df = df[(df['id_1'] == val) & (df['id_2'].isin(common_rows_cols))].groupby('id_2')['car'].sum().reset_index()

        # Fill the intersection of rows and columns with the sum of 'car' values in the original DataFrame
        result_df.loc[val, grouped_df['id_2']] = grouped_df['car'].tolist()

    # Sort the index in descending order for both 'id_1' and 'id_2'
    result_df = result_df.sort_index(axis=0, ascending=False).sort_index(axis=1, ascending=False)
    df=result_df
    return df  


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    car_type = []
    for car_value in df['car']:
        if car_value < 15:
            car_type.append('low')
        elif 15 < car_value < 25:
            car_type.append('medium')
        elif car_value >= 25:
            car_type.append('high')

    df['car_type'] = car_type
    print(df)
    count_low = 0
    count_medium = 0
    count_high = 0

    for car_count in df['car_type']:
        if car_count == 'low':
            count_low += 1
        if car_count == 'medium':
            count_medium += 1
        if car_count == 'high':
            count_high += 1

    result_dict = {'low': count_low, 'medium': count_medium, 'high': count_high}
    sorted_result = dict(sorted(result_dict.items()))

    print(sorted_result)
    return dict(sorted_result)


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    # avg_truck=0
    # for truck_values in df['truck']:
    #     avg_truck=avg_truck+truck_values

    # range_size=range(df['truck'])
    # avg_truck=avg_truck/range_size

     # Calculate the mean of the 'bus' column
    avg_truck = df['truck'].mean()



    # Initialize an empty list to store indexes
    index_avgGreater = []

    # Iterate through the DataFrame and check if 'bus' values exceed twice the mean
    for index, truck_value in df['truck'].items():
        if truck_value > 2 * avg_truck:
            # Append the index to the list
            index_avgGreater.append(index)

    index_avgGreater.sort()
    #print(index_avgGreater)

    return list(index_avgGreater)


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    # Calculate the average of 'truck' column
    avg_truck = df['truck'].mean()
    print(avg_truck)

    # Filter rows where 'truck' values are greater than 7
    filtered_df = df[df['truck'] > 7]
   # print(filtered_df)
    # Get unique values from the 'route' column
    routes_list = list(filtered_df['route'].unique())

    # Sort the list
    sorted_routes = sorted(routes_list)
    return list(sorted_routes)


def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Create a copy to avoid modifying the original DataFrame
    modified_matrix = matrix.copy()

    # Iterate over rows and columns
    for idx, row in modified_matrix.iterrows():
        for col in modified_matrix.columns:
            if row[col] > 20:
                modified_matrix.at[idx, col] *= 0.75
            else:
                modified_matrix.at[idx, col] *= 1.25

    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here

    return pd.Series()



df = pd.read_csv('datasets/dataset-1.csv')
arg_result = generate_car_matrix(df)
# print(result)
print('this is the car matrix')
print(arg_result)



print('this is the car type count')
result1=get_type_count(df)

print('this is the bus indexes')
result2=get_bus_indexes(df)

print('this is the filtered routes')
result3=filter_routes(df)

print('this is the multiplied matrix')
result4=multiply_matrix(arg_result)
print(result4)