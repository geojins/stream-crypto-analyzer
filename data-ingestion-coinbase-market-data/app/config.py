from os import environ as env
from dotenv import load_dotenv

load_dotenv()


class Config():
    KAFKA_BROKERS: str = "localhost:9094"
    COINBASE_WEB_SOCKET_URL: str ='wss://ws-feed.exchange.coinbase.com'
    TOPIC_COINBASE_MESSAGE_TYPE_TICKER='crypto.coinbase.ticker'
    TOPIC_COINBASE_MESSAGE_TYPE_HEARTBEAT='crypto.coinbase.heartbeat'
    
    
    def __init__(self,env) -> None:
        keys =  self.__dict__.keys()
        for key in keys:
            val = env.get(key)
            if val is None and self.__getattribute__(key) is None:
                raise ValueError(f"{key} environment variable missing")
            self.__setattr__(key, val)
    
    def __repr__(self) -> str:
        return str(self.__dict__)
