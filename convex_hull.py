
import math
from functools import cmp_to_key

points = [(1, 1), (2, 2), (3, 3), (1, 3)]
p_0 = None

# points = [(4.4, 14), (6.7, 15.25), (6.9, 12.8), (2.1, 11.1), (9.5, 14.9), 
# (13.2, 11.9), (10.3, 12.3), (6.8, 9.5), (3.3, 7.7), (0.6, 5.1), (5.3, 2.4), 
# (8.45, 4.7), (11.5, 9.6), (13.8, 7.3), (12.9, 3.1), (11, 1.1)]

def graham_scan(input_points):
    """
    Algorithm to find the convex hull for a set of
    two-dimensional points in the plane.
    """
    convex_hull = []
    points = input_points.copy()
    global p_0
    p_0 = find_p_0(points)
    # Consider only remaining points as p_0 is definitely part
    # of the hull.
    points.remove(p_0)

    # Sort points by polar angle between the vector of
    # the point p_0 to the current point and the unity vector in the
    # direction of the x axis.
    points = sorted(points, key=cmp_to_key(compare))
    points = remove_duplicates(points)
    
    # Insert p_0 at first position of the list of points again.
    points.insert(0, p_0)

    convex_hull = construct_convex_hull(points)

    return convex_hull


def find_p_0(points):
    """
    Finds the starting point for the convex hull.
    """
    p_0 = points[0]

    # Find the point with the lowest y coordinate.
    for i in range(1, len(points)):
        if points[i][1] < p_0[1]:
            p_0 = points[i]
        # If y coordinates of two points are the same, choose the
        # point with the lower x coordinate.
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

def compare(p_1, p_2):
    """
    Compare two points.
    """
    v_x_axis = (1, 0)
 
    # Compute vectors from reference point p_0 to the point for
    # each point.
    v_1 =  (p_1[0] - p_0[0], p_1[1] - p_0[1])
    v_2 = (p_2[0] - p_0[0], p_2[1] - p_0[1])

    # Compute angle between vector and x axis.
    angle_1 = angle_between(v_1, v_x_axis)
    angle_2 = angle_between(v_2, v_x_axis)

    if angle_1 < angle_2:
        return -1

    elif angle_1 > angle_2:
        return 1
    
    else:
        # If the angles are equal, put the point that
        # is closer to p_0 in x direction first.
        if p_1[0] < p_2[0]:
            return -1

        elif p_1[0] > p_2[0]:
            return 1
        else:
            return 0

def remove_duplicates(points):
    """
    If multiple points have the same angle, remove
    all except the one farthest away from p_0.
    """
    # Stores indizes of points already looked at.
    visited = []
    indizes_points_to_delete = []
    tmp = []
    v_x_axis = (1, 0)

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
        # Found multiple points that have the same angle.
        if len(tmp) > 1:
            indizes_points_to_delete += points_to_delete(points, tmp)
        tmp = []

    points_duplicates_removed = points.copy()

    # Delete points that should be deleted.
    for i in range(0, len(indizes_points_to_delete)):
        index_point_to_delete = indizes_points_to_delete[i]
        points_duplicates_removed.remove(points[index_point_to_delete])

    return points_duplicates_removed

def compute_vector(p_1, p_2):
    """
    Returns the vector based on two points.
    """
    vector = (p_2[0] - p_1[0], p_2[1] - p_1[1]) 
    return vector

def euclidean_distance(p_1, p_2):
    """
    Compute the euclidean distance between two points.
    """
    a = p_2[0] - p_1[0]
    b = p_2[1] - p_1[1]
    distance = math.sqrt((a * a) + (b * b))
    return distance

def points_to_delete(points, tmp):
    """
    Determine what points can be deleted. Only
    keep the point that is farthest away from p_0.
    """
    max_distance_to_p0 = None
    index_point_with_max_distance = None
    indizes_points_to_delete = []

    for i in range(0, len(tmp)):
        index_of_point = tmp[i]
        distance = euclidean_distance(p_0, points[index_of_point])
        if (max_distance_to_p0 is None) or distance > max_distance_to_p0:
           max_distance_to_p0 = distance
           index_point_with_max_distance = index_of_point

    # Determine indexes of points that should be deleted.
    for i in range(0, len(tmp)):
        index_of_point = tmp[i]
        if index_of_point != index_point_with_max_distance:
            indizes_points_to_delete.append(index_of_point)

    return indizes_points_to_delete

def construct_convex_hull(points):
    """
    Constructs the convex hull based on points
    that are already presorted.
    """
    if len(points) < 3:
        # There is no convex hull for this list of points.
        return None
    
    stack = []
    stack.append(points[0])
    stack.append(points[1])
    stack.append(points[2])

    # Process remaining points.
    for i in range(3, len(points)):
        is_orientation_counterclockwise = False

        a = stack[len(stack) - 2]
        b = stack[len(stack) -1]
        # Current point looked at.
        c  = points[i]

        # If the orientation of the path of a to b to c is counter-clockwise.
        if orientation(a, b, c) > 0:
            is_orientation_counterclockwise = True
        
        while not is_orientation_counterclockwise:
            stack.pop()
            a = stack[len(stack) - 2]
            b = stack[len(stack) -1]

            if orientation(a, b, c) > 0:
                is_orientation_counterclockwise = True

        # At this point the orientation is counter-clockwise.
        stack.append(points[i])

    # Return the convex hull.
    return stack

def orientation(a, b, c):
    """
    Computes the orientation of the path of point a to b to c.
    """

    # If the result is 0, the points are collinear.
    # If it is positive, the orientation is counter-clockwise.
    # Otherwise the orientation is clockwise.
    result = (((b[0] - a[0]) * (c[1] - a[1])) - ((c[0] - a[0]) * (b[1] - a[1])))
    return result    

if __name__ == '__main__':
    print(graham_scan(points))

