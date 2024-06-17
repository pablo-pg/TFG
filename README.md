<a name="readme-top"></a>

[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">Trabajo Final de Grado</h3>

  <p align="center">
    Por Pablo Pérez González
    <br />
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Índice</summary>
  <ol>
    <li>
      <a href="#introducción">Introducción</a>
      <ul>
        <li><a href="#tecnologías-principales">Tecnologías empleadas</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requisitos">Requisitos</a></li>
        <li><a href="#instalación">Instalación</a></li>
      </ul>
    </li>
    <li><a href="#uso">Uso</a></li>
    <li><a href="#licencia">Licencia</a></li>
    <li><a href="#autor">Autor</a></li>
    <li><a href="#referencias">Referencias</a></li>
  </ol>
</details>



<!-- INTRODUCCION -->
## Introducción

Este es el repositorio donde está almacenado todo el código desarrollado en mi TFG.  

Mi proyecto consiste en el desarrollo de una herramienta que utilice la Inteligencia Artificial para generar habitaciones automáticamente de forma tridimensional usando un proyecto en Unity. Para ello, se tuvo que desarrollar un conjunto de datos con el que posteriormente se entrenó un LoRA de Stable Diffusion. También se desarrolló una aplicación web con Flask que sea capaz de comunicarse con el modelo, generar una página web y permitir el acceso mediante APIs. Finalmente, también se desarrolló un proyecto en Unity que se conectó a la aplicación Flask.

Este repositorio se puede separar en:  
* Script que genera el conjunto de datos.
* Aplicación web desarrollada en Flask.
* Proyecto en Unity.

<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>



### Tecnologías principales

* [![Python][Python]][Python-url]
* [![Flask][Flask]][Flask-url]
* [![Unity][Unity]][Unity-url]

<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

Este proyecto no está pensado para ser instalado en múltiples dispositivos. De todos modos, si se quiere probar, a continuación se explicará como hacerlo.

### Requisitos

Debe tener instalado y habilitado el siguiente software.  

* Flask
  ```sh
  pip install Flask
  ```
  
* OpenCV
  ```sh
  pip install opencv-python
  ```

* ComfyUI - [Instalación](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#installing)
* Unity - [Descarga](https://unity.com/es/download)

### Instalación

1. Clonar el repo
   ```sh
   git clone https://github.com/pablo-pg/TFG.git
   ```
   
2. Cree un proyecto en Unity.  
3. Cree un objeto vacío e insértele el script.
4. Añada los prefabs y relaciónelos en el script, así como la URL de la API.
5. Descargue los modelos de IA a utilizar y almacénelos donde la documentación de ComfyUI lo indica.  
* [Modelo base usado - Stable Diffusion 1.5](https://huggingface.co/runwayml/stable-diffusion-v1-5/resolve/main/v1-5-pruned-emaonly.safetensors?download=true)
* [LoRA entrenado para este TFG](https://drive.google.com/file/d/180KBf5eriok5XHYrZH-2S08hPDD8IJZe/view?usp=drive_link)  

<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>


<!-- USAGE EXAMPLES -->
## Uso

Para el uso de este proyecto, debe tener varios servicios activados.  

1. Ejecute ComfyUI - [Repositorio](https://github.com/comfyanonymous/ComfyUI?tab=readme-ov-file#comfyui)  
2. Cargue el workflow deseado.  
3. Teniendo la configuración de desarrollador activada, le aparecerá el botón "Save (API Format)". Guarde el workflow o copielo en el portapapeles.
4. En la apliacación Flask, modifique `app.py` y en la variable `DEFAULT_PROMPT_JSON ` pegue su workflow. La versión del repositorio contiene el workflow y modelos usados para el TFG.
5. Ejecute la aplicación Flask con `python app.py`.
6. En el proyecto en Unity actualice la dirección web de la API, por defecto está un enlace de prueba.
7. Estando ejecutándose ComfyUI y la aplicación Flask, ejecute el proyecto en Unity.



<!-- LICENSE -->
## Licencia

Creado bajo MIT License. Ver `LICENSE.txt` para más información.




<!-- CONTACT -->
## Autor

Pablo Pérez González - alu0101318318@ull.edu.es

Enlace del repo: [https://github.com/pablo-pg/TFG](https://github.com/pablo-pg/TFG)




<!-- REFERENCIAS -->
## Referencias

* [ComfyUI](https://github.com/comfyanonymous/ComfyUI)


<p align="right">(<a href="#readme-top">Volver arriba</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
[license-shield]: https://img.shields.io/github/license/pablo-pg/TFG.svg?style=for-the-badge
[license-url]: https://github.com/pablo-pg/TFG/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[Flask]: https://img.shields.io/badge/Flask-35495E?style=for-the-badge&logo=flask
[Flask-url]: https://flask.palletsprojects.com/en/3.0.x/
[Unity]:  https://img.shields.io/badge/Unity-35495E?style=for-the-badge&logo=unity
[Unity-url]: [https://vuejs.org/](https://unity.com/es/)
[Python]: https://img.shields.io/badge/Python-35495E?style=for-the-badge&logo=python
[Python-url]: https://www.python.org/
