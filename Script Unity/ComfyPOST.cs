using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

public class ComfyPOST : MonoBehaviour {
    public string apiUrl = "http://127.0.0.1:5000/test-api";
    public string prompt = "TFGPabloMap map of a square room with a small table at center";
    // public GameObject plane;
    public GameObject chairPrefab;
    public GameObject doorPrefab;
    public GameObject tablePrefab;
    public float scale = 1f;
    public float scaleFactor = 50f;
    public float roomHeight = 512f;
    public float roomWidth = 512f;

    // Define la clase que representa la estructura del JSON
    public class RoomData {
        public List<ChairData> chairs;
        public List<DoorData> doors;
        public List<TableData> tables;
    }

    public class ChairData {
        public float x;
        public float y;
        public float h;
        public float w;
        public float centroid_x;
        public float centroid_y;
    }

    public class DoorData {
        public float x;
        public float y;
        public float h;
        public float w;
        public float centroid_x;
        public float centroid_y;
    }

    public class TableData
    {
        public float x;
        public float y;
        public float h;
        public float w;
        public float centroid_x;
        public float centroid_y;
    }


    // // Start is called before the first frame update
    void Start()
    {
        string json = "{\"prompt\": \"" + prompt + "\"}";
        StartCoroutine(Upload(json));
    }

    IEnumerator Upload(string json)
    {
        using (UnityWebRequest www = UnityWebRequest.Post(apiUrl, json, "application/json"))
        {
            Debug.Log("Sent POST request");
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else {
                // Si se ha obtenido un resultado correcto
                Debug.Log("Received POST data");
                byte[] bytes_data = www.downloadHandler.data;
                string jsonString = System.Text.Encoding.UTF8.GetString(bytes_data);
                Debug.Log("ALL DATA:\n\n" + jsonString);
                RoomData data = JsonConvert.DeserializeObject<RoomData>(jsonString);
                foreach (var chair in data.chairs) {
                    Debug.Log("Silla encontrada. \nPropiedades:\nx: " + chair.x + "\ny: " + chair.y);
                    chair.x /= scaleFactor;
                    chair.y /= scaleFactor;
                    chair.w /= scaleFactor;
                    chair.h /= scaleFactor;
                    // Calcula la posición del centro del rectángulo
                    Vector3 position = new Vector3(chair.x + (chair.w / 2), chair.w * scale / 2, -(chair.y + (chair.h / 2)));
                    // Instancia el prefab en la posición calculada
                    GameObject instance = Instantiate(chairPrefab, position, Quaternion.identity);
                    // Escala el prefab según las dimensiones del rectángulo
                    instance.transform.localScale = new Vector3(chair.w * scale,  chair.w * scale, chair.h * scale);
                }
                foreach (var door in data.doors) {
                    Debug.Log("Puerta encontrada. \nPropiedades:\nx: " + door.x + "\ny: " + door.y + "\nw: " + door.w + "\nh: " + door.h);
                    door.x /= scaleFactor;
                    door.y /= scaleFactor;
                    door.w /= scaleFactor;
                    door.h /= scaleFactor;
                    Vector3 position = new Vector3(door.x + (door.w / 2), door.w * scale / 2, -(door.y + (door.h / 2)));
                    GameObject instance = Instantiate(doorPrefab, position, Quaternion.identity);
                    instance.transform.localScale = new Vector3(door.w * scale, door.w * scale, door.h * scale);
                    // Se calcula la rotacion
                    if (door.x == 0.0f) {
                        instance.transform.Rotate(0.0f, 90f, 0f);
                    } else {
                        if (door.y == 0.0f) {
                            // Medio sup
                            instance.transform.Rotate(0.0f, 180f, 0f);
                        } else if (Mathf.Approximately(door.y + door.h, roomHeight / scaleFactor)) {
                            // Medio inf - Orientacion por defecto
                        } else {
                            if (Mathf.Approximately(door.x + door.w, roomWidth / scaleFactor)) {
                                // Mitad derecha
                                instance.transform.Rotate(0.0f, -90f, 0.0f);
                            } else {
                                // Mitad
                                Debug.Log("Posicion imposible\nDatos:\n  x+w " + (door.x + door.w) + "\n  roomHeight " + (roomWidth / scaleFactor));
                                instance.transform.Rotate(90.0f, 0f, 0f, Space.Self);
                            }
                        }
                    }

                }

                foreach (var table in data.tables) {
                    Debug.Log("Mesa encontrada. \nPropiedades:\nx: " + table.x + "\ny: " + table.y);
                    table.x /= scaleFactor;
                    table.y /= scaleFactor;
                    table.w /= scaleFactor;
                    table.h /= scaleFactor;
                    Vector3 position = new Vector3(table.x + (table.w / 2), table.w * scale / 2, -(table.y + (table.h / 2)));
                    GameObject instance = Instantiate(tablePrefab, position, Quaternion.identity);
                    instance.transform.localScale = new Vector3(table.w * scale, table.w * scale, table.h * scale);
                }
            }
        }
    }
}
