from flask import Flask, render_template, request
from PIL import Image
from io import BytesIO
from rembg import remove

import numpy as np

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("aplicaFundo.html")


@app.route("/card1", methods=["POST"])
def upload():

    fundo = request.form["fundo"]
    nome = request.form["nome"]
    cidade = request.form["cidade"]
    titulo = request.form["titulo"]
    imagem = request.files["imagem"]

    # pega a foto e remove o fundo
    img = Image.open(imagem)
    imageArray = np.array(img)
    imageArrayClear = remove(imageArray)

    # em breve em componentizo...!
    canal_alfa = imageArrayClear[:, :, 3]
    coordenadas_alfa_zero = np.argwhere(canal_alfa != 0)
    x_inicio = coordenadas_alfa_zero[:, 1].min()
    x_fim = coordenadas_alfa_zero[:, 1].max()
    y_inicio = coordenadas_alfa_zero[:, 0].min()
    y_fim = coordenadas_alfa_zero[:, 0].max()
    cropImageClear = imageArrayClear[y_inicio:y_fim, x_inicio:x_fim]

    # Lê a imagem de fundo
    imageFundo = Image.open(fundo)
    fundoArray = np.array(imageFundo)

    # Transforma a imagem cortada em um tamanho util
    # usando um regrinha de trez para não distorcer o tamanho
    # w1/h1 = w2/h2 => w1*h2 = w2*h1 => h2 = w2*h1 / w1
    fotoImage = Image.fromarray(cropImageClear)
    w1 = fotoImage.width
    h1 = fotoImage.height
    f = 1
    w3 = imageFundo.width * .7   # 70%
    h3 = imageFundo.height * .95 # 95%
    while True:
        w2 = int(imageFundo.width / f)
        h2 = int((w2*h1) / w1)
        if w2 < w3 and h2 < h3:
            print(f)
            break
        # vai diminuindo até a imagem caber
        f += .1

    fotoImage = fotoImage.resize((w2, h2))
    fotoArray = np.array(fotoImage)

    # Posiciona a foto dentro de uma nova área do mesmo tamanho
    areaFoto = np.zeros(fundoArray.shape, dtype=np.uint8)
    # alinha a foto no canto infoerior esquerdo
    y1 = imageFundo.height - fotoArray.shape[0]
    x1 = imageFundo.width - fotoArray.shape[1]
    y2 = y1 + fotoArray.shape[0]
    x2 = x1 + fotoArray.shape[1]
    areaFoto[y1:y2, x1:x2] = fotoArray

    # Extrair o canal alfa como máscara
    fotoMask = areaFoto[:, :, 3]

    # Aplicar a máscara para mesclar as imagens
    limiar = 200  # quanto menor mais contorno existe
    fundoArray[fotoMask > limiar] = areaFoto[fotoMask > limiar]

    output = BytesIO()
    img = Image.fromarray(fundoArray)
    img.save(output, format='PNG')
    output.seek(0)

    return output.read(), 200, {'Content-Type': 'image/png'}


if __name__ == "__main__":
    app.run(debug=True)
