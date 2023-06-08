from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from typing import List

from WebSockGoita import GoitaRoom, Player

class WebSockManager:
    def __init__(self, room_num):
        self.connections: List[WebSocket] = []
        self.room_num = room_num
        self.room_connections = [[] for _ in range(room_num)]

    def connect(self, websock: WebSocket):
        self.connections.append(websock)

    def enter_room(self, room: int, websock: WebSocket):
        if not (0 <= room < self.room_num):
            raise ValueError("Invalid room num")
        self.room_connections[room].append(websock)

    def broadcast_all_json(self, json: dict):
        for connection in self.connections:
            connection.send_json(json)

    def broadcast_room_json(self, room: int, json: dict):



def start_api(rooms_num=10):
    app = FastAPI()

    rooms = [GoitaRoom() for _ in range(rooms_num)]

    @app.get("/rooms")
    def get_rooms():
        return rooms_num

    @app.websocket("/play/{room_number}")
    async def playing(websock: WebSocket, room_number: int, name: str):

        await websock.accept()

        if not (0 <=  room_number <= rooms_num):
            await websock.close(code=4000, reason="invalid room number")
            return

        player = Player(name, websock.headers["sec-websocket-key"])
        is_seated = False
        seat_num = -1

        try:
            while True:
                data = await websock.receive_json()

                if data["type"] == "sit":
                    try:
                        rooms[room_number].seat(data["seat_num"], player)
                        is_seated = True
                        seat_num = data["seat_num"]

                        await websock.({
                            "type": "message",

                        })

                    except ValueError:
                        await websock.send_json({
                            "type": "error",
                            "code": 4001,
                            "reason": "invalid seat num"
                        })

                if data["type"] == "leave":
                    try:
                        rooms[room_number].unseat(data["seat_num"], player)
                        is_seated = False
                        seat_num = -1
                    except ValueError:
                        await websock.send_json({
                            "type": "error",
                            "code": 4001,
                            "reason": "invalid seat num"
                        })

                if data["type"] == "ready":
                    try:
                        rooms[room_number].ready(player)
                    except ValueError:
                        await websock.send_json({
                            "type": "error",
                            "code": 4002,
                            "reason": "invalid "
                        })


        except WebSocketDisconnect:
            if is_seated:
                rooms[room_number].unseat(seat_num, player)
            await websock.close()




