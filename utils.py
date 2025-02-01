import plotly.graph_objects as go


def create_cuboid_mesh(origin, size, color):
    x0, y0, z0 = origin
    dx, dy, dz = size

    x = [x0, x0 + dx, x0 + dx, x0, x0, x0 + dx, x0 + dx, x0]
    y = [y0, y0, y0 + dy, y0 + dy, y0, y0, y0 + dy, y0 + dy]
    z = [z0, z0, z0, z0, z0 + dz, z0 + dz, z0 + dz, z0 + dz]

    bottom_i = [0, 0]
    bottom_j = [1, 2]
    bottom_k = [2, 3]

    top_i = [4, 4]
    top_j = [5, 6]
    top_k = [6, 7]

    front_i = [0, 0]
    front_j = [1, 5]
    front_k = [5, 4]

    right_i = [1, 1]
    right_j = [2, 6]
    right_k = [6, 5]

    back_i = [2, 2]
    back_j = [3, 7]
    back_k = [7, 6]

    left_i = [3, 3]
    left_j = [0, 4]
    left_k = [4, 7]

    i = bottom_i + top_i + front_i + right_i + back_i + left_i
    j = bottom_j + top_j + front_j + right_j + back_j + left_j
    k = bottom_k + top_k + front_k + right_k + back_k + left_k

    return go.Mesh3d(
        x=x, y=y, z=z, i=i, j=j, k=k, color=color, opacity=1, flatshading=True
    )
