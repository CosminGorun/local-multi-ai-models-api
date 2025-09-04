Local Multi AI Models API

How to run:
Run the runner.py script. This will use the command:
uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
and start a server on port 8000.

The API uses FastAPI. Work in progress.

Currently, there are 3 main classes:

custom_model
This class imports and uses a pre-installed model from Hugging Face.
It can be used with the following endpoints:

POST:
initModel – loads the model into memory.
delModel – frees the model from memory.

GET:
getResponse – returns a string with the model's answer.

generator3D
Generates a 3D object from text or image, using Shap-E.

openrouter_deepseek
Calls the DeepSeek free model using OpenRouter.

I am still working on and updating this project, so the code may change, but the README may refer to an older version.

Dependencies are listed in the file requirements.txt.
