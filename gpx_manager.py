import gpxpy, gpxpy.gpx
import os
import csv
import datetime

def load_gpx_file(name, path='data/'):
    with open(os.path.join(path, name), 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)
    return gpx

def import_files():
    with open('output/locations.csv', 'r') as f:
        reader = csv.reader(f)
        try:
            next(reader)
            points = [row for row in reader]
            times = [int(row[0]) for row in points]
        except:
            times = []

    original_length = len(times)
    
    try:
        with open('output/completed.txt', 'r') as f:
            completed = f.read().splitlines()
    except:
        completed = []
    
    done = []
    for file in os.listdir('data/GPX'):
        if file.endswith('.gpx') and file not in completed:
            gpx = load_gpx_file(file, 'data/GPX')
            for track in gpx.tracks:
                for segment in track.segments:
                    for point in segment.points:
                        timestamp = int(point.time.timestamp())
                        if timestamp not in times:
                            points.append([timestamp, point.latitude, point.longitude])
            done.append(file)
            print('file {} processed'.format(file))
    
    print('{} new points imported\n{} files processed\n{} files skipped'.format(len(points) - original_length, len(done), len(completed)))

    with open('output/locations.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timeunix', 'latitude', 'longitude'])
        for point in points:
            writer.writerow(point)
    with open('output/completed.txt', 'a') as f:
        for file in done:
            f.write(file + '\n')
