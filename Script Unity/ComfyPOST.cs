using Newtonsoft.Json;
using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;

public class ComfyPOST : MonoBehaviour {
    public string apiUrl = "http://127.0.0.1:5000/test-api";
    public string prompt = "TFGPabloMap map of a square room with a small table at center";
    public GameObject plane;
    public GameObject chairPrefab;
    public GameObject doorPrefab;
    public GameObject tablePrefab;
    public float scale = 1f;
    public float scaleFactor = 10f;

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
                    Vector3 position = new Vector3(chair.x + (chair.w / 2), 0f, chair.y + (chair.h / 2));
                    // Instancia el prefab en la posición calculada
                    GameObject instance = Instantiate(chairPrefab, position, Quaternion.identity);
                    // Escala el prefab según las dimensiones del rectángulo
                    instance.transform.localScale = new Vector3(chair.w * scale,  1f, chair.h * scale);
                }
                foreach (var door in data.doors) {
                    Debug.Log("Puerta encontrada. \nPropiedades:\nx: " + door.x + "\ny: " + door.y);
                    door.x /= scaleFactor;
                    door.y /= scaleFactor;
                    door.w /= scaleFactor;
                    door.h /= scaleFactor;
                    Vector3 position = new Vector3(door.x + (door.w / 2), 0f, door.y + (door.h / 2));
                    GameObject instance = Instantiate(doorPrefab, position, Quaternion.identity);
                    instance.transform.localScale = new Vector3(door.w * scale, 1f, door.h * scale);
                }

                foreach (var table in data.tables) {
                    Debug.Log("Mesa encontrada. \nPropiedades:\nx: " + table.x + "\ny: " + table.y);
                    table.x /= scaleFactor;
                    table.y /= scaleFactor;
                    table.w /= scaleFactor;
                    table.h /= scaleFactor;
                    Vector3 position = new Vector3(table.x + (table.w / 2), 0f, table.y + (table.h / 2));
                    GameObject instance = Instantiate(tablePrefab, position, Quaternion.identity);
                    instance.transform.localScale = new Vector3(table.w * scale,  1f, table.h * scale);
                }
            }
        }
    }
}
