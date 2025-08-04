from os import environ as env
from dotenv import load_dotenv

load_dotenv()


class Config:
    KAFKA_BROKERS: str = "localhost:9094"
    COINBASE_WEB_SOCKET_URL: str = "wss://ws-feed.exchange.coinbase.com"
    TOPIC_COINBASE_MESSAGE_TYPE_TICKER = "crypto.coinbase.ticker"
    TOPIC_COINBASE_MESSAGE_TYPE_HEARTBEAT = "crypto.coinbase.heartbeat"

    def __init__(self, env=env) -> None:
        keys = [k for k in self.__class__.__dict__.keys() if k.isupper()]
        for key in keys:
            val = env.get(key)
            if val is None:
                val = getattr(self.__class__, key)
                if val is None:
                    raise ValueError(f"{key} environment variable missing")
            setattr(self, key, val)
    
    def __repr__(self) -> str:
        return str(self.__dict__)
