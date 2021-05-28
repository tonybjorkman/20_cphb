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
    pics['smokrs']['smokr_3'] = imread('./images_mut/smokrs/smokr_3.png')
    pics['smokas']['smoka_3'] = imread('./images_mut/smokas/smoke3_6_115.png')
    pics['waves']['wave1'] = imread('./images_mut/waves/wave1.png')  # 69, 35
    pics['waves']['wave2'] = imread('./images_mut/waves/wave2.png')  # 69, 35
    pics['ships']['ship_3'] = imread('./images_mut/ships/ship_3.png')  # 105, 145
    pics['explosions']['explosion'] = imread('./images_mut/expls/explosion.png')
    pics['sails']['sail_3'] = imread('./images_mut/sails/sail3_11_66.png')
    return pics