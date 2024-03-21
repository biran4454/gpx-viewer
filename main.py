import gpx_manager
import map_manager

def main():
    gpx_manager.import_files()
    map_manager.full_map()

def clear_cache():
    gpx_manager.clear_cache()