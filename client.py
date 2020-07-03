import grpc

import currency_pb2
import currency_pb2_grpc

channel = grpc.insecure_channel('localhost:50051')
stub = currency_pb2_grpc.CurrencyStub(channel)

request = currency_pb2.Empty()

response = stub.getAll(request)

print(response)
