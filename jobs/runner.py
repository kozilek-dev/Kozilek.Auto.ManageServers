import logging
from apscheduler.schedulers.background import BackgroundScheduler


class Runner:
    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def add_job(self, job):
        logging.info(f"Job adicionado com sucesso: {job}")
        self.scheduler.add_job(job.action, 'interval', hours=job.hours, minutes=job.minutes, seconds=job.seconds)

    def start(self):
        logging.info("Iniciando agendador...")
        self.scheduler.start()
