from sshtunnel import SSHTunnelForwarder
import psycopg2
import tkinter as tk

def connect_to_db():
    # Read credentials from pass.conf
    with open("pass.conf", "r") as f:
        lines = f.read().splitlines()
        ssh_user = lines[0]
        ssh_pass = lines[1]
        db_user = lines[2]
        db_pass = lines[3]

    ssh_tunnel = SSHTunnelForwarder(
        ("pascal.fis.agh.edu.pl", 22),
        ssh_username=ssh_user,
        ssh_password=ssh_pass,
        remote_bind_address=("localhost", 5432),
        local_bind_address=("localhost", 5432),
    )
    ssh_tunnel.start()

    conn = psycopg2.connect(
        host="localhost",
        port=ssh_tunnel.local_bind_port,
        user=db_user,
        password=db_pass,
        dbname="u2kopyto",
    )
    return conn, ssh_tunnel
