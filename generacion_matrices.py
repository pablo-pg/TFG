import numpy as np
import random
import os
import cv2

ruta_base = 'F:/TFG/Generación matrices/data'

class Room:
  objects = ["table", "chair", "door"]

  # Constructor
  # Se le pasa el tamaño de la habitación mediante un par, p.e. size=(10,20)
  def __init__(self, size):
    self.matrix = np.zeros(size, dtype=int)
    self.text = []
    self.objectsCount = {}


  # Varia el inicio de la frase para que se permita de formas diferentes
  def _randomStartText(self):
    text = "TFGPabloMap"
    map = "map" 
    of_a = "of a"
    square = "square"
    room = "room"
    where_there = "where there"
    with_ = "with"
    random.seed()
    if random.randint(0, 100) % 2:
      text =  text + " " + map        # TFGPabloMap map
      if random.randint(0, 100) % 2:
        text =  text + " " + of_a     # TFGPabloMap map of a
        if random.randint(0, 100) % 2:
          text =  text + " " + square 
        text =  text + " " + room    # TFGPabloMap map of a square room
        if random.randint(0,100) % 2:
          text =  text + " " + where_there          # TFGPabloMap map of a square room where there
        else:
          text =  text + " " + with_                # TFGPabloMap map of a square room with
      elif random.randint(0, 100) % 2:
        text =  text + " " + where_there              # TFGPabloMap map where there
      else:
        text =  text + " " + with_                    # TFGPabloMap map with
    else:
      if random.randint(0, 100) % 2:
        text =  text + " " + square
      text = text + " " + room                        # TFGPabloMap room
      if random.randint(0, 100) % 2:
        text =  text + " " + where_there              # TFGPabloMap room where there
      else:
        text =  text + " " + with_                    # TFGPabloMap room whith
    text = text + " "
    return text


  # Se inserta un objeto a la matriz
  # :Params
  # objectName:str :- Nombre del elemento a añadir
  # objectSize: int :- Tamaño del elemento
  # position: str :- Posición donde se añadirá
  def addObject(self, objectName: str, objectSize: int, position: str):
    # Calculo el valor que tendra en la matriz segun el diccionario de elementos validos
    objectValue = self.objects.index(objectName) + 1

    size_str = ""
    if objectSize == 1:
      size_str = "small"
    elif objectSize == 2:
      size_str = "medium"
    elif objectSize == 3:
      size_str = "big"
    else:
      size_str = "very big"

    # Calculo las esquina sup-izq
    submatrix_size = objectSize
    up_left_corner_y = None
    up_left_corner_x = None
    # Posicion en eje y
    if "top" in position or "up" in position:
      up_left_corner_y = 0
    elif "bottom" in position or "down" in position:
      up_left_corner_y = (self.matrix.shape[0] - objectSize)
    elif ("center" in position or "middle" in position) and not ("top" in position or "bottom" in position):
      up_left_corner_y = (self.matrix.shape[0] - objectSize) // 2
    else:    # No se introdujo informacion del eje y
      possibilities = [0, (self.matrix.shape[0] - objectSize), (self.matrix.shape[0] - objectSize) // 2]
      up_left_corner_y = possibilities[random.randint(0,10) % 3]
    # Posicion en eje x
    if "left" in position:
      up_left_corner_x = 0
    elif "right" in position:
      up_left_corner_x = (self.matrix.shape[1] - objectSize)
    elif ("center" in position or "middle" in position) and not ("left" in position or "right" in position):
      up_left_corner_x = (self.matrix.shape[1] - objectSize) // 2
    else:    # No se introduzco informacion del eje x, se elige al azar
      possibilities = [0, (self.matrix.shape[1] - objectSize), (self.matrix.shape[1] - objectSize) // 2]
      up_left_corner_x = possibilities[random.randint(0,10) % 3]

    # Se comprueba si se superponen
    if np.sum(self.matrix[up_left_corner_y : up_left_corner_y + submatrix_size,
               up_left_corner_x : up_left_corner_x + submatrix_size]) > 0:
      # print(f'    OVERLAP, {objectName} in {up_left_corner_y}')
      pass
    if objectName == "door" and (position == "center" or position == "middle"):
      pass
    else:
      if not objectName in self.objectsCount:
        self.objectsCount[objectName] = {
          # "count": 1,
          "values": [(position, size_str)]
        }
      else:
        self.objectsCount[objectName]["values"].append((position, size_str))
      self.matrix[up_left_corner_y : up_left_corner_y + submatrix_size,
               up_left_corner_x : up_left_corner_x + submatrix_size] = np.full((submatrix_size, submatrix_size), objectValue)

  # Genera el texto a partir de la matriz en modo lista "3 de X, 5 de Y, etc"
  def list_prompt(self):
    # Modo lista
    # text = "TFGMapPablo map of a square room where there "
    text = self._randomStartText()
    if text[-2] == "e":   # Para saber si termina en there is/are o with
      text += "is "
    if len(self.objectsCount.keys()) == 1:
      for position, size_str in self.objectsCount[list(self.objectsCount.keys())[0]]["values"]:
        text += "a "
        if random.randint(0, 5) % 2:
          text += size_str + " "
        text += list(self.objectsCount.keys())[0]
        if  random.randint(0, 5) % 2:
          text += " at "
        else:
          text += " in "
        text += position + ", "
    else:
      for roomObject in self.objectsCount:
        if roomObject == list(self.objectsCount.keys())[-1]:
          text = text[:-2]
          text += " and "
        for position, size_str in self.objectsCount[roomObject]["values"]:
          text += "a "
          if random.randint(0, 5) % 2:
            text += size_str + " "
          text += roomObject
          if random.randint(0, 5) % 2:
            text += " at "
          else:
            text += " in "
          text += position + ", "
    text = text[:-2]
    self.text.append(text)

  def generateImage(self):
    # Obtener todos los valores únicos en la matriz
    valores_unicos = np.array([0, 1, 2, 3, 4])

    # Obtener el valor máximo en la matriz
    max_valor = valores_unicos.max()

    # Generar una paleta de colores HSV con suficientes colores para cubrir todos los valores posibles
    colores_hsv = np.zeros((max_valor + 1, 1, 3), dtype=np.uint8)
    colores_hsv[:, 0, 0] = np.linspace(0, 179, max_valor + 1)  # Tonos (0 a 179)
    colores_hsv[:, 0, 1] = 255  # Saturación constante
    colores_hsv[:, 0, 2] = 255  # Valor constante

    # Convertir la paleta HSV a formato RGB
    colores_rgb = cv2.cvtColor(colores_hsv, cv2.COLOR_HSV2RGB)

    # Crear un diccionario para asignar colores a valores únicos
    color_dict = {valor: colores_rgb[valor][0][::-1] for valor in valores_unicos}

    # Crear una matriz de colores utilizando el diccionario
    matriz_colores = np.array([[color_dict[valor] for valor in fila] for fila in self.matrix])

    # Convertir la matriz de colores a formato uint8
    matriz_colores = matriz_colores.astype(np.uint8)

    # Crear la imagen con OpenCV
    imagen = cv2.cvtColor(matriz_colores, cv2.COLOR_RGB2BGR)

    imagen = cv2.resize(imagen, (512, 512), interpolation=cv2.INTER_NEAREST)
    return imagen
  
database_size = 150000
# database_size = 100
room_size = (15, 15)
limit_of_elements = (1, 10)
elements_types = len(Room.objects)
images_width = 1024
positions = [
    "top left", "left top", "center top", "top center", "top right", "right top", "top",
    "left", "center left", "left center", "center", "center right", "right center", "right",
    "bottom left", "left bottom", "center bottom", "bottom center", "bottom right", "right bottom", "bottom"
]

all_rooms = []
random.seed()
for i in range(database_size):
  print("room ", i + 1)
  room = Room(room_size)
  number_elements = random.randint(limit_of_elements[0], limit_of_elements[1])
  # print(f"    {number_elements} elementos")
  for i in range(number_elements):
    element = random.randint(0, elements_types - 1)
    size = random.randint(1, int(min(room_size) / 2))
    position = positions[random.randint(0, len(positions)-1)]
    # print(f'    Elemento: {element} en posición {position}')
    room.addObject(Room.objects[element], size, position)
  room.list_prompt()
  all_rooms.append(room)

print(len(all_rooms))
for i in range(len(all_rooms)):
    ruta_text_drive = ruta_base + "/room_" + str(i) + ".txt"
    image = all_rooms[i].generateImage()
    print(f'{i + 1}/{len(all_rooms)}')
    cv2.imwrite(f"data/room_{i}.jpg", image)
    with open(ruta_text_drive , "w+", encoding="utf-8") as file:
        file.write("\n".join(all_rooms[i].text))

