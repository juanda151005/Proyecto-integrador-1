import os, json
from openai import OpenAI
from dotenv import load_dotenv
from routes.models import Route 

class recomendacionesIA():
    load_dotenv(".env")
    def __init__(self, request):
        api_key = os.getenv("openai_apikey")
        self.client = OpenAI(api_key=api_key)

    def RecommendCityWithList(self, citylist):
        promt = f"""
        Imagina que eres un asesor de viajes y tienes la tarea de recomendar varias opciones de destino siguiente con base en una lista de ciudades ya decididas por el cliente, las cuales el piensa visitar antes de la ciudad que tu debes recomendar. 
        
        Las ciudades definidadas por el cliente son {citylist}.

        Aparte debes crear una breve descripcion en la cual le vas a decir al usuario que sitios turisticos puede visitar en las ciudades recomendadas.
        
        Asegurate que la respuesta la des en un formato json de la siguiente forma:
        'cities': [city1, city2, ...],
        'description':[description_city1, description_city2, ...]
        """

        msg = [
            {"role": "user", "content": promt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=msg,
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        return json.loads(response.choices[0].message.content) # Returns JSON formmated response.
    
    def CreateRouteWithOriginCity(self, origincity, time):
        promt = f"""
        Imagina que eres un asesor de viajes y tienes la tarea de crear una ruta de viaje para un cliente solo teniendo la informacion sobre la ciudad desde donde se desea empezar la ruta y el tiempo que tiene disponible para viajar. 
        
        La ciudad de origen definida por el cliente es {origincity} y el tiempo que tiene disponible es {time}.

        Aparte de esto tambien crea una descripcion de que hacer y que visitar en cada ciudad de la ruta y el tiempo estimado que puede estar alli.

        La primer ciudad de la ruta debe ser la dicha por el cliente. 

        Asegurate que la respuesta la des en un formato json de la siguiente forma:
        'cities': [city1, city2, ...],
        'description': [description_city1 'con el tiempo', description_city2 'con el tiempo', ...]
        """

        msg = [
            {"role": "user", "content": promt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=msg,
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        return json.loads(response.choices[0].message.content) # Returns JSON formmated response.
    
    def RecommendCityWithDescription(self, description):
        promt = f"""
        Imagina que eres un asesor de viajes y tienes la tarea de recomendar varias opciones de destino a un cliente que te da una descripcion general del lugar que desea visitar. 
        
        La descripcion que te da el cliente es la siguiente {description}.

        Aparte de esto tambien crea una descripcion de que hacer y que visitar en cada ciudad que recomiendes.

        Asegurate que la respuesta la des en un formato json de la siguiente forma:
        'cities': [city1, city2, ...],
        'description':[description_city1, description_city2, ...]
        """

        msg = [
            {"role": "user", "content": promt}
        ]
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=msg,
            response_format={"type": "json_object"},
            max_tokens=2000
        )
        return json.loads(response.choices[0].message.content) # Returns JSON formmated response.