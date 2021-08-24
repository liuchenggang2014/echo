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
5. setup glb support grpc(only secure mode)
- step1: create the self signed certificate and upload it into glb
[reference doc](https://cloud.google.com/load-balancing/docs/ssl-certificates/self-managed-certs)

```
openssl genrsa -out server.pem 2048
```

```
# create csr file
openssl req -new -key server.pem \
    -out csr.pem \
    -config csr.config \
    -subj "/C=CN/ST=BJ/L=BJ/O=goodvm/OU=IT/CN=grpc.goodvm.net"
```

```
# self sign the csr file to generate the ca file
openssl x509 -req -signkey server.pem -in csr.pem -out ca.pem -days 365
```

```
gcloud compute ssl-certificates create self-signed-grpc-good-vm \           
    --certificate=ca.pem \
    --private-key=server.pem \   
    --global
```

- step 2: upload the ca and key file into the grpc server and run it with specified port

- step3: config the glb with https(http2) and backend service with http2
```
# describe forwarding rule
cliu@dev2:~/ssl $ gcloud compute forwarding-rules describe glb-dev2-http-forwarding-rule-2 --global
IPAddress: 35.241.27.231
IPProtocol: TCP
creationTimestamp: '2021-08-12T05:52:47.509-07:00'
description: ''
fingerprint: V3sLfk9cgRU=
id: '8209510847680653168'
kind: compute#forwardingRule
labelFingerprint: 42WmSpB8rSM=
loadBalancingScheme: EXTERNAL
name: glb-dev2-http-forwarding-rule-2
networkTier: PREMIUM
portRange: 443-443
selfLink: https://www.googleapis.com/compute/v1/projects/cliu101/global/forwardingRules/glb-dev2-http-forwarding-rule-2
target: https://www.googleapis.com/compute/v1/projects/cliu101/global/targetHttpsProxies/glb-dev2-http-target-proxy-2
```

```
# describe target proxy
cliu@dev2:~/ssl $ gcloud compute target-https-proxies describe glb-dev2-http-target-proxy-2 --global
creationTimestamp: '2021-08-12T05:52:43.445-07:00'
fingerprint: DHgl5JHvYY8=
id: '9202884977349928820'
kind: compute#targetHttpsProxy
name: glb-dev2-http-target-proxy-2
quicOverride: NONE
selfLink: https://www.googleapis.com/compute/v1/projects/cliu101/global/targetHttpsProxies/glb-dev2-http-target-proxy-2
sslCertificates:
- https://www.googleapis.com/compute/v1/projects/cliu101/global/sslCertificates/self-signed-grpc-good-vm
urlMap: https://www.googleapis.com/compute/v1/projects/cliu101/global/urlMaps/glb-dev2-http
```

```
# describe backend service
cliu@dev2:~/ssl $ gcloud compute backend-services describe bs-dev2-5001 --global
affinityCookieTtlSec: 0
backends:
- balancingMode: UTILIZATION
  capacityScaler: 1.0
  group: https://www.googleapis.com/compute/v1/projects/cliu101/zones/asia-east1-b/instanceGroups/dev2-group
  maxUtilization: 0.8
connectionDraining:
  drainingTimeoutSec: 300
creationTimestamp: '2021-08-23T02:17:44.003-07:00'
description: ''
enableCDN: false
fingerprint: yoIdFX3c5Pc=
healthChecks:
- https://www.googleapis.com/compute/v1/projects/cliu101/global/healthChecks/hc-http
id: '3696128212520065368'
kind: compute#backendService
loadBalancingScheme: EXTERNAL
logConfig:
  enable: false
name: bs-dev2-5001
port: 80
portName: secure-grpc
protocol: HTTP2
selfLink: https://www.googleapis.com/compute/v1/projects/cliu101/global/backendServices/bs-dev2-5001
sessionAffinity: NONE
timeoutSec: 30
```

