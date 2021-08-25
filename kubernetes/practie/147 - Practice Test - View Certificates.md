Practice Test - View Certificates

- https://uklabs.kodekloud.com/topic/practice-test-view-certificate-details-2/

---

Q1. Identify the certificate file used for the `kube-api server`

```shell
root@controlplane:~# cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep "tls-cert-file"
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
```

---

Q2. Identify the Certificate file used to authenticate `kube-apiserver` as a client to `ETCD` Server

```shell
root@controlplane:~# cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep "etcd-certfile"
    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
```

---

Q3. Identify the key used to authenticate `kubeapi-server` to the `kubelet` server

```shell
root@controlplane:~# cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep "kubelet-client-key"
    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
```

---

Q4. Identify the ETCD Server Certificate used to host ETCD server

```shell
root@controlplane:~# cat /etc/kubernetes/manifests/etcd.yaml | grep "cert-file"
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
```

- `/etc/kubernetes/pki/etcd/server.crt`

---

Q5. Identify the ETCD Server CA Root Certificate used to serve ETCD Server

- ETCD can have its own CA. So this may be a different CA certificate than the one used by kube-api server.

```shell
root@controlplane:~# cat /etc/kubernetes/manifests/etcd.yaml | grep trusted-ca-file
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```

- `/etc/kubernetes/pki/etcd/ca.crt`

---

Q6. What is the Common Name (CN) configured on the Kube API Server Certificate?

- **OpenSSL Syntax:** `openssl x509 -in file-path.crt -text -noout`

```shell
root@controlplane:~# openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text
Certificate:
    Data:
        ...
        Subject: CN = kube-apiserver
```

- `kube-apiserver`

---

Q7. What is the name of the CA who issued the Kube API Server Certificate?

```shell
root@controlplane:~# openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number: 3741788026180140848 (0x33ed80628d46ff30)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: CN = kubernetes
```

- `kubernetes`

---

Q8. Which of the below alternate names is not configured on the Kube API Server Certificate?

```shell
root@controlplane:~# openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text
...
X509v3 Subject Alternative Name: 
  DNS:controlplane, DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc,
  DNS:kubernetes.default.svc.cluster.local, IP Address:10.96.0.1, IP Address:10.30.21.6
```

- X509v3 Subject Alternative Name 없는 항목은 `kube-master` 이다.

---

Q9. What is the Common Name (CN) configured on the ETCD Server certificate?

```shell
root@controlplane:~# openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -text
Certificate:
    Data:
       ...
        Subject: CN = controlplane
```



---

Q10. How long, from the issued date, is the Kube-API Server Certificate valid for?

- File: `/etc/kubernetes/pki/apiserver.crt`

```shell
root@controlplane:~# openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text
...
      Validity
            Not Before: Aug 24 13:45:34 2021 GMT
            Not After : Aug 24 13:45:35 2022 GMT
...
```

- 2021 ~ 2022 년 까지 1년

---

Q11. How long, from the issued date, is the Root CA Certificate valid for?

- File: `/etc/kubernetes/pki/ca.crt`

```shell
root@controlplane:~# openssl x509 -in /etc/kubernetes/pki/ca.crt -text
...
        Validity
            Not Before: Aug 24 13:45:34 2021 GMT
            Not After : Aug 22 13:45:34 2031 GMT
...
```

- 기간 설정이 10년이다.

---

Q12. Kubectl suddenly stops responding to your commands. Check it out! Someone recently modified the `/etc/kubernetes/manifests/etcd.yaml` file

- You are asked to investigate and fix the issue. Once you fix the issue wait for sometime for kubectl to respond. Check the logs of the ETCD container.

```shell
#
# /etc/kubernetes/pki/etcd/server-certificate.crt 있는지 확인
#
root@controlplane:~# cd /etc/kubernetes/pki/etcd/
root@controlplane:/etc/kubernetes/pki/etcd# ls
ca.crt  ca.key  healthcheck-client.crt  healthcheck-client.key  peer.crt  peer.key  server.crt  server.key

#
# cert-file 파일 찾기
#
root@controlplane:~# ls -l /etc/kubernetes/pki/etcd/server* | grep .crt
-rw-r--r-- 1 root root 1188 Aug 24 13:45 /etc/kubernetes/pki/etcd/server.crt

#
# etcd.yaml 수정
#
vi /etc/kubernetes/manifests/etcd.yaml
#   - --cert-file=/etc/kubernetes/pki/etcd/server-certificate.crt
   - --cert-file=/etc/kubernetes/pki/etcd/server.crt
   
root@controlplane:~# kubectl -n kube-system delete pod kube-apiserver-controlplane 
pod "kube-apiserver-controlplane" deleted
root@controlplane:~# kubectl apply -f /etc/kubernetes/manifests/etcd.yaml
pod/etcd created
root@controlplane:~# kubectl -n kube-system get pod 
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-74ff55c5b-mgcgq                1/1     Running   0          28m
coredns-74ff55c5b-tfh9t                1/1     Running   0          28m
etcd-controlplane                      1/1     Running   0          2m10s
kube-apiserver-controlplane            1/1     Running   6          28m
kube-controller-manager-controlplane   1/1     Running   1          28m
kube-flannel-ds-bg7c8                  1/1     Running   0          28m
kube-proxy-xvfn5                       1/1     Running   0          28m
kube-scheduler-controlplane            1/1     Running   1          28m
```

---

Q13. The kube-api server stopped again! Check it out. Inspect the kube-api server logs and identify the root cause and fix the issue.

- Run `docker ps -a` command to identify the kube-api server container. 
- Run `docker logs container-id` command to view the logs.

```shell
#
# If we inspect the kube-apiserver container on the controlplane, we can see that it is frequently exiting.
#
root@controlplane:~# docker ps -a | grep kube-apiserver
f540e60cfe72        ca9843d3b545           "kube-apiserver --ad…"   About a minute ago   Exited (1) About a minute ago                       k8s_kube-apiserverkube-apiserver-controlplane_kube-system_e35cc6f28d99d517373fa2e2abd59742_4
5b2bb9d23aff        k8s.gcr.io/pause:3.2   "/pause"                 4 minutes ago        Up 4 minutes                                        k8s_POD_kube-apiserver-controlplane_kube-system_e35cc6f28d99d517373fa2e2abd59742_0


#
# If we now inspect the logs of this exited container, we would see the following errors:
#
root@controlplane:~# docker logs f540e60cfe72 --tail=2
W0824 14:21:18.143608       1 clientconn.go:1223] grpc: addrConn.createTransport failed to connect to {https://127.0.0.1:2379  <nil> 0 <nil>}. Err :connection error: desc = "transport: authentication handshake failed: x509: certificate signed by unknown authority". Reconnecting...
Error: context deadline exceeded
root@controlplane:~# 

#
# vi kube-apiserver.yaml
#
vi /etc/kubernetes/manifests/kube-apiserver.yaml

#    - --etcd-cafile=/etc/kubernetes/pki/ca.crt
    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
    
#
# 수정결과 확인
#
root@controlplane:~# docker ps -a | grep kube-apiserver
75503ee06667        ca9843d3b545           "kube-apiserver --ad…"   About a minute ago   Up About a minute                                 k8s_kube-apiserver_kube-apiserver-controlplane_kube-system_f75cac65a6eabbeaef1c805e337818a6_0
c825025a243d        k8s.gcr.io/pause:3.2   "/pause"                 About a minute ago   Up About a minute                                 k8s_POD_kube-apiserver-controlplane_kube-system_f75cac65a6eabbeaef1c805e337818a6_0
```

