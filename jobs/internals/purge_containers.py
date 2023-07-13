from apscheduler.schedulers.background import BackgroundScheduler
from jobs.IJob import IJob
from manager.server_manager import MinecraftManager

universal_manager = MinecraftManager()


class PurgeContainersJob(IJob):
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.action = lambda: self.purge_servers()
        super().__init__(self.action, hours, minutes, seconds)

    def purge_servers(self):
        servers = universal_manager.get_all_servers()
        for server in servers:
            if not universal_manager.is_healthy(server):
                universal_manager.delete_server(server)
