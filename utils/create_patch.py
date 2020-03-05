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
import math

parser = argparse.ArgumentParser()
parser.add_argument('--dir_src')
parser.add_argument('--dir_dst')
parser.add_argument('--size', help= 'patch size in each dimension (height, width), e.g. --size 256 256', type=int, nargs='+')
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
    # path_dst=  path_dst.replace('.tif', '.jpg')
    img = tifffile.imread(path_src)
    # warning: pay attention to normalization; loss of precision due to int 16-->8 conversion
    lower, upper = suggest_normalization_param(img)
    img_norm = intensity_normalization(img, [lower, upper])
    img = (img_norm*255).astype(np.uint8)
    print(img.shape, img.dtype)
    if len(img.shape)>2:
        width, height = img.shape[1:3]
        height_new = math.ceil(height/args.size[0])*args.size[0]
        width_new = math.ceil(width/args.size[1])*args.size[1]
        width_range = np.arange(0, width, args.size[0])
        height_range = np.arange(0, height, args.size[1])
        for i in range(img.shape[0]):
            img_slice = Image.fromarray(img[i, :, :])
            bg= Image.new(mode='L',size=(width_new,height_new))
            bg.paste(img_slice,box=(0,0))
            for c in tqdm(width_range):
                for r in tqdm(height_range):
                    img_patch = bg.crop((c,r,c+args.size[1],r+args.size[0]))
                    path_dst_slice_patch = path_dst.replace('.', '_slice-{}_c-{}_r-{}.'.format(i,c,r))
                    img_patch.save(path_dst_slice_patch)
    else:
        width, height = img.shape
        height_new = math.ceil(height / args.size[0]) * args.size[0]
        width_new = math.ceil(width / args.size[1]) * args.size[1]
        width_range = np.arange(0, width, args.size[0])
        height_range = np.arange(0, height, args.size[1])
        bg = Image.new(mode='L', size=(width_new, height_new))
        img_pil = Image.fromarray(img)
        bg.paste(img_pil, box=(0, 0))
        for c in tqdm(width_range):
            for r in tqdm(height_range):
                img_patch = bg.crop((c, r, c + args.size[1], r + args.size[0]))
                path_dst_patch = path_dst.replace('.', '_c-{}_r-{}.'.format(c, r))
                img_patch.save(path_dst_patch)
