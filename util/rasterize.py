import argparse
import collections
import json
import os
import sys
import csv

import numpy as np
from PIL import Image
from tqdm import tqdm

import mercantile
from rasterio.crs import CRS
from rasterio.transform import from_bounds
from rasterio.features import rasterize
from rasterio.warp import transform
from supermercado import burntiles

from util.colors import make_palette
from util.tiles import tiles_from_list

def feature_to_mercator(feature):
    """Normalize feature and converts coords to 3857.

    Args:
      feature: geojson feature to convert to mercator geometry.
    """
    # Ref: https://gist.github.com/dnomadb/5cbc116aacc352c7126e779c29ab7abe

    src_crs = CRS.from_epsg(4326)
    dst_crs = CRS.from_epsg(3857)

    geometry = feature["geometry"]
    if geometry["type"] == "Polygon":
        xys = (zip(*part) for part in geometry["coordinates"])
        xys = (list(zip(*transform(src_crs, dst_crs, *xy))) for xy in xys)

        yield {"coordinates": list(xys), "type": "Polygon"}

    elif geometry["type"] == "MultiPolygon":
        for component in geometry["coordinates"]:
            xys = (zip(*part) for part in component)
            xys = (list(zip(*transform(src_crs, dst_crs, *xy))) for xy in xys)

            yield {"coordinates": list(xys), "type": "Polygon"}


def burn(tile, features, size):
    """Burn tile with features.

    Args:
      tile: the mercantile tile to burn.
      features: the geojson features to burn.
      size: the size of burned image.

    Returns:
      image: rasterized file of size with features burned.
    """

    # the value you want in the output raster where a shape exists
    burnval = 1
    shapes = ((geometry, burnval) for feature in features for geometry in feature_to_mercator(feature))

    bounds = mercantile.xy_bounds(tile)
    transform = from_bounds(*bounds, size, size)

    return rasterize(shapes, out_shape=(size, size), transform=transform)

def generate_tiles(feature_path, ouput_dir, zoom, classes=['background', 'buildings'], colors= ['white', 'dark'], size=512):
    """rasterize input geojson features into xyz tiles

    Args:
        feature_path (str): input geojson feature collection
        ouput_dir (str): output dir for tiles
        zoom (int): zoom level for xyz tiles
        classes (list, optional): name of classes for the features. Defaults to ['background', 'buildings'].
        colors (list, optional): name of color mappings for the classes. Defaults to ['white', 'dark'].
        size (int, optional): size of output tiles. Defaults to 512.
    """
    assert len(classes) == len(colors), "classes and colors coincide"
    
    bg = colors[0]
    fg = colors[1]

    with open(feature_path) as f:
        fc = json.load(f)

    feature_map = collections.defaultdict(list)
    tiles = [] 

    for i, feature in enumerate(tqdm(fc["features"], ascii=True, unit="feature")):

        if feature["geometry"]["type"] != "Polygon":
            continue

        # get tiles      
        try:
            tiles.extend(map(tuple, burntiles.burn([feature], zoom).tolist()))
        except:
            pass
    
        # Find all tiles the features cover and make a map object for quick lookup.
        try:
            for tile in burntiles.burn([feature], zoom=zoom):
                feature_map[mercantile.Tile(*tile)].append(feature)
        except ValueError as e:
            print("Warning: invalid feature {}, skipping".format(i), file=sys.stderr)
            continue

    tiles = list(set(tiles))        
    # Burn features to tiles and write to a slippy map directory.
    
    for tile in tqdm(tiles_from_list(tiles), ascii=True, unit="tile"):
        if tile in feature_map:
            out = burn(tile, feature_map[tile], size)
        else:
            out = np.zeros(shape=(size, size), dtype=np.uint8)

        out_dir = os.path.join(ouput_dir, 'building', str(tile.z), str(tile.x))
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "{}.png".format(tile.y))

        if os.path.exists(out_path):
            prev = np.array(Image.open(out_path))
            out = np.maximum(out, prev)

        out = Image.fromarray(out, mode="P")
        palette = make_palette(bg, fg)
        out.putpalette(palette)
        out.save(out_path, optimize=True)


if __name__=='__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("features", type=str, help="path to GeoJSON features file")
    parser.add_argument("out", type=str, help="directory to write converted images")
    parser.add_argument("--zoom", type=int, required=True, help="zoom level of tiles")
    parser.add_argument("--size", type=int, default=512, help="size of rasterized image tiles in pixels")
    args = parser.parse_args()
    
    classes = ['background', 'buildings']
    colors  = ['white', 'dark']

    generate_tiles(args.features, args.out, args.zoom, classes, colors, args.size)