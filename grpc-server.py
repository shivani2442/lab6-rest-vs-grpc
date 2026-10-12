#!/usr/bin/env python3

import argparse
import base64
from concurrent import futures
import io
import logging

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Service(lab6_pb2_grpc.Lab6Servicer):

    def Add(self, request, context):
        return lab6_pb2.addReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            img.verify()

            img = Image.open(io.BytesIO(request.img))
            width, height = img.size

            return lab6_pb2.imageReply(
                width=width,
                height=height
            )
        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid image data"
            )

    def DotProduct(self, request, context):
        if len(request.a) != len(request.b):
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Vectors must have the same length"
            )

        result = sum(a * b for a, b in zip(request.a, request.b))

        return lab6_pb2.dotProductReply(dotproduct=result)

    def JsonImage(self, request, context):
        try:
            image_bytes = base64.b64decode(request.img, validate=True)

            img = Image.open(io.BytesIO(image_bytes))
            img.verify()

            img = Image.open(io.BytesIO(image_bytes))
            width, height = img.size

            return lab6_pb2.imageReply(
                width=width,
                height=height
            )
        except Exception:
            context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                "Invalid base64-encoded image"
            )


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    lab6_pb2_grpc.add_Lab6Servicer_to_server(
        Lab6Service(),
        server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()

    print(f"gRPC server listening on port {port}")
    print("Press Ctrl+C to stop.")

    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(grace=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lab 6 gRPC server")
    parser.add_argument(
        "-p", "--port",
        type=int,
        default=50051,
        help="Port on which to run the gRPC server"
    )

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    serve(args.port)
