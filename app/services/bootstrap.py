from concurrent import futures
from ..constants import MAX_WORKERS
import grpc

grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=MAX_WORKERS))
