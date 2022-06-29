import numpy as np

PI = np.pi

def get_orientation_id(velocity):
    speed = sum([i**2 for i in velocity])
    if speed < 0.01:
        return 0
    theta = np.arctan2(velocity[1], velocity[0])
    # right
    if -PI/4 < theta <= PI/4:
        return 2 
    # top
    elif PI/4 < theta <= 3*PI/4:
        return 0 
    # down
    elif -PI/4 >= theta > -3*PI/4:
        return 3 
    # left
    elif theta <= -3*PI/4 or theta > 3*PI/4:
        return 1 
    else:
        raise Exception(f"ERROR: theta-angle = {theta/PI} pi")
