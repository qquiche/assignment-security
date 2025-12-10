#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple


def receive_common_info(conn: socket.socket) -> Tuple[int, int]:
    data = conn.recv(1024).decode()
    base, prime_modulus = map(int, data.split(','))
    conn.sendall("ACK".encode())
    return (base, prime_modulus)

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_server(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_address, server_port))
    server_socket.listen(1)

    conn, addr = server_socket.accept()
    base, prime_modulus = receive_common_info(conn)

    secret = random.randint(1, 100)
    server_public = pow(base, secret, prime_modulus)

    client_public = int(conn.recv(1024).decode())
    conn.sendall(str(server_public).encode())

    shared_secret = pow(client_public, secret, prime_modulus)

    conn.close()
    server_socket.close()

    print(f"Base int is {base}")
    print(f"Modulus is {prime_modulus}")
    print(f"Secret is {secret}")
    print(f"Int received from peer is {client_public}")
    print(f"Shared secret is {shared_secret}")

    return (base, prime_modulus, secret, shared_secret)

def main(args):
    dh_exchange_server(args.address, args.port)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the server will bind to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the server will listen on.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
