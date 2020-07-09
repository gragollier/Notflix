import logging
import paramiko
import os

def seed(file, hosts):
    for host in hosts:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host['host'], port=host['port'], username="root", key_filename=host['key'], look_for_keys=False)

        logging.info(f"Uploading file to {host}")

        sftp = ssh.open_sftp()
        sftp.put(file, f"/usr/share/nginx/html/{file}")
        sftp.close()

        logging.info(f"Extracting archive")

        ssh.exec_command(f"mkdir /usr/share/nginx/html/{file.strip('.zip')}")
        ssh.exec_command(f"mv /usr/share/nginx/html/{file} /usr/share/nginx/html/{file.strip('.zip')}/{file}")
        ssh.exec_command(f"cd /usr/share/nginx/html/{file.strip('.zip')}")
        logging.info(ssh.exec_command(f"unzip /usr/share/nginx/html/{file.strip('.zip')}/{file} -d /usr/share/nginx/html/{file.strip('.zip')}")[2].readlines())
        ssh.exec_command(f"rm /usr/share/nginx/html/{file.strip('.zip')}/{file}")
        ssh.exec_command(f"chmod a+rx /usr/share/nginx/html/{file.strip('.zip')}/*")
        ssh.close()

    logging.info("Cleaning up local zip file")

    os.remove(file)

    return file.strip('.zip')