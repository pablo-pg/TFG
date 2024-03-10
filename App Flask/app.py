from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import flask
import json
import urllib
import time

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
socketio = SocketIO(app)

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

# @app.route('/img/<path:filename>') 
# def send_file(filename): 
#     return send_from_directory(app.upload_folder, filename)

@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        try:

            new_text = flask.request.form['new_text']
            # Cargar el JSON predeterminado
            prompt = json.loads(DEFAULT_PROMPT_JSON)
            # Modificar la frase del prompt con la introducida por el usuario
            prompt["6"]["inputs"]["text"] = new_text
            # Enviar la solicitud a ComfyUI
            comfyui_response = json.loads(queue_prompt(prompt))
            logger.info(comfyui_response)

            prompt_id = comfyui_response['prompt_id']
            print('prompt_id:', {prompt_id})
            # Emitir mensaje para iniciar el procesamiento en el servidor WebSocket
            socketio.emit('start_processing', {'prompt_id': prompt_id}, namespace='/processing')
            # Esperar resultados del procesamiento
            output_images = get_images(prompt_id)

            # Generar una URL única para la primera imagen (puedes adaptarlo según tus necesidades)
            first_image_url = f'images/{prompt_id}.jpg'

            return render_template('result.html', output_images=first_image_url)
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
            print('Response with 200 code')
            # Acceder al contenido de la respuesta
            content = response.read().decode('utf-8')
            # print(content)
            return content
        else:
            print(f"Error en la solicitud. Código de estado: {response.getcode()}")
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error en la solicitud a ComfyUI: {str(e)}'})


def get_image(filename, subfolder, folder_type):
    try:
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        print(f'get the image: {url_values}')
        with urllib.request.urlopen(f"http://127.0.0.1:8188/view?{url_values}") as response:
            return response.read()
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al obtener la imagen: {str(e)}'})

def get_history(prompt_id):
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:8188/history/{prompt_id}") as response:
            return json.loads(response.read())
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error al obtener el historial: {str(e)}'})

def get_images(prompt_id):
    output_images = {}
    print('get_images')
    time.sleep(30)

    history = get_history(prompt_id)[prompt_id]
    print(f'got the history')
    for node_id in history['outputs']:
        node_output = history['outputs'][node_id]
        if 'images' in node_output:
            images_output = []
            for i, image in enumerate(node_output['images']):
                print(f'saving image {i}')
                image_data = get_image(image['filename'], image['subfolder'], image['type'])
                images_output.append(image_data)

                # Guardar cada imagen en el servidor (opcional)
                save_generated_image(image_data, f'{prompt_id}')

            output_images[node_id] = images_output

    return output_images



def save_generated_image(image_content, filename):
    with open(f'static/images/{filename}.jpg', 'wb') as f:
        f.write(image_content)

if __name__ == '__main__':
    app.run(debug=True)