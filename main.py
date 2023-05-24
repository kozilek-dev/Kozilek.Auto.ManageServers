from manager import server_manager


if __name__ == '__main__':
    manager = server_manager.MinecraftManager()
    server = server_manager.MinecraftServer('mc-test3', 19133, {'EULA': 'TRUE'})
    created_server = manager.create_server(server)