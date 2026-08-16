import asyncio
import json
import pyautogui
import websockets

# Configure pyautogui
pyautogui.FAILSAFE = False  # disable mouse going to corner to abort
pyautogui.PAUSE = 0

async def handler(websocket, path):
    print("Client connected")
    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get('type')
            print(f"Received: {msg_type}")

            if msg_type == 'mousemove':
                x = data.get('x', 0)
                y = data.get('y', 0)
                # Move mouse to absolute coordinates (assuming screen size 1920x1080, adjust if needed)
                # Note: pyautogui uses screen coordinates, not video coordinates.
                # You may need to scale based on actual screen size and video size.
                pyautogui.moveTo(x, y, duration=0)

            elif msg_type == 'mousedown':
                button = data.get('button', 0)
                if button == 0:
                    pyautogui.mouseDown(button='left')
                elif button == 2:
                    pyautogui.mouseDown(button='right')
                else:
                    pyautogui.mouseDown(button='middle')

            elif msg_type == 'mouseup':
                button = data.get('button', 0)
                if button == 0:
                    pyautogui.mouseUp(button='left')
                elif button == 2:
                    pyautogui.mouseUp(button='right')
                else:
                    pyautogui.mouseUp(button='middle')

            elif msg_type == 'keydown':
                key = data.get('key', '')
                # Map common keys to pyautogui key names
                key_map = {
                    'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
                    'Enter': 'enter', 'Backspace': 'backspace', 'Tab': 'tab',
                    'Shift': 'shift', 'Control': 'ctrl', 'Alt': 'alt',
                    'Escape': 'esc', ' ': 'space',
                }
                pyautogui.keyDown(key_map.get(key, key))

            elif msg_type == 'keyup':
                key = data.get('key', '')
                key_map = {
                    'ArrowUp': 'up', 'ArrowDown': 'down', 'ArrowLeft': 'left', 'ArrowRight': 'right',
                    'Enter': 'enter', 'Backspace': 'backspace', 'Tab': 'tab',
                    'Shift': 'shift', 'Control': 'ctrl', 'Alt': 'alt',
                    'Escape': 'esc', ' ': 'space',
                }
                pyautogui.keyUp(key_map.get(key, key))

            else:
                print(f"Unknown command: {msg_type}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")

async def main():
    print("Starting input server on ws://localhost:8765")
    async with websockets.serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
