#!/usr/bin/env python3

import argparse
import base64
import random
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc


IMAGE_FILE = "Flatirons_Winter_Sunrise_edit_2.jpg"


def doAdd(stub, debug=False):
    response = stub.Add(lab6_pb2.addMsg(a=5, b=10))

    if debug:
        print("Response:", response)
        assert response.sum == 15


def doRawImage(stub, debug=False):
    with open(IMAGE_FILE, "rb") as image_file:
        image_bytes = image_file.read()

    response = stub.RawImage(
        lab6_pb2.rawImageMsg(img=image_bytes)
    )

    if debug:
        print("Response:", response)


def doDotProduct(stub, debug=False):
    a = [random.random() for _ in range(100)]
    b = [random.random() for _ in range(100)]

    response = stub.DotProduct(
        lab6_pb2.dotProductMsg(a=a, b=b)
    )

    if debug:
        print("Response:", response)


def doJsonImage(stub, debug=False):
    with open(IMAGE_FILE, "rb") as image_file:
        image_bytes = image_file.read()

    encoded_image = base64.b64encode(image_bytes).decode("ascii")

    response = stub.JsonImage(
        lab6_pb2.jsonImageMsg(img=encoded_image)
    )

    if debug:
        print("Response:", response)


parser = argparse.ArgumentParser(
    description="Lab 6 gRPC client for timing RPC operations"
)

parser.add_argument(
    "host",
    help="Hostname or IP address of the gRPC server"
)

parser.add_argument(
    "cmd",
    choices=["add", "rawImage", "dotProduct", "jsonImage"],
    help="Operation to perform"
)

parser.add_argument(
    "reps",
    type=int,
    help="Number of repetitions"
)

parser.add_argument(
    "-p", "--port",
    type=int,
    default=50051,
    help="Server port (default: 50051)"
)

parser.add_argument(
    "-d", "--debug",
    action="store_true",
    help="Print responses"
)

args = parser.parse_args()

if args.reps <= 0:
    parser.error("reps must be greater than zero")

address = f"{args.host}:{args.port}"
print(f"Running {args.reps} reps against {address}")

operations = {
    "add": doAdd,
    "rawImage": doRawImage,
    "dotProduct": doDotProduct,
    "jsonImage": doJsonImage,
}

with grpc.insecure_channel(address) as channel:
    stub = lab6_pb2_grpc.Lab6Stub(channel)

    grpc.channel_ready_future(channel).result(timeout=10)

    operation = operations[args.cmd]

    operation(stub, debug=False)

    start = time.perf_counter()

    for _ in range(args.reps):
        operation(stub, debug=args.debug)

    elapsed = time.perf_counter() - start
    milliseconds_per_operation = elapsed * 1000 / args.reps

    print(f"Took {milliseconds_per_operation:.3f} ms per operation")
