import pprint, time
from UPISAS.exemplar import Exemplar
import logging
pp = pprint.PrettyPrinter(indent=4)
logging.getLogger().setLevel(logging.INFO)

# TODO add actual exemplar name
class YourExemplar(Exemplar):
    """
    A class which encapsulates a self-adaptive exemplar run in a docker container.
    """
    _container_name = ""
    def __init__(self, auto_start: "Whether to immediately start the container after creation" =False, container_name = "fas-api-test"):
        my_docker_kwargs = {
            "name": container_name,    # TODO add your container name
            "image": "fas-api", # TODO add your exemplar's image name
            "ports" : {5000: 5001}} # TODO add any other necessary ports

        super().__init__("http://localhost:5001", my_docker_kwargs, auto_start)
    
    def start_run(self):
       self.exemplar_container.exec_run(cmd = 'flask run', detach=True)
