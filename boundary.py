import construct
import cv2 as cv
from PIL import Image
import numpy
import random
import pickle
import scipy
from skimage.measure import compare_ssim as ssim

# Feature extractor
def extract_features(image, vector_size=32):
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        print("KPS: ", kps)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten()
        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = numpy.concatenate([dsc, numpy.zeros(needed_size - dsc.size)])
    except:
        print('Error')
        return None

    return dsc


def boundary_match():
    xml_file = 'data\\20xm2v2.xml'
    tif_file = 'data\\20xm2v2.tif'

    cropped_tif_files = construct.extract_cell(xml_file, tif_file)

    for tif_file_name in cropped_tif_files:
        cropped_tif_track = Image.open(tif_file_name)
        print(tif_file_name)
        tif_frame_features = []

        try:
            while True:
                #Perform future extraction for every frame
                tif_frame = numpy.array(cropped_tif_track)
                print("Frame: ", cropped_tif_track.tell())
                dsc = extract_features(tif_frame)
                if dsc is not None and len(dsc) > 0:
                    tif_frame_features.append(dsc)
                cropped_tif_track.seek(cropped_tif_track.tell() + 1)
        except EOFError:
            pass

        first_frame_features = tif_frame_features[0]
        first_frame_features = first_frame_features.reshape(1, -1)
        correlation_list = scipy.spatial.distance.cdist(tif_frame_features, first_frame_features, 'cosine').reshape(-1)
        print(correlation_list)
        correlation_list = correlation_list.tolist()
        max_cor_frame = correlation_list.index(max(correlation_list))
        print("Maximum correlation in frame: ", max_cor_frame)


        
if __name__ == "__main__":
    boundary_match()




