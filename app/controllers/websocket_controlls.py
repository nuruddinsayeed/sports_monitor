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


from typing import Dict
from fastapi import WebSocket

from app.helpers.excepitons import AlreadlyConnected


class ConnectionManager:
    """Manges Websockets connections"""
    
    def __init__(self) -> None:
        # self.active_monitors: List[WebSocket] = []
        self.user_monitor: Dict[str, WebSocket] = {}
        
    async def connect_user(self, websocket: WebSocket) -> None:
        await websocket.accept()
    
    async def connect_moinitor(self, websocket: WebSocket, username: str):
        await websocket.accept()
        if self.user_monitor.get(username, None):
            raise AlreadlyConnected("A monitor is already Monitoring this user")
        self.user_monitor[username] = websocket
    
    async def brodcust_to_monitor(self, message: str, username: str):
        # for connection in self.active_monitors:
        #     await connection.send_text(message)
        monitor_socket = self.user_monitor.get(username, None)
        if monitor_socket:
            await monitor_socket.send_text(data=message)
        
    async def disconnect_monitor(self, websocket: WebSocket, username: str):
        self.user_monitor.pop(username, None)

