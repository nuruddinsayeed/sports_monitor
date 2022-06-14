import json
import websockets
import random,time
import asyncio

async def send_to_ws():
    async with websockets.connect('ws://127.0.0.1:8000/ws/walking/nuruddin') as websocket:

        for i in range(30):
            # await websocket.send(json.dumps({'value':random.randint(1,100)}))
            await websocket.send(json.dumps({
                'x':random.randint(1,100)/10,
                'y':random.randint(1,100)/10,
                'z': random.randint(1,100)/10
            }))

            response = await websocket.recv()
            print(response)
            time.sleep(1)
            
            
if __name__ == '__main__':
    asyncio.run(send_to_ws())