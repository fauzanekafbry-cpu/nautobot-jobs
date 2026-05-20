from nautobot.apps.jobs import Job, StringVar, ObjectVar
from nautobot.dcim.models import Device
from netmiko import ConnectHandler

# Variabel global untuk mengelompokkan menu di dashboard Nautobot
name = "Otomasi Cisco IOS"

class KonfigurasiVlanInterface(Job):
    # ---Bagian 1: Definisi GUI Form ---
    # Nautobot akan otomatis membuat dropdown perangkat berdasarkan data di database
    perangkat = ObjectVar(
        description="Pilih perangkat Cisco yang ingin dikonfigurasi:",
        model=Device
    )
    nama_interface = StringVar(
        description="Masukkan nama port/interface (contoh: GigabitEthernet0/1):",
        default="GigabitEthernet0/1"
    )
    vlan_id = StringVar(
        description="Masukkan VLAN ID baru (contoh: 10):",
        default="10"
    )

    # Metadata untuk tampilan di halaman utama Nautobot
    class Meta:
        name = "Form Konfigurasi VLAN Port Cisco"
        description = "GUI untuk mengubah VLAN pada port Switch Cisco secara aman tanpa CLI."
        has_sensitive_variables = False

    # --- Bagian 2: Logika Python Script (Eksekusi) ---
    def run(self, data, commit):
        # Mengambil data yang diinput oleh user dari GUI Form
        device_obj = data["perangkat"]
        interface = data["nama_interface"]
        vlan = data["vlan_id"]

        # Mengambil IP address perangkat langsung dari database Nautobot
        if not device_obj.primary_ip4:
            self.logger.error(f"Perangkat {device_obj.name} tidak memiliki IP utama di Nautobot.")
            return
        
        ip_address = str(device_obj.primary_ip4.address.ip)
        self.logger.info(f"Memulai koneksi ke {device_obj.name} ({ip_address})...")

        # Kredensial perangkat (bisa disesuaikan dengan Cisco DevNet Sandbox Anda)
        kredensial_cisco = {
            'device_type': 'cisco_ios',
            'host': ip_address,
            'username': 'developer',  # Ganti sesuai kredensial sandbox/perangkat
            'password': 'C1sco12345',
            'secret': 'C1sco12345',
        }

        # Menyusun perintah CLI Cisco berdasarkan input dari GUI menggunakan Template f-string
        perintah_cli = [
            f"interface {interface}",
            "switchport mode access",
            f"switchport access vlan {vlan}"
        ]

        # Eksekusi SSH menggunakan Netmiko
        try:
            self.logger.info("Menghubungkan ke switch via SSH...")
            
            # Membuka koneksi SSH
            net_connect = ConnectHandler(**kredensial_cisco)
            net_connect.enable()
            
            self.logger.info(f"Mengirimkan perintah konfigurasi ke {interface}...")
            # Mengirimkan perintah CLI ke Cisco
            output = net_connect.send_config_set(perintah_cli)
            
            # Menampilkan log hasil eksekusi CLI ke GUI Nautobot agar bisa dibaca engineer
            self.logger.info(f"Output dari perangkat:\n{output}")
            
            # Memutuskan koneksi SSH
            net_connect.disconnect()
            
            self.logger.success(f"Berhasil! Interface {interface} sekarang berada di VLAN {vlan}.")
            
        except Exception as e:
            # Jika ada error (misal salah password/gagal SSH), log error akan muncul di GUI
            self.logger.error(f"Gagal melakukan konfigurasi ke perangkat: {str(e)}")