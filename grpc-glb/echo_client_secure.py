import grpc

import echo_pb2 as pb2
import echo_pb2_grpc as pb2_grpc

# reference code in : https://github.com/sandtable/ssl_grpc_example/
# https://www.openssl.org/docs/man1.0.2/man1/req.html

def run():
    # read the ca and create the credentials
    with open('ca.pem', 'rb') as f:
        trusted_certs = f.read()

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    # create channel
    conn = grpc.secure_channel("grpc.goodvm.net:443", credentials)

    # create client stub
    client = pb2_grpc.echoStub(conn)

    # call the service and get the echo response
    response = client.GetEcho(pb2.GetEchoReq(
        name = "cliu-secure"
    ))
    print(response)

if __name__ == '__main__':
    run()