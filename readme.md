# Título del Proyecto

Breve descripción del proyecto.

## Requisitos

- Requisito 1
- Requisito 2
- Requisito 3

## Instalación

1. Clona el repositorio.
2. Ejecuta el comando `npm install` para instalar las dependencias.
3. Configura las variables de entorno en el archivo `.env`.
4. Ejecuta el comando `npm start` para iniciar la aplicación.

## Uso

Explica cómo utilizar tu proyecto y proporciona ejemplos de código si es necesario.

## Contribución

Si deseas contribuir a este proyecto, sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios necesarios y realiza un commit (`git commit -m 'Agrega nueva característica'`).
4. Haz push a la rama (`git push origin feature/nueva-caracteristica`).
5. Abre una Pull Request.

## Licencia

Indica la licencia bajo la cual se distribuye tu proyecto.

## Contacto

Si tienes alguna pregunta o sugerencia, no dudes en contactarme a través de [correo electrónico](correo@example.com) o [Twitter](https://twitter.com/tu_usuario).



Para realizar las mediciones de latencia, throughput, packet loss e inter-arrival time en tu red 5G personal, puedes seguir estos pasos y usar las siguientes herramientas:

### 1. **Preparación del Entorno**
   
   - **Conexión Remota:**
     - **SSH:** Configura los PCs del UE, gNB y CORE para que acepten conexiones SSH. Esto te permitirá acceder y controlar remotamente los dispositivos sin necesidad de estar físicamente presente en la sala.
     - **TMUX/Screen:** Utiliza herramientas como `tmux` o `screen` para mantener las sesiones SSH activas y poder desconectarte sin interrumpir los procesos en ejecución.
   
   - **Automatización:**
     - **Python Scripts:** Usa Python junto con bibliotecas como `paramiko` para SSH y `subprocess` para ejecutar comandos y recopilar datos. Puedes crear una GUI simple utilizando `Tkinter` o una interfaz web ligera con `Flask`.

### 2. **Herramientas de Medición**

   - **Iperf3:**
     - **Latencia y Throughput:** Configura `iperf3` para medir el throughput y latencia entre el UE y el CORE. `iperf3` puede funcionar en modo cliente-servidor, y te dará métricas como bitrate, jitter y pérdida de paquetes.
     - **Packet Loss:** Iperf3 también reporta el número de datagramas perdidos, lo que te permite calcular la tasa de pérdida de paquetes.
   
   - **Ping:**
     - **Latencia:** Usa el comando `ping` para medir la latencia. Ejecuta ping desde el UE al CORE y registra los tiempos de respuesta (RTT).

   - **TCPDump/Wireshark:**
     - **Inter-arrival Time y Packet Analysis:** Utiliza `tcpdump` para capturar tráfico en la interfaz de red y `Wireshark` para analizar los tiempos de llegada de los paquetes, jitter, y otros detalles.

### 3. **Procedimiento Detallado**

   **Paso 1: Configurar y ejecutar Iperf3**
   
   - **Servidor Iperf3 en CORE:**
     ```bash
     iperf3 -s
     ```
   
   - **Cliente Iperf3 en UE:**
     ```bash
     iperf3 -c <CORE_IP> -u -b 10M -t 60
     ```

   Esto medirá el throughput y te dará estadísticas sobre la latencia y pérdida de paquetes.

   **Paso 2: Ejecutar Ping para Latencia**

   En el UE, ejecuta:
   ```bash
   ping <CORE_IP> -c 100
   ```

   Esto te dará la latencia promedio, mínima, máxima y desviación estándar.

   **Paso 3: Capturar y analizar tráfico con Tcpdump**

   - **Captura en el UE:**
     ```bash
     sudo tcpdump -i eth0 -w ue_capture.pcap
     ```

   - **Captura en el CORE:**
     ```bash
     sudo tcpdump -i eth0 -w core_capture.pcap
     ```

   - **Análisis con Wireshark:**
     Abre los archivos .pcap en Wireshark y utiliza la funcionalidad de análisis de tiempo de llegada de paquetes.

### 4. **Automatización y Recolección de Datos**

   - **Python Script de Ejemplo:**
     ```python
     import paramiko
     import subprocess
     
     def run_ssh_command(host, username, password, command):
         ssh = paramiko.SSHClient()
         ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
         ssh.connect(host, username=username, password=password)
         stdin, stdout, stderr = ssh.exec_command(command)
         output = stdout.read().decode()
         ssh.close()
         return output
     
     ue_host = 'ue_ip'
     core_host = 'core_ip'
     username = 'your_username'
     password = 'your_password'
     
     # Run iperf3 on UE
     iperf_command = 'iperf3 -c {} -u -b 10M -t 60'.format(core_host)
     iperf_output = run_ssh_command(ue_host, username, password, iperf_command)
     print("Iperf3 Output:", iperf_output)
     
     # Run ping on UE
     ping_command = 'ping {} -c 100'.format(core_host)
     ping_output = run_ssh_command(ue_host, username, password, ping_command)
     print("Ping Output:", ping_output)
     
     # Run tcpdump on UE
     tcpdump_command = 'sudo tcpdump -i eth0 -w ue_capture.pcap'
     tcpdump_output = run_ssh_command(ue_host, username, password, tcpdump_command)
     print("Tcpdump Output:", tcpdump_output)
     ```

   - **Automatización con Crontab:**
     Configura tareas en crontab para ejecutar estos scripts periódicamente si necesitas recopilar datos de manera continua.

### 5. **Esquema del Procedimiento**

1. **Configuración Inicial:**
   - Establecer conexión SSH en todos los nodos.
   - Instalar y configurar `iperf3`, `ping`, `tcpdump`.

2. **Ejecución de Pruebas:**
   - Ejecutar `iperf3` para throughput y latencia.
   - Ejecutar `ping` para latencia detallada.
   - Capturar tráfico con `tcpdump`.

3. **Análisis de Datos:**
   - Analizar archivos .pcap con Wireshark.
   - Procesar y graficar resultados de `iperf3` y `ping` con Python.

4. **Automatización:**
   - Crear scripts en Python para ejecutar comandos y recopilar resultados.
   - Usar crontab para programar la ejecución de scripts.

Este procedimiento te permitirá obtener las mediciones necesarias para tu trabajo de fin de grado, con herramientas ampliamente usadas en la industria y métodos de análisis robustos.

