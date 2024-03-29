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

import logging
from fastapi import WebSocket, APIRouter, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from starlette.websockets import WebSocketState

from app.controllers.websocket_controlls import ConnectionManager
from app.Activity import activity_processor


SPM_LOGGER = logging.getLogger("spm_logger")
router = APIRouter()
websocket_manager = ConnectionManager()


@router.websocket("/{ativity_type}/{username}")
async def user_activity_ws(websocket: WebSocket, ativity_type:str, username: str):
    
    # TODO: verify user before connect
    await websocket_manager.connect_user(websocket=websocket,
                                         username=username,
                                         activity_type = ativity_type)
    try:
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                data = await websocket.receive_text()
                
                processed_activity = activity_processor.process_activity(
                    username=username,activity_type=ativity_type,data=data
                )
                
                await websocket_manager.brodcust_to_monitor(
                    message=processed_activity, username=username)
                
                await websocket.send_text(f"activity: ({ativity_type}) name: ({username})")
            else:
                SPM_LOGGER.warning(f"Websocket disconnected for user {username}\
                    Trying to reconnect...")
                # await websocket_manager.connect(websocket=websocket)
                await websocket_manager.connect_user(websocket=websocket,
                                                     username=username)
                
    except WebSocketDisconnect:
        # await websocket_manager.connect_user(websocket=websocket)
        # await websocket_manager.disconnect(websocket=websocket,
        #                                    username=username)
        await websocket_manager.disconnect_user(username=username,
                                                activity_type = ativity_type)
        print("Websocket Disconnected....")
        
@router.websocket("/monitor/user/{username}")
async def monitor_ws(websocket: WebSocket, username: str):
    
    # TODO: verify user before connect
    await websocket_manager.connect_moinitor(websocket=websocket,
                                             username=username)
    
    try:
        while True:
            if websocket.application_state == WebSocketState.CONNECTED:
                
                data = await websocket.receive_text()
                print(f'user sayes {data}')
            else:
                SPM_LOGGER.warning(f"Websocket disconnected for Monior\
                    Trying to reconnect...")
                await websocket_manager.connect_moinitor(websocket=websocket,
                                             username=username)
                   
    except WebSocketDisconnect:
        await websocket_manager.disconnect_monitor(websocket=websocket,
                                                   username=username)
        print("Websocket Disconnected.......")