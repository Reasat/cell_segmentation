from tiffile import imread
import matplotlib.pyplot as  plt
import numpy as np
from aicssegmentation.core.pre_processing_utils import \
    (intensity_normalization,
     suggest_normalization_param,
     edge_preserving_smoothing_3d)
path = r'E:\hackathon_data\Segmentation\Harvard_Lung\LUNG-1-LN\LUNG-1-LN_40X_1.tif'

img = imread(path)
lower, upper = suggest_normalization_param(img)
img_norm = intensity_normalization(img, [lower, upper])

print(img_norm.max())
# img_norm = img_norm[1000:1512,3000:3512]
plt.imshow(img_norm)
plt.show()