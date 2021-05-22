from matplotlib.pyplot import imread
def load_pics():

    pics = {}
    # pics['backgr'] = imread('./images/backgr_small1.png')  # 482, 187
    pics['backgr'] = imread('./images/backgr_small1.png')  # 482, 187
    pics['smoke_r_f'] = imread('./images/smokes/smoke_r_f.png')
    pics['smoke3'] = imread('./images/smokes/smoke3_6_115.png')
    pics['wave1'] = imread('./images/waves/wave1.png')  # 69, 35
    pics['wave2'] = imread('./images/waves/wave2.png')  # 69, 35
    pics['ship3'] = imread('./images/ships/ship3.png')  # 105, 145
    pics['explosion'] = imread('./images/expls/explosion.png')
    return pics