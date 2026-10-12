# Lab 6: REST vs gRPC

## Benchmark Results

All latency values are average milliseconds per operation (ms/op), except PING, which is average round-trip time (RTT). The local measurements were collected on the Mac, and the cloud measurements were collected from the west client VM.

| Method | Local (ms/op) | Same-Zone (ms/op) | Different Region (ms/op) |
|---|---:|---:|---:|
| REST add | 1.485 | 4.045 | 422.107 |
| gRPC add | 0.126 | 1.413 | 143.064 |
| REST rawimg | 2.225 | 12.231 | 1624.855 |
| gRPC rawimg | 0.884 | 15.703 | 200.894 |
| REST dotproduct | 1.616 | 4.785 | 349.002 |
| gRPC dotproduct | 0.142 | 1.608 | 208.160 |
| REST jsonimg | 9.818 | 46.086 | 1511.676 |
| gRPC jsonimg | 4.183 | 34.544 | 237.007 |
| PING (average RTT) | 1.161 | 0.563 | 141.428 |

## Observations

In the local measurements, gRPC had lower latency than REST for all four operations. In the same-zone cloud measurements, gRPC was faster for add, dotproduct, and jsonimg, while REST was faster for rawimg. In the different-region measurements, gRPC was faster for all four operations.

The average ping RTT increased from 0.563 ms within the same zone to 141.428 ms between the west and Europe regions. This substantial increase in network latency contributed to the higher cross-region operation times. Image operations also include the cost of transferring and processing image payloads, so their timings reflect more than network latency alone.

The REST client makes HTTP requests for individual operations, while the gRPC client reuses a channel and its underlying HTTP/2 connection across calls. Reusing a connection can reduce repeated connection-establishment overhead. The actual performance difference depends on the operation, payload, client implementation, and network conditions; gRPC is not guaranteed to be faster for every workload.

The local tests used 1,000 repetitions for add and dotproduct and 100 repetitions for rawimg and jsonimg. The cloud tests used the same repetition counts. These results describe this particular setup and should not be treated as universal performance guarantees.
