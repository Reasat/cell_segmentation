import os

path_file_subset = r'E:\hackathon_data\Segmentation\representative-subset.txt'

with open(path_file_subset,'r') as f:
    flnames = [flname.strip() for flname in f.readlines()]
for fl in flnames:
    print(fl)

# centers = flname.split('/') [0] for flname in flnames