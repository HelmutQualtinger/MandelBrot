import matplotlib.pyplot as plt
import numpy as np
import numba
import webbrowser
import plotly.graph_objects as go


@numba.njit  # remove this line for debugging in python
def juliaset(width: int, height: int, x_min: float, x_max: float, y_min: float, y_max: float, max_iter: int, c: complex) -> np.ndarray:
    img = np.zeros((height, width))

    zval = np.zeros((height, width), dtype=np.complex128)

    for i in range(height):
        for j in range(width):
            x = x_min + (x_max - x_min) * j / (width - 1)
            y = y_min + (y_max - y_min) * i / (height - 1)
            z = complex(x, y)
            for k in range(max_iter):
                if abs(z) > 2:
                    break
                z = z * z + c
            img[i, j] = k
            zval[i, j] = z

    return img, zval


@numba.jit(nopython=True)  # remove this line for debugging in python
def mandelbrot(width: int, height: int, x_min: float, x_max: float, y_min: float, y_max: float, max_iter: int) -> tuple:
    img = np.zeros((height, width))
    zval = np.zeros((height, width), dtype=np.complex128)

    for i in range(height):
        for j in range(width):
            x = x_min + (x_max - x_min) * j / (width - 1)
            y = y_min + (y_max - y_min) * i / (height - 1)
            c = complex(x, y)
            z = 0+0j
            for k in range(max_iter):
                if abs(z) > 2:
                    break
                z = z * z + c
            img[i, j] = k
            zval[i, j] = z
    return img, zval


width = 15000
height = 8000
x_min = -2
x_max = 2
y_min = -1.5
y_max = 1.5
max_iter = 1000

img, z = juliaset(width, height, x_min, x_max,
                  y_min, y_max, max_iter, 0.5+0.5j)

# Calculate the absolute values of the heat values
img = np.log2(img + 1)

plt.figure(figsize=(100, 80))
# Save the image as a JPG file
plt.imshow(np.real(z), cmap='plasma_r',)
plt.axis('off')


# Save the image as a JPG file
plt.imshow(np.real(z), cmap='plasma_r',)
plt.axis('off')
plt.savefig('julia.jpg', bbox_inches='tight', pad_inches=0, dpi=300)

webbrowser.open('julia.jpg')
