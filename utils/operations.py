import matplotlib.pyplot as plt

def merge_and_average_integers(integers, cluster_range=50):
      """
      Merges consecutive integers within a given range and calculates the average of each merged cluster.

      Args:
            integers (list): A list of integers.
            cluster_range (int, optional): The maximum range between consecutive integers to be merged. Defaults to 50.

      Returns:
            list: A list of integers representing the average of each merged cluster.
      """

      clusters = []
      current_cluster = [integers[0]]

      for number in integers[1:]:
            if number - current_cluster[-1] <= cluster_range:
                  current_cluster.append(number)
            else:
                  clusters.append(current_cluster)
                  current_cluster = [number]
      
      if current_cluster:
            clusters.append(current_cluster)
      
      return [sum(cluster) // len(cluster) for cluster in clusters]

def indices_below_threshold(data, rolling_window, group_threshold, deviation_threshold):
      
      rolling_std = data['accel_abs'].rolling(window=rolling_window).std()
      threshold = rolling_std.mean() - rolling_std.std() / deviation_threshold

      return rolling_std[(rolling_std.shift(-group_threshold) < threshold) & (rolling_std.shift(group_threshold) < threshold)].index

def label_gestures(df, filter_column, threshold, rolling_window, group_threshold, deviation_threshold):
            
      indices_to_drop = []
      gesture_number = 1

      for i, sub_group in df.groupby(['file_number', 'gesture']):

            below_threshold = indices_below_threshold(sub_group, rolling_window, group_threshold, deviation_threshold)
            breakpoints = merge_and_average_integers(below_threshold, 25)

            breakpoints.insert(0, sub_group.index[0])
            breakpoints.append(sub_group.index[-1])

            for b in range(len(breakpoints) - 1):
                  segment = df.loc[breakpoints[b]:breakpoints[b+ 1]][filter_column]
                  all_below_threshold = (segment < threshold).all()
                  if all_below_threshold:
                        dropping = range(breakpoints[b], breakpoints[b + 1])
                        indices_to_drop += dropping
                  else:
                        df.loc[breakpoints[b]:breakpoints[b + 1], 'gesture_number'] = int(gesture_number)
                        gesture_number += 1

      df.drop(indices_to_drop, inplace=True)
      df.dropna(subset=['gesture_number'], inplace=True)
      df.reset_index(drop=True, inplace=True)


def number_to_color(number):
    """
    Maps a number between to a color using the viridis colormap.

    Parameters:
    - number: An integer

    Returns:
    - A color in RGBA format.
    """

    
    # Normalize the number to the range [0, 1]
    normalized_number = (number - 1) / (100 - 1)
    
    # Choose a colormap
    colormap = plt.cm.viridis
    
    # Map the normalized number to a color
    color = colormap(normalized_number)
    
    return color