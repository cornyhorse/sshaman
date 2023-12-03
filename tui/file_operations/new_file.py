from management.sshman import SSHAMan


def new_file(group_path, alias, host, **kwargs):
    smn = SSHAMan()
    smn.add_server(group_path, alias, host, **kwargs)
