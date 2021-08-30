Practice Test - Worker Node Failure

- https://uklabs.kodekloud.com/topic/practice-test-worker-node-failure-2/

---

Q1. Fix the broken cluster

- Fix node01

```shell
# ------------------------------------------------------------
# node01 상태가 NotReady 이다.
root@controlplane:~# kubectl get nodes 
NAME           STATUS     ROLES                  AGE   VERSION
controlplane   Ready      control-plane,master   37m   v1.20.0
node01         NotReady   <none>                 37m   v1.20.0

# ------------------------------------------------------------
# node01 으로 접속
root@controlplane:~# ssh node01

# ------------------------------------------------------------
# kubelet 서비스가 inactive (dead) 상태이다.
root@node01:~# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: inactive (dead) since Mon 2021-08-30 00:07:46 UTC; 5min ago
   
# ------------------------------------------------------------
# kubelet 서비스가 재기동 이후 정상상태 확인
root@node01:~# systemctl restart kubelet 
root@node01:~# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Mon 2021-08-30 00:13:56 UTC; 7s ago
   
# ------------------------------------------------------------
# controlplane으로 돌아가 node01 상태를 확인
root@node01:~# exit
logout
Connection to node01 closed.
root@controlplane:~# kubectl get nodes 
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   43m   v1.20.0
node01         Ready    <none>                 43m   v1.20.0
```



---

Q2. The cluster is broken again. Investigate and fix the issue.

- Fix cluster

```shell
# ------------------------------------------------------------
# 노드의 상태를 확인한다.
root@controlplane:~# kubectl get nodes 
NAME           STATUS     ROLES                  AGE   VERSION
controlplane   Ready      control-plane,master   45m   v1.20.0
node01         NotReady   <none>                 45m   v1.20.0

# ------------------------------------------------------------
# node01로 접속
root@controlplane:~# ssh node01
Last login: Mon Aug 30 00:09:31 2021 from 10.40.237.7

# ------------------------------------------------------------
# kubelet의 상태를 확인한다.
root@node01:~# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: activating (auto-restart) (Result: exit-code) since Mon 2021-08-30 00:17:20
   
# ------------------------------------------------------------
# journalctl를 활용하여 로그를 확인한다.
# shift + G 키를 눌러 맨 아래로 이동 합니다.
root@node01:~# journalctl -u kubelet
-- Logs begin at Sun 2021-08-29 23:30:11 UTC, end at Mon 2021-08-30 00:19:04 UTC. --
...
unable to load client CA file /etc/kubernetes/pki/WRONG-CA-FILE.crt: open /etc/kubernetes/pki/WRONG-CA-FILE.crt: no such file or directory
# CA 파일이 잘못 되었음을 확인 할 수 있다.

# ------------------------------------------------------------
# /etc/kubernetes/pki 경로에 파일 확인
root@node01:~# ls /etc/kubernetes/pki/ -la
total 12
drwxr-xr-x 2 root root 4096 Aug 29 23:31 .
drwxr-xr-x 1 root root 4096 Aug 29 23:31 ..
-rw-r--r-- 1 root root 1066 Aug 29 23:31 ca.crt

# ------------------------------------------------------------
# kubelet/config.yaml 파일 수정
root@node01:~# vi /var/lib/kubelet/config.yaml
# clientCAFile: /etc/kubernetes/pki/WRONG-CA-FILE.crt 를
# clientCAFile: /etc/kubernetes/pki/ca.crt 로 수정한다.


# ------------------------------------------------------------
# 데몬 재시작
systemctl daemon-reload
systemctl restart kubelet
systemctl status kubelet

# ------------------------------------------------------------
# controlplane으로 돌아가 node01 상태를 확인
root@node01:~# exit
logout
Connection to node01 closed.
root@controlplane:~# kubectl get nodes 
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   43m   v1.20.0
node01         Ready    <none>                 43m   v1.20.0
```

---

Q3. The cluster is broken again. Investigate and fix the issue.

```shell
root@controlplane:~# kubectl get node
NAME           STATUS     ROLES                  AGE   VERSION
controlplane   Ready      control-plane,master   61m   v1.20.0
node01         NotReady   <none>                 61m   v1.20.0


root@controlplane:~# ssh node01
Last login: Mon Aug 30 00:17:14 2021 from 10.40.237.7


root@node01:~# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/lib/systemd/system/kubelet.service; enabled; vendor preset: enabled)
  Drop-In: /etc/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: active (running) since Mon 2021-08-30 00:32:30 UTC; 29s ago


root@node01:~# journalctl -u kubelet.service
# shift + g
# "node01" with API server: Post "https://controlplane:6553/api/v1/nodes": dial tcp 10.40.237.5:6553: connect: connection refused

# -----------------------------------------------------------------------
# node01에서 로그를 봤을 때 포트가 6553 인데 controlplane의 포트는 6443 이다.
# node01에서 관련 포트를 수정해야 한다.
root@node01:~# exit
logout
Connection to node01 closed.
root@controlplane:~# kubectl cluster-info 
Kubernetes control plane is running at https://controlplane:6443
KubeDNS is running at https://controlplane:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

# -----------------------------------------------------------------------
# kubelet.conf 를 수정
root@controlplane:~# ssh node01
Last login: Mon Aug 30 00:32:45 2021 from 10.40.237.7
root@node01:~# vi /etc/kubernetes/kubelet.conf


# ------------------------------------------------------------
# 데몬 재시작
systemctl daemon-reload
systemctl restart kubelet
systemctl status kubelet

# ------------------------------------------------------------
# controlplane으로 돌아가 node01 상태를 확인
root@node01:~# exit
logout
Connection to node01 closed.
root@controlplane:~# kubectl get nodes 
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   43m   v1.20.0
node01         Ready    <none>                 43m   v1.20.0

```

