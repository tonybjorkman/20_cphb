# TODO: Stray white pixels over areas where some movement is desired.

import os
import numpy as np
from matplotlib.pyplot import imread, imsave
from PIL import Image

# os.remove(<file name>)
# image_names = os.listdir('images_orig')
_, folder_names, _ = os.walk('./images_raw').__next__()

for folder_name in folder_names:
    _, _, file_names = os.walk('./images_raw/' + folder_name).__next__()
    for file_name in file_names:
        pic = imread('./images_raw/' + folder_name + '/' + file_name)
        if pic.shape[2] == 3:
            alpha_ = np.full((pic.shape[0], pic.shape[1]), 1)
            pic = np.dstack((pic, alpha_))

        array_binary = np.where(pic[:, :, 1] == 1.0, 0.0, 1)  # where alpha should be 1, and 0 otherwise
        pic[:, :, 3] = np.multiply(array_binary, np.ones_like(pic[:, :, 2]))  # alpha set to 0 in correct places

        imsave('./images_mut/' + folder_name + '/' + file_name, pic)
    print("done folder " + str(folder_name))

