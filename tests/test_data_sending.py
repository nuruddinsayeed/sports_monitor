import json
import websockets
import random,time
import asyncio

async def send_to_ws():
    async with websockets.connect('ws://127.0.0.1:8000/ws/running/sayed', ping_interval=None) as websocket:
        
        
        # sitting, jogging, downstairs, walking, standing, disconnected,
        #     abnormal, fall_detected
        for i in range(120):
            dup = json.dumps(
            {
                'x':random.randint(1,100)/10,
                'y':random.randint(1,100)/10,
                'z': random.randint(1,100)/10,
                'activity_class': 'standing',
                'activityStatus': 'normalActivity'
            })
            print("sending rand ", dup)
            
            await websocket.send(dup)
            
            response = await websocket.recv()
            # print(response)
            time.sleep(1)

        # for i in range(3):
        #     # await websocket.send(json.dumps({'value':random.randint(1,100)}))
        #     await websocket.send(json.dumps({
        #         'x':random.randint(1,100)/10,
        #         'y':random.randint(1,100)/10,
        #         'z': random.randint(1,100)/10
        #     }))

        #     response = await websocket.recv()
        #     print(response)
        #     time.sleep(1)
            
            
if __name__ == '__main__':
    asyncio.run(send_to_ws())