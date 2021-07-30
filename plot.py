
from convex_hull import graham_scan
import matplotlib.pyplot as plt

# Original points.
points = [(4.4, 14), (6.7, 15.25), (6.9, 12.8), (2.1, 11.1), (9.5, 14.9), 
    (13.2, 11.9), (10.3, 12.3), (6.8, 9.5), (3.3, 7.7), (0.6, 5.1), (5.3, 2.4), 
    (8.45, 4.7), (11.5, 9.6), (13.8, 7.3), (12.9, 3.1), (11, 1.1)]

convex_hull = graham_scan(points)

x_values = []
y_values  = []

for i in range(0, len(convex_hull)):
    x_values.append(convex_hull[i][0])
    y_values.append(convex_hull[i][1])

x_values.append(convex_hull[0][0])
y_values.append(convex_hull[0][1])

plt.plot(x_values, y_values, '-d', color='c', markersize=8, markerfacecolor='m', markeredgecolor='m', label='Path of the convex hull')

x_values = []
y_values  = []

for i in range(0, len(points)):
    if not(points[i] in convex_hull):
        x_values.append(points[i][0])
        y_values.append(points[i][1])

plt.plot(x_values, y_values, 'o', color='black', markersize=8);

plt.title("Convex hull")
plt.xlabel("x")
plt.ylabel("y");
plt.legend()

plt.show()

