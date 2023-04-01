import threading
import logging
import logging.config
import yaml
from sen0386 import Sen0386

"""
Constants
"""
LOGGER = "main"
SEN0386_SERIALNO = "AB0O5A7Z"

"""
Current sensor values
"""
sen038SensorValues = None

"""
Setup logging    
"""
with open(file = 'logging.yaml', mode = 'r') as stream:
    config = yaml.load(stream = stream, Loader = yaml.FullLoader)
    logging.config.dictConfig(config)
    
logger = logging.getLogger(LOGGER)

"""
Setting up modules
"""
logger.info("Starting setup")
sen0386 = Sen0386(serialno = SEN0386_SERIALNO)
logger.info("Sen0386 setup")

"""
Thread module setup
"""
def sen038Thread():
    logger.info("Starting sen038Thread")  
    while True:
        sen038SensorValues = sen0386.readSensorValues()
        print(sen038SensorValues)

logger.info("Starting thread setup")        
sen0386Thread = threading.Thread(target = sen038Thread)
sen0386Thread.start()
logger.info("Completed Sen0386 setup")
