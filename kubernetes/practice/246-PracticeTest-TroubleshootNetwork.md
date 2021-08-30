Practice Test - Troubleshoot Network

- https://uklabs.kodekloud.com/topic/practice-test-troubleshoot-network-2/

---

Q1. `Troubleshooting Test 1:` A simple 2 tier application is deployed in the `triton` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

- DB Service working?
- WebApp Service working?

```shell
kubectl describe pods -n triton
# mysql Pod 의 상태가 Pending 으로 되어 있다.
# 이벤트 로그 부분을 보면
# networkPlugin cni failed to teardown pod ....이라고 출력된다.

# weave 이라는 네트워크 플러그인을 설치한다.
kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')"

kubectl describe pods -n triton
# mysql Pod 의 상태가 Running 으로 되어 있고, IP 주소가 할당되었다.
# 웹 페이지도 정상으로 출력된다.

kubectl get pods -n kube-system
# weave-net-xxxxx 이라는 이름의 Pod를 볼 수 있다.
kubectl logs -n kube-system weave-net-xxxxx
# weave-net-xxxxx의 로그를 확인 할 수 있다.
```



---

Q2. `**Troubleshooting Test 2:**` The same 2 tier application is having issues again. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

```shell
kubectl get pods -n kube-system -o wide
# kube-proxy-xxxxx 에서 CrashLoopBackOff 상태의 Pod을 확인 할 수 있다.

kubectl -n kube-system logs kube-proxy-xxxxx
# kube-proxy-xxxxx의 상세 로그를 볼 수 있다.

kubectl -n kube-system edit ds kube-proxy
#spec:
#  containers:
#  - command:
#	- /usr/local/bin/kube-proxy
#	- --config=/var/lib/kube-proxy/config.conf   <--- 올바른 설정

kubectl delete pods -n kube-system kube-proxy-xxxxxxx
# 상태가 변하지 않는다면 proxy pod를 삭제해 본다.(전부)
```

---

Q3. Troubleshooting Test 3:
The same 2 tier application is broken again. 
It must display a green web page on success.
Click on the app tab at the top of your terminal to view your application. 
It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

```shell
kubectl get pods -n kube-system -o wide
# coredns Pod의 상세내용을 확인한다.
kubectl describe pods - kube-system coredns-xxxxx-xxxxx
# 라벨을 확인해 보면 kube-dns 으로 되어 있다.
# Labels: k8s-app=kube-dns

kubectl -n kube-system get ep kube-dns
# Selector: k8s-app=core-dns (x)
# Selector: k8s-app=kube-dns (o) 으로 수정한다.
# coredns-xxxxx-xxxxx의 Pod 라벨 내용이 kube-dns이기 때문이다.

kubectl -n kube-system get svc kube-dns -o yaml > dns.yaml
vi dns.yaml
# selector.k8s-app의 value 값을 수정한다.

kubectl replace -f dns.yaml
kubectl -n kube-system get ep kube-dns
# 수정된 Selector 내용을 확인 할 수 있다.
```



