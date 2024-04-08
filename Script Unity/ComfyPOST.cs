using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class ComfyPOST : MonoBehaviour

{
    public string apiUrl = " http://127.0.0.1:5000/test";
    public string prompt = "A girl flying";

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
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success)
            {
                Debug.LogError(www.error);
            }
            else
            {
                Debug.Log("Form upload complete!");
            }
        }
    }

    // Función para aplicar la textura al plano
    void ApplyTexture(byte[] imageData)
    {
        // Crear una textura a partir de los bytes de la imagen
        Texture2D texture = new Texture2D(2, 2);
        texture.LoadImage(imageData);

        // Obtener el plano al que se aplicará la textura
        MeshRenderer meshRenderer = GetComponent<MeshRenderer>();

        // Aplicar la textura al material del plano
        meshRenderer.material.mainTexture = texture;
    }

}
