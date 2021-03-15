
import math
from functools import cmp_to_key

# points = [(1, 0.5), (2, 1), (3.5, 1.5), (5, 0.5),
#     (2, 2.5), (1, 3.5), (4, 4), (5, 4.5), (1, 5), (4, 0.5)]

input_points = [(1, 0.5), (4, 0.5), (4, 0.5), (2, 1), (4, 2), (2, 1), (1, 5), (2, 10), (4, 4), (8, 8)]

def graham_scan(input_points):
    """
    Finds the convex hull for a set of two-dimensional points in the plane.
    """
    points = input_points.copy()
    # print(points)
    convex_hull = []
    p_0 = find_p_0(points)
    points.remove(p_0)

    points_p_0_added = []
    for i in range(0, len(points)):
        points_p_0_added.append([points[i], p_0])

    """
    Sorts remaining points by polar angle between the vector (of
    the reference point to the current point) and the unity vector in the
    direction of the x axis.
    """
    points_p_0_added_sorted = sorted(points_p_0_added, key=cmp_to_key(compare))
    
    points = []

    for i in range(0, len(points_p_0_added_sorted)):
        points.append(points_p_0_added_sorted[i][0])

    print('p0 is {}'.format(p_0))
    print('Sorted points by polar angle: \n{}'.format(points))
    points = remove_duplicates(p_0, points)
    print('Points with duplicates removed: {}'.format(points))

def find_p_0(points):
    """
    Finds the starting point for the convex hull.
    """
    p_0 = points[0]
    possible_p_0 = []

    for i in range(1, len(points)):
        if points[i][1] < p_0[1]:
            p_0 = points[i]
        elif points[i][1] == p_0[1] and points[i][0] < p_0[0]:
            p_0 = points[i]

    return p_0

def angle_between(v_1, v_2):
    """
    Computes the angle in degrees between two vectors.
    """
    scalar = (v_1[0] * v_2[0]) + (v_1[1] * v_2[1])
 
    magnitude_v_1 = math.sqrt((v_1[0] * v_1[0]) + (v_1[1] * v_1[1]))
    magnitude_v_2 = math.sqrt((v_2[0] * v_2[0]) + (v_2[1] * v_2[1]))
    
    cos_angle = scalar / (magnitude_v_1 * magnitude_v_2)
    angle_radian = math.acos(cos_angle)
    angle_degrees = angle_radian * 180 / math.pi

    return angle_degrees

def compare(element_1, element_2):
    """
    Compare function used for sorting by polar angle with p_0
    as reference point.
    """
    v_x_axis = (1, 0)
    p_0 = element_1[1]
    p_1 = element_1[0]
    p_2 = element_2[0]
 
    """
    Compute vectors from reference point p_0 to current point for
    each point.
    """
    v_1 =  (p_1[0] - p_0[0], p_1[1] - p_0[1])
    v_2 = (p_2[0] - p_0[0], p_2[1] - p_0[1])

    angle_1 = angle_between(v_1, v_x_axis)
    angle_2 = angle_between(v_2, v_x_axis)
    # print('Angle 1: {}'.format(angle_1))
    # print('Angle 2: {}'.format(angle_2))

    if angle_1 < angle_2:
        return -1

    elif angle_1 > angle_2:
        return 1
    
    else:
        # If the angles are equal, put the point first that
        # is closer to p_0 in x direction.
        if p_1[0] < p_2[0]:
            return -1

        elif p_1[0] > p_2[0]:
            return 1
        else:
            return 0

def remove_duplicates(p_0, points):
    """
    If multiple points have the same angle, remove
    all except the one farthes away from p0.
    """
    visited = []
    to_delete = []
    tmp = []
    v_x_axis = (1, 0)
    # print('Points are currently: {}'.format(points))

    for i in range(0, len(points)):
        if not (i in visited):
            visited.append(i)
            tmp.append(i)
            angle_current_point = angle_between(compute_vector(p_0, points[i]), v_x_axis)

            # Figure out which points have the same
            # angle.
            for j in range (i + 1, len(points)):
                angle_other_point = angle_between(compute_vector(p_0, points[j]), v_x_axis)
                if angle_current_point == angle_other_point:
                   tmp.append(j)
                   visited.append(j)
        if len(tmp) > 1:
            to_delete += points_to_delete(p_0, points, tmp)
        tmp = []

    print('Points to be deleted: {}'.format(to_delete))
    result_points = points.copy()

    # Delete points that should be deleted.
    for i in range(0, len(to_delete)):
        result_points.remove(points[to_delete[i]])

    return result_points

def compute_vector(p_1, p_2):
    """
    Returns the vector based on two points.
    """
    vector = (p_2[0] - p_1[0], p_2[1] - p_1[1]) 
    return vector

def euclidean_distance(p_1, p_2):
    """
    Computed the euclidean distance between two points.
    """
    a = p_2[0] - p_1[0]
    b = p_2[1] - p_1[1]
    distance = math.sqrt((a * a) + (b * b))
    return distance

def points_to_delete(p_0, points, tmp):
    """
    Determine what points (represented through the index) can
    be deleted. Only keep the point that is farthest away from p_0.
    """
    # print('Temp is currently: {}'.format(tmp))
    max_distance_to_p0 = None
    index_point_with_max_distance = None
    to_delete = []

    for i in range(0, len(tmp)):
        distance = euclidean_distance(p_0, points[tmp[i]])
        if (max_distance_to_p0 is None) or distance > max_distance_to_p0:
           max_distance_to_p0 = distance
           index_point_with_max_distance = tmp[i]

    # print('Found point farthest away from p_0: {}'.format(index_point_with_max_distance))

    # Determine indexes of point that should be deleted.
    for i in range(0, len(tmp)):
        if tmp[i] != index_point_with_max_distance:
            to_delete.append(tmp[i])

    # print('Points to be deleted: {}'.format(to_delete))
    return to_delete

graham_scan(input_points)

