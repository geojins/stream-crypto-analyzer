from websocketclient import WebSocketClient
from messagehandler import CryptoMessageHandler
import json
from config import Config

req={
    "type": "subscribe",
    "product_ids": [
        "ETH-USD",
        "ETH-EUR"
    ],
    "channels": [
        "level2",
        "heartbeat",
        { "name": "full"},
        {
            "name": "ticker",
            "product_ids": [
                "ETH-BTC",
                "ETH-USD"
            ]
        }
    ]
}
def main():
    client = WebSocketClient(Config.COINBASE_WEB_SOCKET_URL)
    handler = CryptoMessageHandler()
    client.run(json.dumps(req), handler)

if __name__ == '__main__':
     main()