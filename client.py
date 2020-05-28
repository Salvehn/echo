import asyncio

looping = True


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f"Server responded: {str(data.decode())}\n")

    if str(data.decode()).startswith('stop'):
        global looping
        looping = False

    writer.close()
    await writer.wait_closed()

if __name__ == '__main__':
    while looping:
        print('Type command: ')
        command = input()
        if command == '':
            command='help'
        asyncio.run(tcp_echo_client(command))
