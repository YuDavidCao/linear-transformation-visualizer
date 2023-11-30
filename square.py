import numpy as np

sqaure_vertices = np.array(
    [
        (0, 0, 0, 1),
        (0, 1, 0, 1),
        (1, 1, 0, 1),
        (1, 0, 0, 1),
        (0, 0, 1, 1),
        (0, 1, 1, 1),
        (1, 1, 1, 1),
        (1, 0, 1, 1),
    ]
)

square_faces = np.array(
    [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
        (0, 4, 5, 1),
        (2, 3, 7, 6),
        (1, 2, 6, 5),
        (0, 3, 7, 4),
    ]
)