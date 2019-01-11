import construct
import cv2 as cv
from PIL import Image
import numpy

xml_file = 'data\\20xm2v2.xml'
tif_file = 'data\\20xm2v2.tif'

cropped_tif_files = construct.extract_cell(xml_file, tif_file)

for tif in cropped_tif_files:
    tif_image = Image.open(tif)
    print(tif)

    try:
        while True:
            tif_frame = numpy.array(tif_image)
            print(tif_frame)
            tif_frame_edges = cv.Canny(tif_frame, 0, 150)
            cv.imshow('Image', tif_frame_edges)
            cv.waitKey(0)
            tif_image.seek(tif_image.tell() + 1)
    except EOFError:
        pass

