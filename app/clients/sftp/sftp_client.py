from typing import Optional, Tuple

import paramiko
from paramiko import SFTPClient, Transport


def get_sftp_client(
        host: str,
        port: int,
        username: str,
        password: str
) -> Tuple[Optional[SFTPClient], Transport]:
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)
    return paramiko.SFTPClient.from_transport(transport), transport
