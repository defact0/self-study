Practice Test - Networking Weave

- https://uklabs.kodekloud.com/topic/practice-test-networking-weave-2/

---

Q1. How many Nodes are part of this cluster?

```shell
root@controlplane:~# kubectl get nodes
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   57m   v1.20.0
node01         Ready    <none>                 56m   v1.20.0
```

- `2`

---

Q2. What is the Networking Solution used by this cluster?

```shell
root@controlplane:~# ls /etc/cni/net.d/
10-weave.conflist
```

- `weave`

---

Q3. How many weave agents/peers are deployed in this cluster?

```shell
root@controlplane:~# kubectl get pods -n kube-system
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-74ff55c5b-2m55d                1/1     Running   0          58m
coredns-74ff55c5b-gvvwf                1/1     Running   0          58m
etcd-controlplane                      1/1     Running   0          58m
kube-apiserver-controlplane            1/1     Running   0          58m
kube-controller-manager-controlplane   1/1     Running   0          58m
kube-proxy-6ckzd                       1/1     Running   0          58m
kube-proxy-9wkbk                       1/1     Running   0          57m
kube-scheduler-controlplane            1/1     Running   0          58m
weave-net-gxrb7                        2/2     Running   1          58m
weave-net-phfcj                        2/2     Running   0          57m
```

- `2`

---

Q4. On which nodes are the weave peers present?

```shell
root@controlplane:~# kubectl get pods -n kube-system -o wide
NAME                                   READY   STATUS    NODE        
coredns-74ff55c5b-2m55d                1/1     Running   controlplane
coredns-74ff55c5b-gvvwf                1/1     Running   controlplane
etcd-controlplane                      1/1     Running   controlplane
kube-apiserver-controlplane            1/1     Running   controlplane
kube-controller-manager-controlplane   1/1     Running   controlplane
kube-proxy-6ckzd                       1/1     Running   controlplane
kube-proxy-9wkbk                       1/1     Running   node01      
kube-scheduler-controlplane            1/1     Running   controlplane
weave-net-gxrb7                        2/2     Running   controlplane  <---- 여기
weave-net-phfcj                        2/2     Running   node01        <---- 여기
```

- `One on every node`

---

Q5. Identify the name of the bridge network/interface created by weave on each node

```shell
root@controlplane:~# ip link
....
5: weave: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1376 qdisc noqueue state UP mode DEFAULT group default qlen 1000
    link/ether 82:93:0e:02:66:9a brd ff:ff:ff:ff:ff:ff
```

- `weave`

---

Q6. What is the POD IP address range configured by weave?

```shell
root@controlplane:~# ip addr show weave
5: weave: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1376 qdisc noqueue state UP group default qlen 1000
    link/ether 82:93:0e:02:66:9a brd ff:ff:ff:ff:ff:ff
    inet 10.50.0.1/16 brd 10.50.255.255 scope global weave
       valid_lft forever preferred_lft forever
```

- `10.X.X.X`

---

Q7. What is the default gateway configured on the PODs scheduled on node01?

```shell
root@controlplane:~# ip r
default via 172.17.0.1 dev eth1 
...
10.50.0.0/16 dev weave proto kernel scope link src 10.50.0.1 <--- 여기
```

- `10.50.192.0`

