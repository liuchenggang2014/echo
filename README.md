# echo testing program in tcp/udp/grpc

1. udp echo
2. tcp echo
3. grpc insecure echo 
```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. echo.proto
```
4. grpc secure echo
```
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. echo.proto
```
```
# create the self signed certificate file to test secure grpc
openssl req -newkey rsa:2048 -nodes -keyout server.key -x509 -days 365 -out server.crt \
-subj "/C=CN/ST=BJ/L=BJ/O=goodvm/OU=IT/CN=grpc.goodvm.net"

# copy the certificate file(server.crt) onto the client and add one line into the /etc/hosts local dns file
35.194.230.220 grpc.goodvm.net
```
