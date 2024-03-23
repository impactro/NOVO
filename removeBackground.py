from flask import request
from PIL import Image
from io import BytesIO
from rembg import remove

import numpy as np


def removeBackground():

    imagem = request.files["imagem"]
    img = Image.open(imagem)

    imageArray = np.array(img)
    imageArrayClear = remove(imageArray)

    # com base no programa foto1.py
    canal_alfa = imageArrayClear[:, :, 3]
    coordenadas_alfa_zero = np.argwhere(canal_alfa != 0)
    x_inicio = coordenadas_alfa_zero[:, 1].min()
    x_fim = coordenadas_alfa_zero[:, 1].max()
    y_inicio = coordenadas_alfa_zero[:, 0].min()
    y_fim = coordenadas_alfa_zero[:, 0].max()
    cropImageClear = imageArrayClear[y_inicio:y_fim, x_inicio:x_fim]

    img = Image.fromarray(cropImageClear)
    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)

    return output.read(), 200, {'Content-Type': 'image/png'}
