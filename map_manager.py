import folium
import csv

class Path:
    def __init__(self, points):
        self.points = points
        self.coords = [[float(point[1]), float(point[2])] for point in points]
        self.start_time = points[0][0]
        self.end_time = points[-1][0]

def load_points():
    with open('output/locations.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)
        points = [row for row in reader]
    return points

# analyse points and create paths from sets of points that are separated by more than 30 minutes
def create_paths(points):
    paths = []
    current_path = []
    for point in points:
        if not current_path:
            current_path.append(point)
        elif int(point[0]) - int(current_path[-1][0]) > 1800:
            paths.append(Path(current_path))
            current_path = [point]
        else:
            current_path.append(point)
    paths.append(Path(current_path))
    return paths

def create_map(paths):
    m = folium.Map(location=[paths[0].points[0][1], paths[0].points[0][2]], zoom_start=12)
    for path in paths:
        folium.PolyLine(path.coords, color='blue', weight=2.5, opacity=1).add_to(m)
    return m

def full_map():
    points = load_points()
    paths = create_paths(points)
    m = create_map(paths)
    m.save('output/map.html')