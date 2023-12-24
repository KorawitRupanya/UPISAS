Group: 2_3_Emergent Web Server_NU-5B51-Collaborative_Jorit-Rishikesh



# UPISAS
Unified Python interface for self-adaptive system exemplars.

### Prerequisites 
Tested with Python 3.9.12

### Installation
In a terminal, navigate to the parent folder of the project and issue:
```
pip install -r requirements.txt

```

### Run

Firstly to run the solution you need to have EWS docker image readily available and ews container running to use by our wrapper server and also the wrapper server docker image should be available. You can build the wrapper server image using our wrapper server project [here] (https://github.com/KorawitRupanya/EWS-wrapper-server)

Run any client from EWS Exemplar and then try the following:

In a terminal, navigate to the parent folder of the project and issue:
```
python3 run.py
```

### Run unit tests
In a terminal, navigate to the parent folder of the project and issue:
```
python -m UPISAS.tests.upisas.test_exemplar
python -m UPISAS.tests.upisas.test_strategy
python -m UPISAS.tests.swim.test_swim_interface

This is how to run test for EWS interface
python -m UPISAS.tests.ews.test_ews_interface
```

