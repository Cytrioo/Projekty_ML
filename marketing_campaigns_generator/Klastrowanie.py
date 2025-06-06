import json
from pycaret.clustering import setup, create_model, plot_model, predict_model

def klastrowanie(data, ile_grup):
    setup(data=data)
    model = create_model("kmeans", num_clusters=ile_grup)
    return model

def wizualizacja(model):
    vis = plot_model(model, plot='cluster', display_format="streamlit")
    return vis

def send_clu(model_c, df, cel, MODEL_GPT, openaikey):
    mkmeans = predict_model(model_c, df)
    Opis_klastra = {}
    for k_id in mkmeans['Cluster'].unique():
        klaster_df = mkmeans[mkmeans['Cluster'] == k_id]
        summary = ""
        for column in mkmeans:
            if column == 'Cluster':
                continue

            value_counts = klaster_df[column].value_counts()
            value_counts_str = ', '.join([f"{idx}: {cnt}" for idx, cnt in value_counts.items()])
            summary += f"{column} - {value_counts_str}\n"

        Opis_klastra[k_id] = summary
    
    prompt = "Użyłem algorytmu klastrowania."
    for k_id, opis in Opis_klastra.items():
        prompt += f"\n\nKlaster {k_id}:\n{opis}"

    prompt += """
    Wygeneruj najlepsze nazwy dla każdego z klastrów oraz najlepszą treść reklamowa dla danego klastra. Wykorzystaj mój cel reklamowy do wygenerowania reklamy.
    Celem kampanii reklamowej jest """
    
    prompt += cel

    prompt += """
    
    . Użyj formatu JSON. Przykładowo:
    {
        "Cluster 0": {
            "nazwa": "Klaster 0",
            "reklama": "W tym klastrze proponuje...."
        },
        "Cluster 1": {
            "nazwa": "Klaster 1",
            "reklama": "W tym klastrze proponuje...."
        }
    }
    """
    response = openaikey.chat.completions.create(
        model=MODEL_GPT,
        temperature=0,
        messages=[
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    )
    result = response.choices[0].message.content.replace("```json", "").replace("```", "").strip()
    Nazwy = json.loads(result)
    return Nazwy