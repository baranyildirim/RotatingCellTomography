# construct.py
# Parse XML file and RCT data to produce cropped TIFFs with cells
# Use Pillow to work with TIFF files
import xml.etree.ElementTree as ET
from PIL import Image   
import os
import numpy
import operator

xml_file = 'data\\20xm2v2.xml'
tif_file = 'data\\20xm2v2.tif'

def extract_cell(xml_file, tif_file):
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
        #track_spots = sorted(track_spots)
        track_spot_IDs.append(track_spots)
        print(track_spots)

    track_spot_data = []
    # For each spot in each track, collect data about the spot
    for track in track_spot_IDs:
        spots = []
        for spot_id in track:
            spot_data = trackmate_xml_tree_root.find('./Model/AllSpots//Spot/[@ID="' + spot_id +'"]')
            frame = int(spot_data.get('FRAME'))
            x_cord = float(spot_data.get('POSITION_X'))
            y_cord = float(spot_data.get('POSITION_Y'))
            print("\n", spot_id, frame, x_cord, y_cord)
            spots.append((frame, x_cord, y_cord))
        #sort spot data by frame
        spots = sorted(spots, key=operator.itemgetter(0))
        track_spot_data.append(spots)


    # For each spot in each track, seek the frame from the TIFF file
    # Crop the frame based on the coordinates of the spot
    # Create TIFF files from the cropped frames  
    cropped_tif_files = []
    for idx, spots in enumerate(track_spot_data):
        new_frames = []
        for spot in spots:
            tif_data.seek(spot[0])
            print(tif_data.tell())
            # Cropping bounds
            x1 = spot[1] - 40
            y1 = spot[2] - 40
            if x1 < 0:
                x1 = 0
            if y1 < 0:
                y1 = 0
            x2 = x1 + 80
            y2 = y1 + 80
            print("Bounds: ", x1, y1, x2, y2)
            new_frames.append(tif_data.crop((x1, y1, x2, y2)))
        new_frames[0].save('Track' + str(idx) + '.tif', save_all=True, append_images=new_frames[1:])
        cropped_tif_files.append('Track' + str(idx) + '.tif')
    return cropped_tif_files

if __name__ == '__main__':
    extract_cell(xml_file, tif_file)

        


    

    

    

    
    
