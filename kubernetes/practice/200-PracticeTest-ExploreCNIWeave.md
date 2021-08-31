Practice Test - Explore CNI Weave

- https://uklabs.kodekloud.com/topic/practice-test-cni-weave-2/

---

Q1. Inspect the kubelet service and identify the network plugin configured for Kubernetes.

```shell
root@controlplane:~# ps -aux | grep kubelet | grep --color network-plugin= 
root      4782  0.0  0.0 4003348 99088 ?       Ssl  00:47   0:32 /usr/bin/kubelet --bootstrap-kubeconfig=/etc/kubernetes/bootstrap-kubelet.conf --kubeconfig=/etc/kubernetes/kubelet.conf --config=/var/lib/kubelet/config.yaml --network-plugin=cni --pod-infra-container-image=k8s.gcr.io/pause:3.2
```

- `cni`

---

Q2. What is the path configured with all binaries of CNI supported plugins?

- `/opt/cni/bin`

---

Q3. Identify which of the below plugins is not available in the list of available CNI plugins on this host?

```shell
root@controlplane:~# ls /opt/cni/bin
bandwidth  bridge  dhcp  firewall  flannel  host-device  host-local  ipvlan  loopback  macvlan  portmap  ptp  sbr  static  tuning  vlan
```

- 문제 보기에 있던 `CISCO` 는 cni에서 지원목록에 없다.

---

Q4. What is the CNI plugin configured to be used on this kubernetes cluster?

```shell
root@controlplane:~# ls /etc/cni/net.d/
10-flannel.conflist
```

- `flannel`

---

Q5. What binary executable file will be run by kubelet after a container and its associated namespace are created.

```shell
root@controlplane:~# cat /etc/cni/net.d/10-flannel.conflist
{
  "name": "cbr0",
  "cniVersion": "0.3.1",
  "plugins": [
    {
      "type": "flannel",
      "delegate": {
        "hairpinMode": true,
        "isDefaultGateway": true
      }
    },
    {
      "type": "portmap",
      "capabilities": {
        "portMappings": true
      }
    }
  ]
}
```

- `flannel`



