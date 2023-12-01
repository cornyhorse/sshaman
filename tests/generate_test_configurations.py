def generate_default_config(test_config_path):
    from entities import ServerGroup, Server
    print("Generating default config...")
    g1 = ServerGroup(group_name='group1', sshaman_path=test_config_path)
    g1.make_child('sg1')

    s = Server(
        alias='vm1',
        host='192.168.1.100',
        port=22,
        user='root',
        password='12345',
        identity_file='~/.ssh/id_rsa',
        forward_ports=[
            '80:localhost:8080',
            '443:localhost:8443'
        ],
        start_commands=["echo 'hello world'", "ls -la"]
    )
    g1.add_server(s)


    s2 = Server(
        alias='vm2',
        host='192.168.1.100',
        port=22,
        user='root',
        password='12345',
        identity_file='~/.ssh/id_rsa',
        forward_ports=[
            '80:localhost:8080',
            '443:localhost:8443'
        ],
        start_commands=["echo 'hello world'", "ls -la"]
    )

    sg2 = g1.children['sg1']
    sg2.add_server(s2)
    g2 = ServerGroup(group_name='group2', sshaman_path=test_config_path)
    group_list = [g1, g2]
    return group_list
