import asyncio
import socket
import logging

#Configure logging
logging.basicConfig(level=logging.INFO, filename='server_connections.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def handle_client(reader, writer, port):
    addr = writer.get_extra_info('peername')
    
    # Log the connection attempt
    logging.info(f"Connection attempt from {addr} on port {port}")

    try:
        data = await reader.read(100)
        #Decode with errors ignored
        message = data.decode('utf-8', errors='ignore')
        logging.info(f"Received data from {addr} on port {port}: {message}")
    except Exception as e:
        logging.error(f"Error handling data from {addr}: {e}")

    response = f"Mock server on port {port} response\n"
    writer.write(response.encode())
    await writer.drain()

    writer.close()
    await writer.wait_closed()  # Ensure the writer is properly closed

async def start_server(port):
    server = await asyncio.start_server(lambda r, w: handle_client(r, w, port), '0.0.0.0', port) #Set your Bind IP here ( by default all )
    async with server:
        await server.serve_forever()

#Function to check if a port is in use
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('0.0.0.0', port))
        except socket.error:
            return True
        return False

#Main routine to start servers on available port
async def main():
    tasks = []
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
