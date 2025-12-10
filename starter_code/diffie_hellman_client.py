#!/usr/bin/env python3
import socket
import argparse
import random
from pathlib import Path
from typing import Tuple


def send_common_info(sock: socket.socket, server_address: str, server_port: int) -> Tuple[int, int]:
    sock.connect((server_address, server_port))

    base = random.randint(2, 100)
    prime_modulus = random.randint(2, 100)

    message = f"{base},{prime_modulus}".encode()
    sock.sendall(message)

    ack = sock.recv(1024).decode()

    return (base, prime_modulus)

# Do NOT modify this function signature, it will be used by the autograder
def dh_exchange_client(server_address: str, server_port: int) -> Tuple[int, int, int, int]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    base, prime_modulus = send_common_info(sock, server_address, server_port)

    secret = random.randint(1, 100)
    client_public = pow(base, secret, prime_modulus)

    sock.sendall(str(client_public).encode())
    server_public = int(sock.recv(1024).decode())

    shared_secret = pow(server_public, secret, prime_modulus)
    sock.close()

    print("Base proposal successful.")
    print(f"Base int is {base}")
    print(f"Modulus is {prime_modulus}")
    print(f"Secret is {secret}")
    print(f"Int received from peer is {server_public}")
    print(f"Shared secret is {shared_secret}")

    return (base, prime_modulus, secret, shared_secret)


def main(args):
    if args.seed:
        random.seed(args.seed)
    
    dh_exchange_client(args.address, args.port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--address",
        default="127.0.0.1",
        help="The address the client will connect to.",
    )
    parser.add_argument(
        "-p",
        "--port",
        default=8000,
        type=int,
        help="The port the client will connect to.",
    )
    parser.add_argument(
        "--seed",
        dest="seed",
        type=int,
        help="Random seed to make the exchange deterministic.",
    )
    # Parse options and process argv
    arguments = parser.parse_args()
    main(arguments)
