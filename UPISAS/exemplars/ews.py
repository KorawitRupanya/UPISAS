import pprint, time
from UPISAS.exemplar import Exemplar
import logging
pp = pprint.PrettyPrinter(indent=4)
logging.getLogger().setLevel(logging.INFO)

class EWS(Exemplar):
    """
    A class which encapsulates a self-adaptive exemplar run in a docker container.
    """
    def __init__(self, auto_start: "Whether to immediately start the container after creation" =False):
        my_docker_kwargs = {
            "name": "ews-wrapper-server-testing", # Testing container name
            "image": "ews-wrapper-server", # Image name
            "ports" : {5000: 5001}} # Map container port 5000 to host port 5001

        super().__init__("http://localhost:5001", my_docker_kwargs, auto_start)
    
    def start_run(self):
       self.exemplar_container.exec_run(cmd = 'flask run', detach=True)
