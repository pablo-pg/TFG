using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class ComfyPOST : MonoBehaviour

{
    public string apiUrl = "http://127.0.0.1:5000/test-api";
    public string prompt = "TFGPabloMap map of a square room with a small table at center";
    public GameObject plane;

    public delegate void OnDataGot();
    public OnDataGot RoomWithTexture;

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
                byte[] image = www.downloadHandler.data;

                // Crear una textura desde la imagen obtenida
                Texture2D texture = new Texture2D(1, 1);
                texture.LoadImage(image);

                // Asignar la textura al material del plano
                Material planeMaterial = plane.GetComponent<Renderer>().material;
                planeMaterial.mainTexture = texture;
                // Se llama al notificador cuando se ha terminado el proceso
                RoomWithTexture();
            }
        }
    }
}
