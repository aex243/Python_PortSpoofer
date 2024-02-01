import asyncio
import socket

async def handle_client(reader, writer, port):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message} from {addr}")

    response = f'Mock server on port {port} response\n'
    writer.write(response.encode())
    await writer.drain()

    print("Closing the connection")
    writer.close()

async def start_server(port):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, port), '192.168.238.1', port) #Set your Bind IP here
    addr = server.sockets[0].getsockname()
    print(f'Server started, serving on {addr}')

    async with server:
        await server.serve_forever()
        
#Function to check if a port is in use#
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('192.168.238.1', port))
        except socket.error:
            return True
        return False

#Main routine to start servers on available port
async def main():
    tasks = []
    ip = '192.168.238.1'
    print("Checking available ports...")
    for port in range(1024, 65535): #Set port range here
        if not is_port_in_use(port):
            print(f"Starting server on port {port}")
            task = asyncio.create_task(start_server(port))
            tasks.append(task)
        else:
            print(f"Skipping port {port} as it is in use.")
    print("All available servers started. Running...")
    await asyncio.gather(*tasks)

asyncio.run(main())
