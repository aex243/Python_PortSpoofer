import asyncio

async def handle_client(reader, writer, port):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message} from {addr}")

    # Unique signature for each port
    response = f'Mock server on port {port} response\n'
    writer.write(response.encode())
    await writer.drain()

    print("Closing the connection")
    writer.close()

async def start_server(port):
    # Bind to the specific IP address
    server = await asyncio.start_server(
        lambda r, w: handle_client(r, w, port),
        '192.168.238.1', port
    )
    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

async def main():
    tasks = []
    for port in range(1024, 1501):
        task = asyncio.create_task(start_server(port))
        tasks.append(task)
    await asyncio.gather(*tasks)

asyncio.run(main())
