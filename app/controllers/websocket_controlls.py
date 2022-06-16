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


from ctypes import c_char_p
from typing import List
from fastapi import WebSocket


class ConnectionManager:
    """Manges Websockets connections"""
    
    def __init__(self) -> None:
        self.active_monitors: List[WebSocket] = []
        
    async def connect_user(self, websocket: WebSocket) -> None:
        await websocket.accept()
    
    async def connect_moinitor(self, websocket: WebSocket):
        await websocket.accept()
        self.active_monitors.append(websocket)
    
    async def brodcust_to_monitor(self, message: str):
        for connection in self.active_monitors:
            await connection.send_text(message)
        
    async def disconnect_monitor(self, websocket: WebSocket):
        self.active_monitors.remove(websocket)

