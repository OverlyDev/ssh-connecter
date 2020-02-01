import paramiko
import os
from Crypto.PublicKey import RSA


def main():
    os.system("rm *.key")
    generate_keys()
    connect_ssh("root", "127.0.0.1")


def generate_keys():
    key = RSA.generate(2048, os.urandom)

    with open("private.key", "wb") as f:
        f.write(key.export_key('PEM'))
        os.system("sudo chmod 0600 private.key")

    pubkey = key.publickey()
    with open("public.key", "wb") as f:
        f.write(pubkey.export_key('OpenSSH'))


def connect_ssh(target_user, target_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
    ssh.load_host_keys("public.key")

    # TODO: Connect hangs. If force stopped, the exceptions will print as they should but for some reason the dang
    #  thing hangs and I don't know why. Further investigation required.
    #  Also, I set all the timeouts to 2 in hopes of it actually timing out but that's not the case.
    try:
        ssh.connect(hostname=target_ip, username=target_user, key_filename="./public.key", auth_timeout=2, timeout=2,
                    banner_timeout=2)

    except paramiko.ssh_exception.AuthenticationException as e:
        print("[!] " + str(e))

    except paramiko.ssh_exception.NoValidConnectionsError as e:
        print("[!] " + e.strerror)

    finally:
        ssh.close()


if __name__ == '__main__':
    main()
