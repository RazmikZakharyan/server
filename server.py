import socket
import asyncio


class Server:
    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        self.main_loop = asyncio.get_event_loop()

        self.users = []

    def set_up(self):
        self.socket.bind(
            ("208.67.222.222", 8000)
        )

        self.socket.listen(5)
        self.socket.setblocking(False)
        print("Server is listening")

    async def send_data(self, data, user_):
        for user in self.users:
            await self.main_loop.sock_sendall(user,
                                              f'|{user_.getsockname()[0]}|'
                                              f'{data.decode()}'.encode())

    async def listen_socket(self, listened_socket: socket.socket = None):
        while True:
            try:
                data = await self.main_loop.sock_recv(listened_socket, 2024)
                await self.send_data(data, listened_socket)
            except ConnectionResetError:
                self.users.remove(listened_socket)
                print(f'User disconnected')
                return

    async def accept_sockets(self):
        while True:
            user_socket, address = await self.main_loop.sock_accept(
                self.socket)
            print(f"User <{address[0]}> connected!")

            self.users.append(user_socket)
            self.main_loop.create_task(self.listen_socket(user_socket))

    async def main(self):
        await self.main_loop.create_task(self.accept_sockets())

    def start(self):
        self.main_loop.run_until_complete(self.main())


if __name__ == '__main__':
    server = Server()
    server.set_up()
    server.start()
