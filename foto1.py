# pip install rembg pillow

import numpy as np
from rembg import remove
from PIL import Image

fileName = "fabio.jpg"
imageFoto = Image.open(fileName)
imageArray = np.array(imageFoto)
imageArrayClear = remove(imageArray)

canal_alfa = imageArrayClear[:, :, 3]
coordenadas_alfa_zero = np.argwhere(canal_alfa != 0)
x_inicio = coordenadas_alfa_zero[:, 1].min()
x_fim = coordenadas_alfa_zero[:, 1].max()
y_inicio = coordenadas_alfa_zero[:, 0].min()
y_fim = coordenadas_alfa_zero[:, 0].max()
print(x_inicio, y_inicio, x_fim, y_fim)

cropImageClear = imageArrayClear[y_inicio:y_fim, x_inicio:x_fim]

imageClear = Image.fromarray(cropImageClear)
imageClear.save(fileName.replace(".jpg", "-remove.png"))
