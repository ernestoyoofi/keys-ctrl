import sys
sys.path.append("./lib")
import websockets
import json
from pynput.mouse import Controller as MouseController, Button as MouseButton
from pynput.keyboard import Controller as KeyboardController
from pynput.keyboard import Key
from lib import generatePin
import asyncio

mouse = MouseController()
keyboard = KeyboardController()
connect_client = None
pin_server = generatePin.generate_pin_token()

def mouse_release(type, postition):
  if type == "press":
    print("Mouse Press On", postition)
    mouse.press(MouseButton[postition.lower()])
  else:
    print("Mouse Release On", postition)
    mouse.release(MouseButton[postition.lower()])

def left_click():
  mouse.click(MouseButton.left)
  print("Left click performed.")

def right_click():
  mouse.click(MouseButton.right)
  print("Right click performed.")

# Function for key actions
def press_key(keys):
  print(keys)
  if isinstance(keys, list):
    for key in keys:
      keyboard.press(key)

    for key in reversed(keys):
      keyboard.release(key)
    
    print(f"Key combination pressed.")
  else:
    keyboard.press(keys)
    keyboard.release(keys)
    print(f"Key {keys} pressed.")

def move_mouse(dx, dy):
  try:
    current_x, current_y = mouse.position
    new_x = current_x + dx
    new_y = current_y + dy
    mouse.position = (new_x, new_y)
    print(f"Mouse moved to ({new_x}, {new_y})")
  except Exception as e:
    print(f"Error moving mouse: {e}")

# Handling WebSocket
print(f'Token: {pin_server}')
async def handle_connection(websocket):
  global connect_client

  print(websocket)

  # path = websocket.path
  # try:
  #   query_parms = dict(item.split("=") for item in path[1:].split("&") if "=" in item)
  # except Exception as e:
  #   await websocket.close(code=4000, reason="Invalid query parameters!")
  #   return

  # pin_token = query_parms.get("pintoken")

  # if not pin_token:
  #   await websocket.close(code=4000, reason="No pintoken!")
  #   return

  # if connect_client is not None:
  #   await websocket.close(code=4001, reason="Server already connected...")
  #   return

  connect_client = websocket
  print(f"Client has connected: {websocket.remote_address}")

  try:
    async for message in websocket:
      try:
        data = json.loads(message)
        action = data.get('action')
        print(f"Received message: {data}")

        if action == 'press_key':
          press_key(data['key'])
        elif action == 'press_sckey':
          press_key(Key[data['key'].lower()])
        elif action == 'press_combination':
          keys = []
          for item in data.get('key', []):
            print(item)
            if item[0] == 'press_sckey': 
              keys.append(Key[item[1].lower()])
            elif item[0] == 'press_key':
              keys.append(item[1])
          press_key(keys)
        elif action == 'mouse_release': 
          mouse_release(data.get("type"), data.get("post"))
        elif action == 'left_click':
          left_click()
        elif action == 'right_click':
          right_click()
        elif action == 'move_mouse':
          details = data.get("details")
          dx = details["dx"]
          dy = details["dy"]
          move_mouse(dx, dy)

      except json.JSONDecodeError:
        await websocket.close(code=4002, reason="Invalid JSON format")
        break

  except websockets.ConnectionClosed:
    print(f"Connection closed: {websocket.remote_address}")
  finally:
    connect_client = None

# Connection
async def main():
  port_server = 8442
  server = await websockets.serve(handle_connection, "192.168.1.4", port_server)

  try:
    print(f'Starting Server: ws://localhost:{port_server}')
    await asyncio.Future()
  except asyncio.CancelledError:
    print("Server Close...")
  finally:
    server.close()
    await server.wait_closed()

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except KeyboardInterrupt:
    print("Server stopped manually.")
