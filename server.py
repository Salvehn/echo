import asyncio
from datetime import datetime
import sys
import re
allowed = ['echo', 'calendar', 'stop' ]


def respond(message):
    match = re.match(rf"({'|'.join(allowed)})[\s]?(.+)?",message)
    command=''
    if match:
        command=match.group(1)
        if command=='echo':
            data = match.group(2)
        elif command=='calendar':
            data = datetime.strftime(datetime.now(), "%Y.%m.%d %H:%M")
        elif command=='stop':
            data = 'TCP Server stops...'
    else:
        data = f'Available commands: {", ".join(allowed)}'
    return data


async def echo_handler(reader, writer):
    addr = writer.get_extra_info('peername')

    data = await reader.read(100)
    message = str(data.decode())
    print(f"Received '{message}' from {addr}")

    data = respond(message)
    print(f"Sending: {data}")
    writer.write(data.encode())
    await writer.drain()


    writer.close()

    if message.startswith('stop'):
        sys.exit(0)


async def main():
    server = await asyncio.start_server(echo_handler, '127.0.0.1', 8888)
    addr = server.sockets[0].getsockname()
    print(f'TCP Server started: {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
