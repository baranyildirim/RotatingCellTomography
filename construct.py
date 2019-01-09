# construct.py
# Parse XML file and RCT data to create 3D model
# Use Pillow to work with TIFF files
import xml.etree.ElementTree as ET
from PIL import Image   
import numpy


xml_file = 'data\\20xm2v2.xml'
avi_file = 'data\\20xm2v2.avi'
tif_file = 'data\\20xm2v2.tif'

# Load TIFF using PIL/Pillow
tif_data = Image.open(tif_file)
print(tif_data.mode)

trackmate_xml_tree = ET.parse(xml_file)
trackmate_xml_tree_root = trackmate_xml_tree.getroot()

# Get tracks from <AllTracks> tag
tracks = trackmate_xml_tree_root.findall('./Model/AllTracks/Track')

# Keep track of spots for each track
track_spot_IDs = []
    
# For each track, get spot IDs
for track in tracks:
    print(track.get('name'))
    spot_count = int(track.get('NUMBER_SPOTS'))
    print(spot_count)
    # If spot count is less than 15 do not process track
    if spot_count < 15:
        continue
    track_spots = set()
    for edge in track.findall('./Edge'):
        track_spots.add(edge.get('SPOT_SOURCE_ID'))
        track_spots.add(edge.get('SPOT_TARGET_ID'))
    track_spots = sorted(track_spots)
    track_spot_IDs.append(track_spots)
    print(track_spots)

# For each spot in each track, seek the frame from the TIFF file
# Crop the frame based on the coordinates of the spot

for track in track_spot_IDs:
    new_frames = []
    new_tif = Image.new('I;16', (150, 150))
    for spot_id in track:
        spot_data = trackmate_xml_tree_root.find('./Model/AllSpots//Spot/[@ID="' + spot_id +'"]')
        frame = spot_data.get('FRAME')
        x_cord = spot_data.get('POSITION_X')
        y_cord = spot_data.get('POSITION_Y')
        print(spot_id, frame, x_cord, y_cord)

        tif_data.seek(int(frame))
        print(tif_data.tell())

        # Cropping bounds
        new_frames.append(tif_data.crop((float(x_cord) - 75 , float(y_cord) - 75, float(x_cord) + 75, float(y_cord) + 75)))

    new_tif.save("test.tif", save_all=True, append_images=new_frames)


    




        


    

    

    

    
    
