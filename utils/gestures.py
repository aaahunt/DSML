import os

def get_gestures():
      """
      Get all the gestures in the data directory.
      
      Parameters:
      None
      
      Returns:
      list: A list of all the gestures in the data directory
      """
      return os.listdir(os.path.join(os.getcwd(), "data"))

def get_columns():
    return ['time', 'accel_x', 'accel_y', 'accel_z', 'accel_abs']