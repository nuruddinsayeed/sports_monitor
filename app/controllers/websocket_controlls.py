'''
File: websocket_controlls.py
Project: SportsSafety
File Created: Sunday, 12th June 2022 11:18:20 pm
Author: Syeed (nur.syeed@stud.fra-uas.de, nuruddinsayeed14@gmail.com)
-----
Last Modified: Sunday, 12th June 2022 11:18:22 pm
Modified By: Syeed (nur.syeed@stud.fra-uas.de>)
-----
Copyright 2022 - 2022 This Module Belongs to Open source project
'''


from typing import List

from fastapi import WebSocket


class ConnectionManager:
    """Manges Websockets connections"""
    
    def __init__(self) -> None:
        self.active_connecitons: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connecitons.append(websocket)
        # TODO: accept user and add user to active websocket user list
        
    async def disconnect(self, websocket: WebSocket):
        self.active_connecitons.remove(websocket)
