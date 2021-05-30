import matplotlib.pyplot as plt
from matplotlib.pyplot import imread

fig, ax = plt.subplots(figsize=(20, 12))
pic = imread('./images_mut/ship_infos/ship_3.png')  #482, 187
ax.imshow(pic, alpha=1)
plt.show()