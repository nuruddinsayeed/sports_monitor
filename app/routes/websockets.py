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

from fastapi import WebSocket, APIRouter
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketState

from app.controllers.websocket_controlls import ConnectionManager

router = APIRouter()
websocket_manager = ConnectionManager()

@router.websocket("/{ativity_type}/{username}")
async def running_ws(websocket: WebSocket, ativity_type:str, username: str):
    
    # TODO: verify user before connect
    await websocket_manager.connect(websocket=websocket)
    
    while True:
        if websocket.application_state == WebSocketState.CONNECTED:
            data = await websocket.receive_text()
            print(data)
            
            await websocket.send_text(f"activity: ({ativity_type}) name: ({username})")
            
            
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