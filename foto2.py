from flask import Flask, request
from PIL import Image
from io import BytesIO
from rembg import remove

import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NOVO Utils</title>
</head>
<body>
    <h1>Remoção de Fundo</h1>
    <form action="/upload" method="POST" enctype="multipart/form-data">
        <input type="file" name="imagem">
        <br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>"""

@app.route("/upload", methods=["POST"])
def upload():
    # Receber o arquivo de imagem e as variáveis do formulário
    imagem = request.files["imagem"]
    # variavel1 = request.form["variavel1"]
    # variavel2 = request.form["variavel2"]

    # Processar a imagem
    img = Image.open(imagem)
    # Aqui você pode fazer qualquer processamento na imagem usando PIL

    imageArray = np.array(img)
    imageArrayClear = remove(imageArray)

    canal_alfa = imageArrayClear[:, :, 3]
    coordenadas_alfa_zero = np.argwhere(canal_alfa != 0)
    x_inicio = coordenadas_alfa_zero[:, 1].min()
    x_fim = coordenadas_alfa_zero[:, 1].max()
    y_inicio = coordenadas_alfa_zero[:, 0].min()
    y_fim = coordenadas_alfa_zero[:, 0].max()
    print(x_inicio, y_inicio, x_fim, y_fim)

    cropImageClear = imageArrayClear[y_inicio:y_fim, x_inicio:x_fim]

    # Criar uma resposta com a imagem processada
    img = Image.fromarray(cropImageClear)
    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)

    return output.read(), 200, {'Content-Type': 'image/png'}

if __name__ == "__main__":
    app.run(debug=True)
