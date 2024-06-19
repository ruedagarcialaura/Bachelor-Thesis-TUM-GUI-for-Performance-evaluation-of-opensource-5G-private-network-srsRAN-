import paramiko
#from views.latency_view import Latency_view

class SSHClient:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)

    def execute_command(self, command):
        if self.client:
            stdin, stdout, stderr = self.client.exec_command(command)
            return stdout.read()
        else:
            return "Not connected."
        
    def execute_command_async(self, command, output_callback=None):
        if self.client:
           stdin, stdout, stderr = self.client.exec_command(command)
           # Leer la salida estándar del comando línea por línea
           while True:
               line = stdout.readline()
               if not line:
                   break
               if output_callback:
                   output_callback(line)
            #Después de leer toda la salida, puedes decidir qué hacer con stderr
            #Por ejemplo, leer y registrar los errores si los hay
           errors = stderr.read().decode('utf-8')
           if errors:
               # Manejar los errores como prefieras
                print("Errors:", errors)
        else:
           print("Not connected.")
        
    def download_file(self, remote_path, local_path):
        if self.client:
            sftp = self.client.open_sftp()
            sftp.get(remote_path, local_path)
            sftp.close()
        else:
            return "Not connected."

    def close(self):
        if self.client:
            self.client.close()