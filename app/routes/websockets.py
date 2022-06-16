'''
File: websockets.py
Project: SportsSafety
File Created: Sunday, 12th June 2022 1:19:46 am
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Sunday, 12th June 2022 1:19:50 am
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''

import json
import logging
import random
import time
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketState

from app.controllers.websocket_controlls import ConnectionManager
from app.Activity import activity_processor


SPM_LOGGER = logging.getLogger("spm_logger")
router = APIRouter()
websocket_manager = ConnectionManager()


@router.websocket("/{ativity_type}/{username}")
async def running_ws(websocket: WebSocket, ativity_type:str, username: str):
    
    # TODO: verify user before connect
    await websocket_manager.connect_user(websocket=websocket)
    
    try:
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                
                activity_processor.process_activity(username=username,
                                                    activity_type=ativity_type,
                                                    data=data)
                
                await websocket_manager.brodcust_to_monitor(message=data)
                
                await websocket.send_text(f"activity: ({ativity_type}) name: ({username})")
            else:
                SPM_LOGGER.warning(f"Websocket disconnected for user {username}\
                    Trying to reconnect...")
                # await websocket_manager.connect(websocket=websocket)
                await websocket_manager.connect_user(websocket=websocket)
                
    except WebSocketDisconnect:
        # await websocket_manager.connect_user(websocket=websocket)
        # await websocket_manager.disconnect(websocket=websocket,
        #                                    username=username)
        print("Websocket Disconnected.............................")
        
@router.websocket("/monitor/{ativity_type}/{username}")
async def running_ws(websocket: WebSocket, ativity_type:str, username: str):
    
    # TODO: verify user before connect
    await websocket_manager.connect_moinitor(websocket=websocket)
    
    try:
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                # data = await websocket.receive_text()
                
                # activity_processor.process_activity(username=username,
                #                                     activity_type=ativity_type,
                #                                     data=data)
                
                # await websocket.send_text(f"activity: ({ativity_type}) name: ({username})")
                
                data = await websocket.receive_text()
                
                if "value" in str(data):
                    await websocket.send_text(data)
                
                
                # user_socket = websocket_manager.get_acive_socket(
                #     username=username)
                # print(f"=========================> {websocket_manager.active_users}")
                # if user_socket:
                #     user_data = await user_socket.receive_text()
                #     await websocket.send_text(user_data)
                #     # data = await websocket.receive_text()
                # else:
                #     raise Exception("no connection found")
                #     for i in range(10):
                #         time.sleep(1)
                #         continue
                #         dup = json.dumps(
                #         {'value': {
                #             'x':random.randint(1,100)/10,
                #             'y':random.randint(1,100)/10,
                #             'z': random.randint(1,100)/10
                #             }
                #         })
                #         print("sending rand ", dup)
                        
                #         await websocket.send_text(dup)
                #         data = await websocket.receive_text()
                        
                # for i in range(10):
                #     dup = json.dumps(
                #     {'value': {
                #         'x':random.randint(1,100)/10,
                #         'y':random.randint(1,100)/10,
                #         'z': random.randint(1,100)/10
                #         }
                #     })
                #     print("sending rand ", dup)
                    
                #     await websocket.send_text(dup)
                #     data = await websocket.receive_text()
            # else:
            #     SPM_LOGGER.warning(f"Websocket disconnected for user {username}\
            #         Trying to reconnect...")
            #     await websocket_manager.connect(websocket=websocket)
                
    except WebSocketDisconnect:
        await websocket_manager.disconnect_monitor(websocket=websocket)
        print("Websocket Disconnected.......")
            
            
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://127.0.0.1:8000/ws/running/syeed");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
async def get():
    return HTMLResponse(html)