import websockets
import asyncio
import signal
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSocketClient:
    """
    This is a generic web socket client to connect and connect and 
    consume messages from a supplied web socket url
    """
    def __init__(self,url) -> None:
        self.url=url
    
    async def __run(self,request, handler):
        try:
            async with websockets.connect(self.url) as ws:
                    await ws.send(request)
                    while True:
                        message= await ws.recv()
                        logger.info(message)
                        handler.handle(message)
        except websockets.ConnectionClosed:
            logger.error("Web socket connection closed")
             

        
    def run(self, request, handler):
        asyncio.get_event_loop().run_until_complete(self.__run(request, handler))


