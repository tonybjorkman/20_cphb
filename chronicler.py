import json
import random
import uuid

import PARAMS

SHIPS = ["1", "3"]
OVERWRITE = 1

class Chronicler:
    """
    Smokas are set only when big map is attempted.
    """

    def __init__(self):
        self.ch = {}
        self.init_chronicle()
        self.run()
        self.export()

    def init_chronicle(self):

        for ship_nid in SHIPS:
            with open('./utils/ship_infos/ship_' + ship_nid + '.json', 'r') as f:
                ship_template = json.load(f)

            self.ch["ship_" + ship_nid] = ship_template

    def run(self):

        for frame in range(PARAMS.FRAMES_START, PARAMS.FRAMES_STOP + 1):

            for ship_id, ship in self.ch.items():
                _r = random.random()
                if frame > 1 and _r < 0.2:  # firing prob
                    if _r < 0.1 and ship_id == 'ship_1':
                        ship['firing_frames'].append(frame)
                    elif ship_id == 'ship_3':
                        ship['firing_frames'].append(frame)



    def export(self):

        if OVERWRITE:
            name = 'chronicle'
        else:
            name = 'chronicle_' + str(uuid.uuid4())[0:4]

        with open('./utils/' + name + '.json', 'w') as f:
            json.dump(self.ch, f, indent=4)

if __name__ == "__main__":
    _ch = Chronicler()





