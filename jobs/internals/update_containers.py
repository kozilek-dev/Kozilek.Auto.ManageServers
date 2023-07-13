from apscheduler.schedulers.background import BackgroundScheduler
from jobs.IJob import IJob
from manager.server_manager import MinecraftManager

universal_manager = MinecraftManager()


class UpdateContainersJob(IJob):
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.action = lambda: self.update_servers()
        super().__init__(self.action, hours, minutes, seconds)

    def update_servers(self):
        servers = universal_manager.get_all_servers()
        for server in servers:
            universal_manager.update_server(server)
