Practice Test - Static Pods

- https://uklabs.kodekloud.com/topic/practice-test-static-pods-2/

---

Q1. How many static pods exist in this cluster in all namespaces?

```shell
root@controlplane:~# kubectl get pods --all-namespaces 
NAMESPACE     NAME                                   READY   STATUS    RESTARTS   AGE
kube-system   coredns-74ff55c5b-7lp9s                1/1     Running   0          12m
kube-system   coredns-74ff55c5b-j724t                1/1     Running   0          12m
kube-system   etcd-controlplane                      1/1     Running   0          12m
kube-system   kube-apiserver-controlplane            1/1     Running   0          12m
kube-system   kube-controller-manager-controlplane   1/1     Running   0          12m
kube-system   kube-flannel-ds-9ztz9                  1/1     Running   0          12m
kube-system   kube-flannel-ds-tf4tz                  1/1     Running   0          12m
kube-system   kube-proxy-442sx                       1/1     Running   0          12m
kube-system   kube-proxy-jzl5q                       1/1     Running   0          12m
kube-system   kube-scheduler-controlplane            1/1     Running   0          12m

root@controlplane:~# kubectl get pods --all-namespaces | grep controlplane
kube-system   etcd-controlplane                      1/1     Running   0          13m
kube-system   kube-apiserver-controlplane            1/1     Running   0          13m
kube-system   kube-controller-manager-controlplane   1/1     Running   0          13m
kube-system   kube-scheduler-controlplane            1/1     Running   0          13m

root@controlplane:~# kubectl get pods --all-namespaces | grep controlplane | wc -l
4
```

- 4개가 있다.

---

Q2. Which of the below components is NOT deployed as a static pod?

```shell
root@controlplane:~# kubectl get pods --all-namespaces | grep controlplane
kube-system   etcd-controlplane                      1/1     Running   0          13m
kube-system   kube-apiserver-controlplane            1/1     Running   0          13m
kube-system   kube-controller-manager-controlplane   1/1     Running   0          13m
kube-system   kube-scheduler-controlplane            1/1     Running   0          13m
```

- `coredns`

---

Q3. Which of the below components is NOT deployed as a static POD?

```shell
root@controlplane:~# kubectl get pods --all-namespaces | grep controlplane
kube-system   etcd-controlplane                      1/1     Running   0          13m
kube-system   kube-apiserver-controlplane            1/1     Running   0          13m
kube-system   kube-controller-manager-controlplane   1/1     Running   0          13m
kube-system   kube-scheduler-controlplane            1/1     Running   0          13m
```

- `kube-proxy`

---

Q4. On which nodes are the static pods created currently?

```shell
root@controlplane:~# kubectl get pods --all-namespaces -o wide | grep controlplane
kube-system   coredns-74ff55c5b-7lp9s                Running   10.244.0.2     controlplane
kube-system   coredns-74ff55c5b-j724t                Running   10.244.0.3     controlplane
kube-system   etcd-controlplane                      Running   10.36.104.12   controlplane
kube-system   kube-apiserver-controlplane            Running   10.36.104.12   controlplane
kube-system   kube-controller-manager-controlplane   Running   10.36.104.12   controlplane
kube-system   kube-flannel-ds-9ztz9                  Running   10.36.104.12   controlplane
kube-system   kube-proxy-442sx                       Running   10.36.104.12   controlplane
kube-system   kube-scheduler-controlplane            Running   10.36.104.12   controlplane
```

- `controlplane`
  - `-o wide` 옵션을 추가하여 어떤 node에 만들어 졌는지 알 수 있다.

---

Q5. What is the path of the directory holding the static pod definition files?

```shell
root@controlplane:~# ps -ef | grep kubernetes | grep config.yaml
root      4835     1  0 22:14 ?        00:01:57 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.2

root@controlplane:~# grep -i static /var/lib/kubelet/config.yaml
staticPodPath: /etc/kubernetes/manifests
```

- `/etc/kubernetes/manifests`

---

Q6. How many pod definition files are present in the manifests folder?

```shell
root@controlplane:/etc/kubernetes/manifests# ls
etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml

root@controlplane:/etc/kubernetes/manifests# ls | wc -l
4
```

- `/etc/kubernetes/manifests` 에 파일이 4개가 존재한다.

---

Q7. What is the docker image used to deploy the kube-api server as a static pod?

```shell
root@controlplane:~# cd /etc/kubernetes/manifests
root@controlplane:/etc/kubernetes/manifests# grep -i image kube-apiserver.yaml 
    image: k8s.gcr.io/kube-apiserver:v1.20.0
    imagePullPolicy: IfNotPresent
```

- `k8s.gcr.io/kube-apiserver:v1.20.0`

---

Q8. Create a static pod named `static-busybox` that uses the `busybox` image and the command `sleep 1000`

- Name: static-busybox
- Image: busybox

```shell
root@controlplane:~# kubectl run --restart=Never --image=busybox static-busybox --dry-run=client -o yaml --command -- sleep 1000 > /etc/kubernetes/manifests/static-busybox.yaml
```

- 자동 생성된다.

---

Q9. Edit the image on the static pod to use `busybox:1.28.4`

```shell
root@controlplane:~# kubectl run --restart=Never --image=busybox:1.28.4 static-busybox --dry-run=client -o yaml --command -- sleep 1000 > /etc/kubernetes/manifests/static-busybox.yaml
```

- 자동 수정된다.

---

Q10. We just created a new static pod named **static-greenbox**. Find it and delete it.

- This question is a bit tricky. But if you use the knowledge you gained in the previous questions in this lab, you should be able to find the answer to it.
- Static pod deleted

```shell
#
# static-greenbox-node01 이라는 Pod가 있는 것을 확인 할 수 있다.
#
root@controlplane:~# kubectl get pod
NAME                          READY   STATUS    RESTARTS   AGE
static-busybox-controlplane   1/1     Running   0          114s
static-greenbox-node01        1/1     Running   0          57s

#
# -o wide 옵션을 넣으면 확장된 정보를 볼 수 있다.
#
root@controlplane:~# kubectl get pod -o wide
NAME                          READY   STATUS    IP           NODE        
static-busybox-controlplane   1/1     Running   10.244.0.5   controlplane
static-greenbox-node01        1/1     Running   10.244.1.4   node01    

#
# node01 으로 접속
#
root@controlplane:~# ssh node01
#
# kubelet의 프로세스 상세 정보를 출력한다.
#
root@node01:~# ps -ef | grep /usr/bin/kubelet 
root     30988     1  0 23:16 ?        00:00:07 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.2
root     33461 33338  0 23:19 pts/0    00:00:00 grep --color=auto /usr/bin/kubelet

#
# kubelet/config.yaml의 staticpod를 출력한다.
#
root@node01:~# grep -i staticpod /var/lib/kubelet/config.yaml
staticPodPath: /etc/just-to-mess-with-you

#
# staticpod 삭제
#
root@node01:~# cd /etc/just-to-mess-with-you
root@node01:/etc/just-to-mess-with-you# ls
greenbox.yaml
root@node01:/etc/just-to-mess-with-you# rm -rf greenbox.yaml 
root@node01:/etc/just-to-mess-with-you# ls
root@node01:/etc/just-to-mess-with-you# 

#
# 최종확인
#  - static-greenbox-node01가 사라져 있다.
#
root@node01:/etc/just-to-mess-with-you# exit
logout
Connection to node01 closed.
root@controlplane:~# kubectl get pod -o wide
NAME                          READY   STATUS    IP           NODE 
static-busybox-controlplane   1/1     Running   10.244.0.5   controlplane
```
