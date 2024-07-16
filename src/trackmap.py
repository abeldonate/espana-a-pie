import folium
from ipyleaflet import Map, Marker, Polyline
import gpxpy
import os
import yaml
import random

# Read the config
with open('config/config.yaml', 'r') as f:
    config_data = yaml.load(f, Loader=yaml.SafeLoader)

BASE_PATH = os.getcwd()
TRACKS_PATH = BASE_PATH + "/" + config_data.get("TRACKS_PATH")
TRACKS_HTML_PATH = BASE_PATH + "/" + config_data.get("TRACKS_HTML_PATH")
FOCUS_COORDINATES = config_data.get("FOCUS_COORDINATES")
LINE_WEIGHT = config_data.get("LINE_WEIGHT")
SMOOTH_FACTOR = config_data.get("SMOOTH_FACTOR")
ZOOM = config_data.get("ZOOM")

color_file = open(BASE_PATH + "/config/colors.hex")
COLORS = color_file.read().split("\n")
color_file.close()

STRING1 = """
"""

STRING2 = """,
        { "bubblingMouseEvents": true, "color": "#bb729f", "dashArray": null, "dashOffset": null, "fill": false, "fillColor": "#bb729f", "fillOpacity": 0.2, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1, "smoothFactor": 1.3, "stroke": true, "weight": 4 }
    ).addTo(map_e96cfa060f3da12267d01ed5d75dd1b1);


    poly_line_75772e934f8a570864941281b2b60152.bindTooltip(
        `<div style="font-size:2rem;">
                     <p><b>recorriendo toda puta elda #1 · 7.491 km</b></p> <p>08/08/22, 20:04:40 - 08/08/22, 21:43:58
                 </div>`,
        { "sticky": false }
    );

</script>
"""

base_map = Map(location=FOCUS_COORDINATES, zoom_start=ZOOM, tiles='CartoDBPositron') #tiles to reduce visual clutter

def _name_to_title(name):
    return name.strip(".gpx").replace("_", " ")

def get_html_tracklist():
    return ["tracks/" + s for s in os.listdir(TRACKS_HTML_PATH)]

def create_html_track(track_name):

    gpx_file = open(TRACKS_PATH + "/" + track_name, 'r')
    gpx = gpxpy.parse(gpx_file)
    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for gpxpoint in segment.points:
                points.append(tuple([gpxpoint.latitude, gpxpoint.longitude]))

    trackname = gpx.tracks[0].name
    time_bounds = gpx.get_time_bounds()
    length = gpx.length_3d()

    start_time, end_time = time_bounds.start_time.strftime("%d/%m/%y, %H:%M:%S"), time_bounds.end_time.strftime("%d/%m/%y, %H:%M:%S")

    with open(TRACKS_HTML_PATH + "/" + track_name.strip(".gpx") + ".html", "w") as file:

        file.write("""<script>

    tile_layer_5975b90028070c88ec26aa5871ada17c.addTo(map_e96cfa060f3da12267d01ed5d75dd1b1);

    var poly_line_55757239bcd43773f00c029b7185ca74 = L.polyline(""" 
    + str(points).replace("(", "[").replace(")", "]") +
    """,
        { "bubblingMouseEvents": true, "color": """
        "\""+ random.choice(COLORS) + "\","
    """ "dashArray": null, "dashOffset": null, "fill": false, "fillColor": "#bb729f", "fillOpacity": 0.2, "fillRule": "evenodd", "lineCap": "round", "lineJoin": "round", "noClip": false, "opacity": 1, "smoothFactor": 1.3, "stroke": true, "weight": 4 }
    ).addTo(map_e96cfa060f3da12267d01ed5d75dd1b1);


    poly_line_75772e934f8a570864941281b2b60152.bindTooltip(
        `<div style="font-size:2rem;">
    """
    + f"<p><b>{trackname} · {round(length/1000,3)} km</b></p> <p>{start_time} - {end_time}" + 
    """
                 </div>`,
        { "sticky": false }
    );

    </script>
    """
        )




def overlayGPX(tracks_path):
    result_map = folium.Map(location=FOCUS_COORDINATES, zoom_start=ZOOM, tiles='CartoDBPositron') #tiles to reduce visual clutter

    for i, gpx_path in enumerate(os.listdir(tracks_path)):
        print(gpx_path)
        gpx_file = open(tracks_path + "/" + gpx_path, 'r')
        gpx = gpxpy.parse(gpx_file)
        points = []
        for track in gpx.tracks:
            for segment in track.segments:
                for gpxpoint in segment.points:
                    points.append(tuple([gpxpoint.latitude, gpxpoint.longitude]))

        trackname = gpx.tracks[0].name
        time_bounds = gpx.get_time_bounds()
        length = gpx.length_3d()

        start_time, end_time = time_bounds.start_time.strftime("%d/%m/%y, %H:%M:%S"), time_bounds.end_time.strftime("%d/%m/%y, %H:%M:%S")

        pline = folium.PolyLine(
            points, color=COLORS[i], weight=LINE_WEIGHT, smooth_factor=SMOOTH_FACTOR ,opacity=1, tooltip=folium.map.Tooltip(f"<p><b>{trackname} · {round(length/1000,3)} km</b></p> <p>{start_time} - {end_time}", style="font-size:2rem;", sticky=False))

        result_map.add_child(pline)
        result_map.save(BASE_PATH + "/" + "resultingmap.html")


# create_html_track("b.gpx")

# print(get_html_tracklist())