Practice Test - Deploy a Kubernetes Cluster using Kubeadm

- https://uklabs.kodekloud.com/topic/practice-test-cluster-installation-using-kubeadm/

---

Q1. Install the `kubeadm` package on the `controlplane` and `node01`.
Use the exact version of `1.21.0-00`

- kubeadm installed on controlplane ?
- Kubeadm installed on worker node01

- 아래 링크 사이트를 참고하여 작업한다.
  https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/

---

Q2. What is the version of `kubelet` installed?

```shell
root@controlplane:~# kubelet --version
Kubernetes v1.22.1
```

- `v1.22.1`

---

Q3. How many nodes are part of kubernetes cluster currently?
Are you able to run `kubectl get nodes`?

- `0`

---

Q4. Lets now bootstrap a `kubernetes` cluster using `kubeadm`.

The latest version of Kubernetes will be installed.

- `ok`

---

Q5. Initialize `Control Plane Node (Master Node)`. Use the following options:

1. `apiserver-advertise-address` - Use the IP address allocated to eth0 on the controlplane node
2. `apiserver-cert-extra-sans` - Set it to `controlplane`
3. `pod-network-cidr` - Set to `10.244.0.0/16`

Once done, set up the `default kubeconfig` file and wait for node to be part of the cluster.

```shell
root@controlplane:~# kubeadm init

...

root@controlplane:~# mkdir -p $HOME/.kube
root@controlplane:~#   sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
root@controlplane:~#   sudo chown $(id -u):$(id -g) $HOME/.kube/config
root@controlplane:~# 
```

---

Q6. Generate a kubeadm join token
Or copy the one that was generated by `kubeadm init` command

- `ok`

---

Q7. Join `node01` to the cluster using the join token

```shell
root@controlplane:~# kubeadm token create --print-join-command
...
root@node01:~# kubeadm join 10.2.223.3:6443 --token 50pj4l.0cy7m2e1jlfmvnif --discovery-token-ca-cert-hash sha256:fb08c01c782ef1d1ad0b643b56c9edd6a864b87cff56e7ff35713cd666659ff4
```

- `Check`

---

Q8. Install a Network Plugin. As a default, we will go with `flannel`
Refer to the official documentation for the procedure

```shell
kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
```
