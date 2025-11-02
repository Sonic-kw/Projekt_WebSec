"""
Chat routes: message history and WebSocket real-time chat
"""
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from typing import List
from jose import JWTError, jwt

from schemas.models import User, ChatMessage
from schemas.schemas import ChatMessageResponse
from handlers.auth import get_current_active_user
from handlers.websocket import manager
from config import SECRET_KEY, ALGORITHM

router = APIRouter()

@router.get("/chat/history", response_model=List[ChatMessageResponse])
async def get_chat_history(
    limit: int = 50,
    current_user: User = Depends(get_current_active_user)
):
    """Get chat message history"""
    messages = await ChatMessage.find_all().sort(-ChatMessage.timestamp).limit(limit).to_list()
    messages.reverse()  # Return in chronological order
    return [
        ChatMessageResponse(
            username=msg.username,
            message=msg.message,
            timestamp=msg.timestamp
        )
        for msg in messages
    ]

@router.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time chat"""
    await manager.connect(websocket)
    
    # Authenticate user
    try:
        token = await websocket.receive_text()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                await websocket.close(code=1008)
                return
            
            user = await User.find_one(User.username == username)
            if user is None or not user.is_active:
                await websocket.close(code=1008)
                return
        except JWTError:
            await websocket.close(code=1008)
            return
        
        # Send welcome message
        await websocket.send_json({
            "type": "system",
            "message": f"Welcome {username}! You are now connected to the chat."
        })
        
        # Send recent chat history (last 50 messages)
        recent_messages = await ChatMessage.find_all().sort(-ChatMessage.timestamp).limit(50).to_list()
        recent_messages.reverse()  # Chronological order
        
        if recent_messages:
            await websocket.send_json({
                "type": "history",
                "messages": [
                    {
                        "username": msg.username,
                        "message": msg.message,
                        "timestamp": msg.timestamp.isoformat()
                    }
                    for msg in recent_messages
                ]
            })
        
        # Handle messages
        while True:
            data = await websocket.receive_text()
            
            # Check for special commands
            if data.startswith("/"):
                command_parts = data.split(maxsplit=1)
                command = command_parts[0].lower()
                
                if command == "/history":
                    # Get custom number of messages
                    limit = 50
                    if len(command_parts) > 1 and command_parts[1].isdigit():
                        limit = int(command_parts[1])
                        limit = min(limit, 200)  # Max 200 messages
                    
                    history_messages = await ChatMessage.find_all().sort(-ChatMessage.timestamp).limit(limit).to_list()
                    history_messages.reverse()
                    
                    await websocket.send_json({
                        "type": "history",
                        "messages": [
                            {
                                "username": msg.username,
                                "message": msg.message,
                                "timestamp": msg.timestamp.isoformat()
                            }
                            for msg in history_messages
                        ]
                    })
                    continue
                
                elif command == "/help":
                    await websocket.send_json({
                        "type": "system",
                        "message": "Available commands:\n/history [number] - Get recent messages (default 50, max 200)\n/help - Show this help message"
                    })
                    continue
            
            # Regular message - save and broadcast
            chat_message = ChatMessage(username=username, message=data)
            await chat_message.insert()
            
            # Broadcast to all connected clients
            message_data = {
                "type": "message",
                "username": username,
                "message": data,
                "timestamp": chat_message.timestamp.isoformat()
            }
            await manager.broadcast(message_data)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WebSocket error: {e}")