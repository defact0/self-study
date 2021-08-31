Practice Test - Explore Kubernetes Environment

- https://uklabs.kodekloud.com/topic/practice-test-explore-environment-2/

---

Q1. How many nodes are part of this cluster?

- Including the master and worker nodes.

  ```shell
  root@controlplane:~# kubectl get nodes
  NAME           STATUS   ROLES                  AGE     VERSION
  controlplane   Ready    control-plane,master   4m2s    v1.20.0
  node01         Ready    <none>                 3m14s   v1.20.0
  ```

  - `2`

----

Q2. What is the Internal IP address of the `controlplane` node in this cluster?

```shell
root@controlplane:~# kubectl get nodes -o wide
NAME           STATUS   ROLES                  AGE     VERSION   INTERNAL-IP
controlplane   Ready    control-plane,master   6m12s   v1.20.0   10.52.144.3
node01         Ready    <none>                 5m24s   v1.20.0   10.52.144.6
```

- `10.52.144.3`

---

Q3. What is the network interface configured for cluster connectivity on the master node?

- node-to-node communication

```shell
# ----------------------------------------------------------
# controlplane 의 IP 주소 확인
root@controlplane:~# kubectl get nodes controlplane -o wide
NAME           STATUS   ROLES                  AGE     VERSION   INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION   CONTAINER-RUNTIME
controlplane   Ready    control-plane,master   7m56s   v1.20.0   10.52.144.3   <none>        Ubuntu 18.04.5 LTS   5.4.0-1051-gcp   docker://19.3.0

# ----------------------------------------------------------
# ip 명령을 사용하여 
root@controlplane:~# ip a | grep -B2 10.52.144.3
82: eth0@if83: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default 
    link/ether 02:42:0a:34:90:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
    inet 10.52.144.3/24 brd 10.52.144.255 scope global eth0
```

- `eth0`

---

Q4. What is the MAC address of the interface on the master node?

```shell
root@controlplane:~# ip link show eth0
82: eth0@if83: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP mode DEFAULT group default 
    link/ether 02:42:0a:34:90:03 brd ff:ff:ff:ff:ff:ff link-netnsid 0
```

- `02:42:0a:34:90:03`

---

Q5. What is the IP address assigned to `node01`?

```shell
root@controlplane:~# kubectl get nodes -o wide
NAME           STATUS   ROLES                  AGE     VERSION   INTERNAL-IP
controlplane   Ready    control-plane,master   6m12s   v1.20.0   10.52.144.3
node01         Ready    <none>                 5m24s   v1.20.0   10.52.144.6
```

- `10.52.144.6`

---

Q6. What is the MAC address assigned to `node01`?

```shell
# Run the command: arp node01 on the controlplane node.
root@controlplane:~# arp node01
Address                  HWtype  HWaddress           Flags Mask            Iface
10.52.144.5              ether   02:42:0a:34:90:04   C                     eth0
```

- `02:42:0a:34:90:04`

---

Q7. We use Docker as our container runtime. What is the interface/bridge created by Docker on this host?

```shell
root@controlplane:~# ip link
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
2: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default 
    link/ether 02:42:aa:49:57:02 brd ff:ff:ff:ff:ff:ff
```

- `docker0`

---

Q8. What is the state of the interface `docker0`?

```shell
root@controlplane:~# ip link show docker0
2: docker0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DEFAULT group default 
    link/ether 02:42:aa:49:57:02 brd ff:ff:ff:ff:ff:ff
```

- `DOWN`

---

Q9. If you were to ping google from the master node, which route does it take?

- What is the IP address of the Default Gateway?

```shell
root@controlplane:~# ip route show default
default via 172.17.0.1 dev eth1 
```

- `172.17.0.1`

---

Q10. What is the port the `kube-scheduler` is listening on in the controlplane node?

```shell
root@controlplane:~# netstat -nplt | grep scheduler
tcp        0      0 127.0.0.1:10259         0.0.0.0:*               LISTEN      4056/kube-scheduler
```

- `10259`

---

Q11. Notice that ETCD is listening on two ports. Which of these have more client connections established?

```shell
netstat -anp | grep etcd
```

- `2379`

---

Q12. Correct! That's because 2379 is the port of ETCD to which all control plane components connect to. 2380 is only for etcd peer-to-peer connectivity. When you have multiple master nodes. In this case we don't.

- ok
  - 2379는 모든 컨트롤 플레인 구성 요소가 연결되는 ETCD의 포트이기 때문입니다. 
  - 2380은 etcd 피어 투 피어 연결 전용입니다. 

