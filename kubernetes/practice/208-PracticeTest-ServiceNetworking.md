Practice Test - Service Networking

- https://uklabs.kodekloud.com/topic/practice-test-service-networking-2/

---

Q1. What network range are the nodes in the cluster part of?

```shell
root@controlplane:~# ip a | grep eth0 
14707: eth0@if14708: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1450 qdisc noqueue state UP group default 
    inet 10.0.129.3/24 brd 10.0.129.255 scope global eth0
```

- `10.0.129.0/24`

---

Q2. What is the range of IP addresses configured for PODs on this cluster?

```shell
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS    RESTARTS   AGE
weave-net-65pcv                        2/2     Running   0          58m
weave-net-xhtg2                        2/2     Running   1          59m


root@controlplane:~# kubectl -n kube-system logs weave-net-65pcv weave
INFO: 2021/08/31 01:29:43.453229 Command line options: map[conn-limit:200 datapath:datapath db-prefix:/weavedb/weave-net docker-api: expect-npc:true http-addr:127.0.0.1:6784 ipalloc-init:consensus=1 ipalloc-range:10.50.0.0/16 metrics-addr:0.0.0.0:6782 name:0e:3b:37:a2:0f:16 nickname:node01 no-dns:true no-masq-local:true port:6783]
INFO: 2021/08/31 01:29:43.453504 weave  2.8.1
INFO: 2021/08/31 01:29:45.448313 Bridge type is bridged_fastdp
INFO: 2021/08/31 01:29:45.448424 Communication between peers is unencrypted.
INFO: 2021/08/31 01:29:45.455516 Our name is 0e:3b:37:a2:0f:16(node01)
INFO: 2021/08/31 01:29:45.455602 Launch detected - using supplied peer list: [10.0.129.3]
INFO: 2021/08/31 01:29:45.455715 Using "no-masq-local" LocalRangeTracker
INFO: 2021/08/31 01:29:45.455743 Checking for pre-existing addresses on weave bridge
INFO: 2021/08/31 01:29:45.461520 [allocator 0e:3b:37:a2:0f:16] No valid persisted data
INFO: 2021/08/31 01:29:45.470567 [allocator 0e:3b:37:a2:0f:16] Initialising via deferred consensus
INFO: 2021/08/31 01:29:45.470720 Sniffing traffic on datapath (via ODP)
INFO: 2021/08/31 01:29:45.473611 ->[10.0.129.3:6783] attempting connection
INFO: 2021/08/31 01:29:45.477116 Listening for HTTP control messages on 127.0.0.1:6784
INFO: 2021/08/31 01:29:45.477157 Listening for metrics requests on 0.0.0.0:6782
INFO: 2021/08/31 01:29:45.541993 ->[10.0.129.3:6783|a6:ad:5d:5a:0c:85(controlplane)]: connection ready; using protocol version 2
INFO: 2021/08/31 01:29:45.543278 overlay_switch ->[a6:ad:5d:5a:0c:85(controlplane)] using fastdp
INFO: 2021/08/31 01:29:45.543462 ->[10.0.129.3:6783|a6:ad:5d:5a:0c:85(controlplane)]: connection added (new peer)
INFO: 2021/08/31 01:29:45.651448 ->[10.0.129.3:6783|a6:ad:5d:5a:0c:85(controlplane)]: connection fully established
INFO: 2021/08/31 01:29:45.653141 sleeve ->[10.0.129.3:6783|a6:ad:5d:5a:0c:85(controlplane)]: Effective MTU verified at 1388
INFO: 2021/08/31 01:29:46.296775 [kube-peers] Added myself to peer list &{[{a6:ad:5d:5a:0c:85 controlplane} {0e:3b:37:a2:0f:16 node01}]}
DEBU: 2021/08/31 01:29:46.305284 [kube-peers] Nodes that have disappeared: map[]
INFO: 2021/08/31 01:29:46.359978 adding entry 10.50.192.0/18 to weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:46.360027 added entry 10.50.192.0/18 to weaver-no-masq-local of 0
10.50.192.0
DEBU: 2021/08/31 01:29:46.844678 registering for updates for node delete events
INFO: 2021/08/31 01:29:50.781823 Discovered remote MAC ee:e8:5e:a5:7c:3b at a6:ad:5d:5a:0c:85(controlplane)
INFO: 2021/08/31 01:29:50.782009 Discovered remote MAC 8e:c3:b3:3e:7f:b8 at a6:ad:5d:5a:0c:85(controlplane)


root@controlplane:~# kubectl -n kube-system logs weave-net-xhtg2 weave
DEBU: 2021/08/31 01:29:21.160433 [kube-peers] Checking peer "a6:ad:5d:5a:0c:85" against list &{[]}
Peer not in list; removing persisted data
INFO: 2021/08/31 01:29:21.454318 Command line options: map[conn-limit:200 datapath:datapath db-prefix:/weavedb/weave-net docker-api: expect-npc:true http-addr:127.0.0.1:6784 ipalloc-init:consensus=0 ipalloc-range:10.50.0.0/16 metrics-addr:0.0.0.0:6782 name:a6:ad:5d:5a:0c:85 nickname:controlplane no-dns:true no-masq-local:true port:6783]
INFO: 2021/08/31 01:29:21.454390 weave  2.8.1
INFO: 2021/08/31 01:29:22.531790 Bridge type is bridged_fastdp
INFO: 2021/08/31 01:29:22.531839 Communication between peers is unencrypted.
INFO: 2021/08/31 01:29:22.535549 Our name is a6:ad:5d:5a:0c:85(controlplane)
INFO: 2021/08/31 01:29:22.535619 Launch detected - using supplied peer list: []
INFO: 2021/08/31 01:29:22.535978 Using "no-masq-local" LocalRangeTracker
INFO: 2021/08/31 01:29:22.536004 Checking for pre-existing addresses on weave bridge
INFO: 2021/08/31 01:29:22.548048 [allocator a6:ad:5d:5a:0c:85] No valid persisted data
INFO: 2021/08/31 01:29:22.553019 [allocator a6:ad:5d:5a:0c:85] Initialising via deferred consensus
INFO: 2021/08/31 01:29:22.553164 Sniffing traffic on datapath (via ODP)
INFO: 2021/08/31 01:29:22.557066 Listening for HTTP control messages on 127.0.0.1:6784
INFO: 2021/08/31 01:29:22.557157 Listening for metrics requests on 0.0.0.0:6782
INFO: 2021/08/31 01:29:22.669717 Error checking version: Get "https://checkpoint-api.weave.works/v1/check/weave-net?arch=amd64&flag_docker-version=none&flag_kernel-version=5.4.0-1051-gcp&os=linux&signature=kbtDD6zZr1X5Ac48tO8R7JvHhpDrXnDUCtGeFH95f30%3D&version=2.8.1": dial tcp: lookup checkpoint-api.weave.works on 10.96.0.10:53: write udp 172.25.0.23:60208->10.96.0.10:53: write: operation not permitted
INFO: 2021/08/31 01:29:23.393070 [kube-peers] Added myself to peer list &{[{a6:ad:5d:5a:0c:85 controlplane}]}
DEBU: 2021/08/31 01:29:23.401956 [kube-peers] Nodes that have disappeared: map[]
INFO: 2021/08/31 01:29:23.449855 Assuming quorum size of 1
INFO: 2021/08/31 01:29:23.450017 adding entry 10.50.0.0/16 to weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:23.450048 added entry 10.50.0.0/16 to weaver-no-masq-local of 0
10.50.0.1
DEBU: 2021/08/31 01:29:23.575875 registering for updates for node delete events
INFO: 2021/08/31 01:29:45.474688 ->[10.0.129.6:48119] connection accepted
INFO: 2021/08/31 01:29:45.475751 ->[10.0.129.6:48119|0e:3b:37:a2:0f:16(node01)]: connection ready; using protocol version 2
INFO: 2021/08/31 01:29:45.475891 overlay_switch ->[0e:3b:37:a2:0f:16(node01)] using fastdp
INFO: 2021/08/31 01:29:45.475954 ->[10.0.129.6:48119|0e:3b:37:a2:0f:16(node01)]: connection added (new peer)
INFO: 2021/08/31 01:29:45.576970 overlay_switch ->[0e:3b:37:a2:0f:16(node01)] using sleeve
INFO: 2021/08/31 01:29:45.577048 ->[10.0.129.6:48119|0e:3b:37:a2:0f:16(node01)]: connection fully established
INFO: 2021/08/31 01:29:45.578531 sleeve ->[10.0.129.6:6783|0e:3b:37:a2:0f:16(node01)]: Effective MTU verified at 1388
INFO: 2021/08/31 01:29:45.977514 overlay_switch ->[0e:3b:37:a2:0f:16(node01)] using fastdp
INFO: 2021/08/31 01:29:46.352931 adding entry 10.50.0.0/17 to weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:46.352968 added entry 10.50.0.0/17 to weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:46.354017 adding entry 10.50.128.0/18 to weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:46.354043 added entry 10.50.128.0/18 to weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:46.355062 deleting entry 10.50.0.0/16 from weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:46.355090 deleted entry 10.50.0.0/16 from weaver-no-masq-local of 0
INFO: 2021/08/31 01:29:50.781010 Discovered remote MAC 0e:3b:37:a2:0f:16 at 0e:3b:37:a2:0f:16(node01)
```

- `10.50.0.0/16`

---

Q3. What is the IP Range configured for the services within the cluster?

```shell
root@controlplane:~# cat /etc/kubernetes/manifests/kube-apiserver.yaml | grep cluster-ip-range
    - --service-cluster-ip-range=10.96.0.0/12
```

- `10.96.0.0/12`

---

Q4. How many kube-proxy pods are deployed in this cluster?

```shell
root@controlplane:~# kubectl get pods -n kube-system
NAME                                   READY   STATUS    RESTARTS   AGE
kube-proxy-8fjxk                       1/1     Running   0          62m
kube-proxy-n4zfd                       1/1     Running   0          62m
```

- `2`

---

Q5. What type of proxy is the kube-proxy configured to use?

```shell
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS    RESTARTS   AGE
kube-proxy-8fjxk                       1/1     Running   0          63m
kube-proxy-n4zfd                       1/1     Running   0          63m

root@controlplane:~# kubectl -n kube-system logs kube-proxy-8fjxk 
....
I0831 01:29:08.873762       1 server_others.go:185] Using iptables Proxier.
.....
```

- `iptables`

---

Q6. How does this Kubernetes cluster ensure that a kube-proxy pod runs on all nodes in the cluster?

```shell
root@controlplane:~# kubectl get ds -n kube-system
NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-proxy   2         2         2       2            2           kubernetes.io/os=linux   65m
weave-net    2         2         2       2            2           <none>                   65m
```

- `using daemonset`