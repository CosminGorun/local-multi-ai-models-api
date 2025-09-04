import os

from gpt4all import GPT4All


class CustomModel(object):
    def __init__(self,model_path,model_name):
        self.system_prompt = ""
        model_file = os.path.join(model_path, model_name)
        if not os.path.exists(model_file):
            raise FileNotFoundError(f"Modelul nu există la: {model_file}")
        self.model_path = model_path
        self.model_name = model_name

        self.model = GPT4All(
             model_name,
             model_path=model_path,
             device="gpu"
        )


    def set_system_prompt(self,system_prompt):
        self.system_prompt = system_prompt

    def set_model_path(self,model_path):
        self.model_path = model_path

    def set_model_name(self,model_name):
        self.model_name = model_name

    def generate_response(self,prompt):
        full_prompt = f"{self.system_prompt}\nÎntrebare: {prompt}"
        response = self.model.generate(
            full_prompt,
            max_tokens=300,
            temp=0.7,
            top_k=40,
            top_p=0.9
        )
        return response.strip()

    def __del__(self):
        try:
            self.model.close()
        except AttributeError:
            pass
        del self.model
        del self.system_prompt
        del self.model_path
        del self.model_name
