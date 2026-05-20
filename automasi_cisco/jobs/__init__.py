from nautobot.apps.jobs import register_jobs
from .cisco_config_job import KonfigurasiVlanInterface

# Mendaftarkan GUI Job dari file sebelah secara resmi
register_jobs(KonfigurasiVlanInterface)
