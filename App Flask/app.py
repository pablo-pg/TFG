from image_treatment import imageTreatment
from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS, cross_origin

import flask
import json
import logging
import urllib
import time

# Logger config
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Creating the app
app = Flask(__name__)
CORS(app) # Habilitar CORS para toda la aplicación

DEFAULT_PROMPT_JSON = """
{
    "3": {
        "inputs": {
            "seed": 1046630439646439,
            "steps": 20,
            "cfg": 8,
            "sampler_name": "euler",
            "scheduler": "normal",
            "denoise": 1,
            "model": [
                "10",
                0
            ],
            "positive": [
                "6",
                0
            ],
            "negative": [
                "7",
                0
            ],
            "latent_image": [
                "5",
                0
            ]
        },
        "class_type": "KSampler",
        "_meta": {
        "title": "KSampler"
        }
    },
    "4": {
        "inputs": {
        "ckpt_name": "v1-5-pruned-emaonly.safetensors"
        },
        "class_type": "CheckpointLoaderSimple",
        "_meta": {
        "title": "Load Checkpoint"
        }
    },
    "5": {
        "inputs": {
        "width": 512,
        "height": 512,
        "batch_size": 1
        },
        "class_type": "EmptyLatentImage",
        "_meta": {
        "title": "Empty Latent Image"
        }
    },
    "6": {
        "inputs": {
        "text": "TFGMapPablo map of a square room where there is a very big chair at center left, a small chair at bottom right, a very big chair at top right, a big door at center right and a very big table at bottom left",
        "clip": [
            "10",
            1
        ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
        "title": "CLIP Text Encode (Prompt)"
        }
    },
    "7": {
        "inputs": {
        "text": "text, watermark",
        "clip": [
            "10",
            1
        ]
        },
        "class_type": "CLIPTextEncode",
        "_meta": {
        "title": "CLIP Text Encode (Prompt)"
        }
    },
    "8": {
        "inputs": {
        "samples": [
            "3",
            0
        ],
        "vae": [
            "4",
            2
        ]
        },
        "class_type": "VAEDecode",
        "_meta": {
        "title": "VAE Decode"
        }
    },
    "9": {
        "inputs": {
        "filename_prefix": "ComfyUI",
        "images": [
            "8",
            0
        ]
        },
        "class_type": "SaveImage",
        "_meta": {
        "title": "Save Image"
        }
    },
    "10": {
        "inputs": {
        "lora_name": "lora.safetensors",
        "strength_model": 1,
        "strength_clip": 1,
        "model": [
            "4",
            0
        ],
        "clip": [
            "4",
            1
        ]
        },
        "class_type": "LoraLoader",
        "_meta": {
        "title": "Load LoRA"
        }
    }
}
"""

# Check if api works POST petition
@app.route('/test-api', methods=['POST'])
@cross_origin()
def test():
    print("Before JSON")
    data = request.json
    print(data)
    return jsonify({'message': 'Imagen generada correctamente'})


@app.route('/', methods=['GET', 'POST'])
@cross_origin()
def index():
    if flask.request.method == 'POST':
        new_text = ''
        is_web_request = False
        try:
            # Se intenta obtener el prompt por petición API. Si no funciona se lee desde la web
            try:
                new_text = request.json
                # print('prompt got via api')
            except:
                print('prompt got via web')
                is_web_request = True
                new_text = flask.request.form['new_text']
            
            # Cargar el JSON predeterminado
            prompt = json.loads(DEFAULT_PROMPT_JSON)
            # Modificar la frase del prompt con la introducida por el usuario
            prompt["6"]["inputs"]["text"] = new_text

            # Enviar la solicitud a ComfyUI
            comfyui_response = json.loads(queue_prompt(prompt))
            # print(f'comfyui response: {comfyui_response}')

            prompt_id = comfyui_response['prompt_id']
            print('Prompt ID:', {prompt_id})

            # Esperar resultados del procesamiento
            output_images = get_images(prompt_id)

            # Generar una ruta única para la imagen
            first_image_url = f'static/images/{prompt_id}.jpg'

            # Se obtienen los datos de la imagen
            fortniture_data = imageTreatment(first_image_url)

            if is_web_request:
                # Se descarga la imagen
                return send_file(first_image_url, as_attachment=True)
            else:
                return jsonify(fortniture_data)
            # return render_template('result.html', output_images=first_image_url)
        except Exception as e:
            print(f"Error en la aplicación Flask: {str(e)}")
            return jsonify({'status': 'error', 'message': 'Se produjo un error en la aplicación', 'error': str(e)})
    return render_template('index.html')

def queue_prompt(prompt):
    try:
        p = {"prompt": prompt}
        data = json.dumps(p).encode('utf-8')
        print('Sending data')
        req = urllib.request.Request("http://127.0.0.1:8188/prompt", data=data)
        print('Sending request')
        response = urllib.request.urlopen(req)

        if response.getcode() == 200:
            print('ComfyUI response with 200 code')
            content = response.read().decode('utf-8')
            return content
        else:
            print(f"Error en la solicitud. Código de estado: {response.getcode()}")
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error en la solicitud a ComfyUI: {str(e)}'})

# Obtiene una imagen
def get_image(filename, subfolder, folder_type):
    try:
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen(f"http://127.0.0.1:8188/view?{url_values}") as response:
            return response.read()
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al obtener la imagen: {str(e)}'})

# Comprueba si la imagen ya ha sido generada previamente
def get_history(prompt_id):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}") as response:
            return json.loads(response.read())
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al obtener el historial: {str(e)}'})

# Genera la imagen
def get_images(prompt_id):
    try:
        output_images = {}
        print('get_images')
        # time.sleep(55)
        while True:
            try:
                history = get_history(prompt_id)[prompt_id]
                break
            except:
                pass
        print('Image generated')
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for i, image in enumerate(node_output['images']):
                    print(f'Saving image')
                    image_data = get_image(image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)

                    # Guardar cada imagen en el servidor
                    save_generated_image(image_data, f'{prompt_id}')

                output_images[node_id] = images_output

        return output_images
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al obtener las imagenes en get_images: {str(e)}'})
    
def save_generated_image(image_content, filename):
    with open(f'static/images/{filename}.jpg', 'wb') as f:
        f.write(image_content)

if __name__ == '__main__':
    app.run(debug=True)