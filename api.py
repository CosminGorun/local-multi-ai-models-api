from http.client import HTTPException

from fastapi import FastAPI
from private_keys import PATH_TO_MODELS_DIR
from components.custom_model import CustomModel

app = FastAPI()
model:CustomModel=None
@app.get("/")
def home():
    return {"message": "Hello from FastAPI"}

@app.post("/initModel")
def initModel():
    global model
    model_name = "Hermes-2-Pro-Mistral-7B.Q4_0.gguf"
    try:
        model = CustomModel(PATH_TO_MODELS_DIR, model_name)
        return {"status": "Model "+model_name+" loaded successfully"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Model not found")


@app.post("/delModel")
def del_model():
    global model
    if model is None:
        return {"status": "Model not initialized"}
    del model
    model = None
    return {"status": "Model deleted successfully"}

@app.get("/getResponse")
def getResponse(user_prompt:str):
    global model
    if model is None:
        return {"status": "Model not initialized"}
    response=model.generate_response(user_prompt)
    return {"response": response}

