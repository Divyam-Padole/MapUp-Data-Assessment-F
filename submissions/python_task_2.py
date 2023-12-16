import pandas as pd

def calculate_distance_matrix(df)->pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    l1 = df['id_start'].tolist()
    l2 = df['id_end'].tolist()
    dis = df['distance'].tolist()
    l = list(set(l1 + l2))
    l.sort()

    distance_matrix = pd.DataFrame(0, columns=l, index=l)

    for i in range(len(l1)):
        distance_matrix.at[l1[i], l2[i]] = dis[i]
        distance_matrix.at[l2[i], l1[i]] = dis[i]

    flag = 40
    for i in range(2, 39):
        j = 0
        flag1 = flag
        while flag1 >= 0:
            p = distance_matrix.iat[i - 1, j] + distance_matrix.iat[i, j + 1]
            distance_matrix.iat[i, j] = p
            distance_matrix.iat[j, i] = p
            i += 1
            j += 1
            flag1 -= 1
        flag -= 1

    return distance_matrix

def unroll_distance_matrix(df):
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Get the number of rows and columns in the input DataFrame
    count_row = df.shape[0]
    count_col = df.shape[1]

    # Create an empty DataFrame to store the unrolled data
    df_unroll = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    for i in range(count_row):
        for j in range(count_col):
            # Skip rows where 'id_start' is equal to 'id_end'
            if df.index[i] == df.columns[j]:
                continue

            # Create a dictionary with the unrolled data
            data = {
                'id_start': df.index[i],
                'id_end': df.columns[j],
                'distance': df.iloc[i, j]
            }

            # Use pd.concat to concatenate DataFrames
            df_unroll = pd.concat([df_unroll, pd.DataFrame(data, index=[0])], ignore_index=True)

    return df_unroll

def find_ids_within_ten_percentage_threshold(df, reference_id) -> list:
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        list: List of IDs whose average distance is within the specified percentage threshold
              of the reference ID's average distance.
    """
    # Count the number of times the reference id is present in the start column
    count_ref_in_start = len(df[df['id_start'] == reference_id])

    if count_ref_in_start > 0:
        # Filter rows where 'id_start' matches the reference_id and calculate the sum of 'distance'
        total_distance = df[df['id_start'] == reference_id]['distance'].sum()

        # Finding the avg values       
        avg_distance = total_distance / count_ref_in_start
        threshold = avg_distance * 0.1

        # Finding the range
        lower_range = avg_distance - threshold
        upper_range = avg_distance + threshold
        print('Lower range:', lower_range)
        print('Upper range:', upper_range)
        
        # Making the list of ids which are in the range
        list_of_ids = sorted(df[(df['id_start'] == reference_id) & 
                                (df['distance'] >= lower_range) & 
                                (df['distance'] <= upper_range)]['id_end'].unique())
        print('List of IDs within 10% threshold:')
        print(list_of_ids)

        return list_of_ids


def calculate_toll_rate(df)->pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df

def calculate_time_based_toll_rates(df)->pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here

    return df

df = pd.read_csv('/run/media/divyam/6AA61296A612633D/sem7/work/mapup/MapUp-Data-Assessment-F-main/MapUp-Data-Assessment-F-main/datasets/dataset-3.csv')

res = calculate_distance_matrix(df)
print('this is the distance matrix')
print(res)

res1 = unroll_distance_matrix(res)
print('this is the unrolled matrix')
print(res1)


res2=find_ids_within_ten_percentage_threshold(res1,1001400)
print('this is the list of ids within 10% threshold')
print(res2)


res3=calculate_toll_rate(res1)
print('this is the toll rate')
print(res3)