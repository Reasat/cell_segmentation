from PIL import Image
import matplotlib.pyplot as  plt
import argparse
import os
import PIL
from tqdm import tqdm
PIL.Image.MAX_IMAGE_PIXELS = 9999999999
import tifffile
import numpy as np
from aicssegmentation.core.pre_processing_utils import \
    (intensity_normalization,
     suggest_normalization_param,
     edge_preserving_smoothing_3d)

parser = argparse.ArgumentParser()
parser.add_argument('--dir_src')
parser.add_argument('--dir_dst')
parser.add_argument('--max_size', help= 'max size in each dimension, e.g. --max_size 256 256', type=int, nargs='+')
args = parser.parse_args()

filepaths_src = []
dirNames = []
for dirName, subdirList, fileList in os.walk(args.dir_src):
    dirNames.append(dirName)
    for fname in fileList:
        filepaths_src.append(os.path.join(dirName,fname))
for dirName in dirNames:
    # print(dirName.replace(args.dir_src, args.dir_dst))
    os.makedirs(dirName.replace(args.dir_src, args.dir_dst), exist_ok=True)
# # path = r'E:\hackathon_data\Segmentation\SegmentationMiniData\Harvard_Lung\LUNG-1-LN\LUNG-1-LN_40X_8.tif'
for path_src in filepaths_src:
    print(path_src)
    path_dst = path_src.replace(args.dir_src, args.dir_dst)
    path_dst=  path_dst.replace('.tif', '.jpg')
    img = tifffile.imread(path_src)
    lower, upper = suggest_normalization_param(img)
    img_norm = intensity_normalization(img, [lower, upper])
    img = (img_norm*255).astype(np.uint8)
    print(img.shape, img.dtype)
    if len(img.shape)>2:
        for i in range(img.shape[0]):
            img_slice=Image.fromarray(img[i,:,:])
            img_slice.thumbnail(args.max_size)  # inplace operation
            path_dst_slice = path_dst.replace('.', '_{}.'.format(i))
            img_slice.save(path_dst_slice)
    else:
        img = Image.fromarray(img)
        img.thumbnail(args.max_size) # inplace operation
        img.save(path_dst)
    # break
