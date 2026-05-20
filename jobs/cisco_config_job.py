from nautobot.apps.jobs import Job, StringVar, ObjectVar, register_jobs
from nautobot.dcim.models import Device

class KonfigurasiVlanInterface(Job):
    perangkat = ObjectVar(
        description="Pilih perangkat Cisco:",
        model=Device
    )
    nama_interface = StringVar(
        description="Masukkan nama port/interface:",
        default="GigabitEthernet0/1"
    )
    vlan_id = StringVar(
        description="Masukkan VLAN ID:",
        default="10"
    )

    class Meta:
        name = "Form Konfigurasi VLAN Port Cisco"
        description = "Uji coba GUI Form (Safe Mode)."
        has_sensitive_variables = False

    def run(self, data, commit):
        device_obj = data["perangkat"]
        interface = data["nama_interface"]
        vlan = data["vlan_id"]
        
        # Simulasi berhasil tanpa mengeksekusi koneksi SSH sungguhan
        self.logger.info(f"Menerima input dari GUI: Perangkat {device_obj.name}")
        self.logger.info(f"Target antarmuka: {interface}, VLAN: {vlan}")
        self.logger.success("GUI Berhasil dieksekusi! (Sistem aman, Netmiko dinonaktifkan sementara)")

register_jobs(KonfigurasiVlanInterface)
