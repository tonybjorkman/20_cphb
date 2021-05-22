
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines
import scipy.integrate as integrate
import matplotlib.animation as animation
from matplotlib.pyplot import imread
from matplotlib.animation import ArtistAnimation

import numpy as np
from matplotlib.animation import ArtistAnimation

from pychubby.base import DisplacementField
from pychubby.visualization import create_animation


class TestCreateAnimation:
    """Collection of tests focused on the `create_animation` function."""

    def test_overall(self, face_img):
        shape = (10, 11)

        delta_x = np.random.random(shape)
        delta_y = np.random.random(shape)

        df = DisplacementField(delta_x, delta_y)
        ani = create_animation(df, face_img, fps=2, n_seconds=1)

        assert isinstance(ani, ArtistAnimation)

def test_overall(self, face_img):
    shape = (10, 11)

    delta_x = np.random.random(shape)
    delta_y = np.random.random(shape)

    df = DisplacementField(delta_x, delta_y)
    ani = create_animation(df, face_img, fps=2, n_seconds=1)

    assert isinstance(ani, ArtistAnimation)

def create_animation(df, img, include_backwards=True, fps=24, n_seconds=2, figsize=(8, 8), repeat=True):
    """Create animation from a displacement field.

    Parameters
    ----------
    df : DisplacementField
        Instance of the ``DisplacementField`` representing the coordinate transformation.

    img : np.ndarray
        Image.

    include_backwards : bool
        If True, then animation also played backwards after its played forwards.

    fps : int
        Frames per second.

    n_seconds : int
        Number of seconds to play the animation forwards.

    figsize : tuple
        Size of the figure.

    repeat : bool
        If True, then animation always replayed at the end.

    Returns
    -------
    ani : matplotlib.animation.ArtistAnimation
        Animation showing the transformation.

    Notes
    -----
    To enable animation viewing in a jupyter notebook write:
    ```
    from matplotlib import rc
    rc('animation', html='html5')
    ```

    """
    n_frames = int(n_seconds * fps)
    interval = (1 / fps) * 1000
    frames = []

    fig = plt.figure(figsize=figsize)
    plt.axis('off')

    for i in range(n_frames + 1):
        df_new = df * (i / n_frames)
        warped_img = df_new.warp(img)
        frames.append([plt.imshow(warped_img, cmap='gray')])

    if include_backwards:
        frames += frames[::-1]

    ani = ArtistAnimation(fig, frames, interval=interval, repeat=repeat)

    return ani


create_animation()