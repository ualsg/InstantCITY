import os
import sys
import time
import argparse
import concurrent.futures as futures

import requests
from PIL import Image
from tqdm import tqdm
from itertools import repeat
from util.tiles import tiles_from_list, fetch_image, get_tiles

import argparse
import csv
import json

from supermercado import burntiles
from tqdm import tqdm

def download_tiles(tiles, ouput_dir, type, rate=10):
    """download static raster tiles from mapbox

    Args:
        feature_path (str): path to the features.json
        ouput_dir (str): output directory
        type (str): building or street
        zoom (int, optional): zoom level for the xyz tile server. Defaults to 15.
        rate (int, optional): number of downloaders. Defaults to 10.
    """
    # specify styles with the default api key
    if type == 'street':
        api = 'https://api.mapbox.com/styles/v1/iceofsky1/cktpg74j90zb617o00ucnk66b/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiaWNlb2Zza3kxIiwiYSI6ImNraTF4ejIxaDBxNGgycm1zd3ZvMThwOGMifQ.-QrGKalxvWk3sY7BqDbI1Q'
    elif type == 'building':
        api = 'https://api.mapbox.com/styles/v1/iceofsky1/ckursyixh6llv17o7ao5kbcwn/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiaWNlb2Zza3kxIiwiYSI6ImNraTF4ejIxaDBxNGgycm1zd3ZvMThwOGMifQ.-QrGKalxvWk3sY7BqDbI1Q'
    elif type == 'highways':
        api = 'https://api.mapbox.com/styles/v1/iceofsky1/ckunrvm0m2avz17m0fnjctyql/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiaWNlb2Zza3kxIiwiYSI6ImNraTF4ejIxaDBxNGgycm1zd3ZvMThwOGMifQ.-QrGKalxvWk3sY7BqDbI1Q'
    elif type == 'primary':
        api = 'https://api.mapbox.com/styles/v1/iceofsky1/ckunrttip1uq117ryux2p2hao/tiles/{z}/{x}/{y}@2x?access_token=pk.eyJ1IjoiaWNlb2Zza3kxIiwiYSI6ImNraTF4ejIxaDBxNGgycm1zd3ZvMThwOGMifQ.-QrGKalxvWk3sY7BqDbI1Q'

    tiles = list(tiles_from_list(tiles))
    
    with requests.Session() as session:
        num_workers = rate

        # tqdm has problems with concurrent.futures.ThreadPoolExecutor; explicitly call `.update`
        # https://github.com/tqdm/tqdm/issues/97
        progress = tqdm(total=len(tiles), ascii=True, unit="image")

        with futures.ThreadPoolExecutor(num_workers) as executor:

            def worker(tile):
                tick = time.monotonic()

                x, y, z = map(str, [tile.x, tile.y, tile.z])
                # add address. 'Type' + 'Features.geojson'
                os.makedirs(os.path.join(ouput_dir, type, z, x), exist_ok=True)
                path = os.path.join(ouput_dir, type, z, x, "{}.{}".format(y, 'png'))

                if os.path.isfile(path):
                    return tile, True

                url = api.format(x=tile.x, y=tile.y, z=tile.z)

                res = fetch_image(session, url)
                if not res:
                    return tile, False
                
                try:
                    image = Image.open(res)
                    image.save(path, optimize=True)
                except OSError as e:
                    print(e)
                    return tile, False

                tock = time.monotonic()

                time_for_req = tock - tick
                time_per_worker = num_workers / rate

                if time_for_req < time_per_worker:
                    time.sleep(time_per_worker - time_for_req)

                progress.update()

                return tile, True

            for tile, ok in executor.map(worker, tiles):
                if not ok:
                    print("Warning: {} failed, skipping".format(tile), file=sys.stderr)

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("type", type=str, help="endpoint with {z}/{x}/{y} variables to fetch image tiles from")
    parser.add_argument("features", type=str, help="path to GeoJSON features file")
    parser.add_argument("--ext", type=str, default="png", help="file format to save images in")
    parser.add_argument("--rate", type=int, default=12, help="rate limit in max. requests per second")
    parser.add_argument("--zoom", type=int, default=15, help="zoom level for xyz tiles")
    parser.add_argument("out", type=str, help="path to slippy map directory for storing tiles")
    args = parser.parse_args()

    tiles = get_tiles(args.features, args.zoom)
    download_tiles(tiles, args.out, args.type, args.rate)