from apscheduler.schedulers.background import BackgroundScheduler
from jobs.IJob import IJob
from manager.server_manager import MinecraftManager

universal_manager = MinecraftManager()


class BackupContainersJob(IJob):
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.action = lambda: self.backup_servers()
        super().__init__(self.action, hours, minutes, seconds)

    def backup_servers(self):
        servers = universal_manager.get_all_servers()
        for server in servers:
            universal_manager.backup_server(server)
