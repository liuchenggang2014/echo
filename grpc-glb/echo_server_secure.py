import grpc

import echo_pb2 as pb2
import echo_pb2_grpc as pb2_grpc

from concurrent import futures
import time

# implement the echo service
class echo(pb2_grpc.echoServicer):
    def GetEcho(self, request, context):
        name = request.name
        
        greet = f'grpc get the request name={name}'

        return pb2.GetEchoReply(result=greet)

def run():

    # get the private key and ca file and create 
    with open('server.pem', 'rb') as f:
        private_key = f.read()
    with open('ca.pem', 'rb') as f:
        certificate_chain = f.read()

    server_credentials = grpc.ssl_server_credentials(
      ((private_key, certificate_chain,),))
    
    # create the grpc server
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4)
    )

    # add the service into the grpc server
    pb2_grpc.add_echoServicer_to_server(echo(), grpc_server)

    # bind the  grpc server with a ip and port
    grpc_server.add_secure_port("0.0.0.0:5001", server_credentials)
    print("server started securely on 0.0.0.0:5001")

    grpc_server.start()

    try:
        while 1:
            time.sleep(3600)
    except KeyboardInterrupt:
        grpc_server.stop(0)


if __name__=="__main__":
    run()