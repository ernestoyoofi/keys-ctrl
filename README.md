 # Keys Control

> [!WARNING]  
> Page has been archived, if you want to fork please but not used for bad things

> [!CAUTION]  
> This script is not used for any place, so make sure this is not done for bad things or harming someone, I as the one who has this repository is not responsible for mistakes that occur

A script which controls the keyboard and mouse, including movement and what buttons are clicked.
To use it, please set the connection section like the example here, you can see the bottom section

```python
async def main():
  port_server = 8442
  ip_server = "192.168.1.4" # set it however you like, can be localhost or 196.168.x.x, for example this 192.168.1.4 or 0.0.0.0
  server = await websockets.serve(handle_connection, ip_server, port_server)
```

How to connect you just copy the [html](./index.html) to another device to access it, then in the prompt section you fill in the url or ws url in [server-unit.py](./server-unit.py)

You change the ip_server and port_server parts as you wish.

_This script is only used for testing and learning only_
