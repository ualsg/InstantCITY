from tqdm import tqdm
import cv2
import numpy as np
import geojson
from util.tiles import tiles_from_slippy_map
from util.features.building import Building_features
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("tile_dir", type=str, help="img dir containing predicted tiles")
parser.add_argument("out", type=str, help="path to GeoJSON to save merged features to")
parser.add_argument("--input_folder_name", type=str, default='input', help="input folder name in the same root folder as predicted tile")


def convert_binary(img_path):
    '''converts RGB imgs to binary images of (0,255) only

    '''
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # make every pixel brighter than 10 to 255(white), only keeping the buildings as dark.
    _, img = cv2.threshold(img, 45, 255, cv2.THRESH_BINARY)
    return img

def mask_to_feature(mask_dir, kernel_size_denoise, kernel_size_grow, simplify_threshold):

    # denoise is removing noises surrounding the images. ie cv2.MORPH_OPEN
    # grow is closing the gaps surrounding the images. ie cv2.MORPH_CLOSE
    # the approximation accuracy as max. percentage of the arc length
    # requires 3 settings of grow to get most polygons ready, 1, 3, 5
    handler = Building_features(kernel_size_denoise, kernel_size_grow , simplify_threshold)
    
    tiles = list(tiles_from_slippy_map(mask_dir))

    for tile, path in tqdm(tiles, ascii=True, unit="mask"):
        binary_img = convert_binary(path)
        mask = (binary_img == 0).astype(np.uint8)
        handler.apply(tile, mask)
    
    # output feature collection
    feature = handler.jsonify()
    
    return feature

if __name__=="__main__":
    args = parser.parse_args()
    features = mask_to_feature(args.tile_dir, kernel_size_denoise = 5, kernel_size_grow = 2, simplify_threshold = 0.008)
    with open(args.out, "w") as fp:
        geojson.dump(features, fp)