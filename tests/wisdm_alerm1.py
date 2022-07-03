import json
from pathlib import Path
import websockets
import time
import asyncio
import csv


data_file = Path(__file__).resolve().parent / "data" / "wisdm_alerm1.csv"

async def send_to_ws():
    async with websockets.connect('ws://127.0.0.1:8000/ws/running/nuruddinsayeed', ping_interval=None) as websocket:
        
        
        # sitting, jogging, downstairs, walking, standing, disconnected,
        #     abnormal, fall_detected
        
        with open(data_file, 'r') as csv_file:
            data_reader = csv.reader(csv_file)
            next(data_reader)
            for row in data_reader:
                
                user_id, activity_class, x, y, z, activityStatus = row
                json_data = json.dumps(
                {
                    'x':x,
                    'y':y,
                    'z': z,
                    'activity_class': activity_class,
                    'activityStatus': activityStatus
                })
                print("sending rand ", json_data)
                await websocket.send(json_data)
                response = await websocket.recv()
                time.sleep(1)

if __name__ == '__main__':
    asyncio.run(send_to_ws())