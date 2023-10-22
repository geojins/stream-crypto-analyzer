from config import Config
from kafka import KafkaProducer
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CryptoMessageHandler:
    '''
    Handler class for Coinbase crypto market data messages. The handler 
    publishes the message to a kafka topic.
    '''
    def __init__(self) -> None:
        self.producer = KafkaProducer(bootstrap_servers=[Config.KAFKA_BROKERS],
                                       value_serializer=self.__serialize)

    def __serialize(self, msg):
        return json.dumps(msg).encode('utf-8')

    def handle(self, message: str):
        try:
            msg =  json.loads(message)
            type = msg.get('type')
            if type is not None and type.lower() == 'ticker':
                self.producer.send(Config.TOPIC_COINBASE_MESSAGE_TYPE_TICKER, msg)
            elif type is not None and type.lower() == 'heartbeat':    
                self.producer.send(Config.TOPIC_COINBASE_MESSAGE_TYPE_HEARTBEAT,msg)
            else:
                #raise ValueError()
                logger.warning(f"Unexpected message type detected {type}")
        except Exception as e:
            logger.warn(f"Error handling message : {message}", exc_info=e)
            

