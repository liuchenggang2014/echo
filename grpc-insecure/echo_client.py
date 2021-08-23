import grpc

import echo_pb2 as pb2
import echo_pb2_grpc as pb2_grpc

def run():
    # create channel
    conn = grpc.insecure_channel('35.194.230.220:5000')

    # create client stub
    client = pb2_grpc.echoStub(conn)

    # call the service and get the echo response
    response = client.GetEcho(pb2.GetEchoReq(
        name = "cliu111"
    ))
    print(response)

if __name__ == '__main__':
    run()