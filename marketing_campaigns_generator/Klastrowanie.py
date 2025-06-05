from pycaret.clustering import setup, create_model, plot_model

def klastrowanie(data, ile_grup):
    setup(data=data)
    model = create_model("kmeans", num_clusters=ile_grup)
    return model

def wizualizacja(model):
    vis = plot_model(model, plot='cluster', display_format="streamlit")
    return vis