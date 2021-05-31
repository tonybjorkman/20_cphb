import os

from matplotlib.pyplot import imread
def load_pics():

    pics = {}
    pics['waves'] = {}
    pics['ships'] = {}
    pics['sails'] = {}
    pics['smokas'] = {}
    pics['smokrs'] = {}
    pics['explosions'] = {}
    pics['backgr'] = imread('./images_mut/backgr_small1.png')  # 482, 187
    # pics['backgr'] = imread('./images_mut/backgr_new1.png')  # 482, 187
    for i in range(5):
        pics['smokrs']['smokr_' + str(i)] = imread('./images_mut/smokrs/smokr_' + str(i) + '.png')

    pics['smokas']['smoka_0'] = imread('./images_mut/smokas/smoka_0.png')
    pics['smokas']['smoka_1'] = imread('./images_mut/smokas/smoka_1.png')
    pics['smokas']['smoka_2'] = imread('./images_mut/smokas/smoka_2.png')
    pics['smokas']['smoka_3'] = imread('./images_mut/smokas/smoka_3.png')
    pics['smokas']['smoka_4'] = imread('./images_mut/smokas/smoka_4.png')
    pics['waves']['wave1s'] = imread('./images_mut/waves/wave1s.png')  # 69, 35
    pics['waves']['wave2s'] = imread('./images_mut/waves/wave2s.png')  # 69, 35
    pics['ships']['ship_3'] = imread('./images_mut/ships/ship_3.png')  # 105, 145
    pics['ships']['ship_1'] = imread('./images_mut/ships/ship_1.png')  # 105, 145
    pics['explosions']['explosion_0'] = imread('./images_mut/expls/explosion_0.png')
    PATH = './images_mut/sails'
    _, _, file_names = os.walk(PATH).__next__()
    for file_name in file_names:
        pics['sails'][file_name[:-4]] = imread(PATH + '/' + file_name)  # without .png

        gg = 5

    # pics['sails']['sail_3_0_20_68'] = imread('./images_mut/sails/sail_3_0_20_68.png')
    # pics['sails']['sail_3_1_53_79'] = imread('./images_mut/sails/sail_3_1_53_79.png')
    return pics