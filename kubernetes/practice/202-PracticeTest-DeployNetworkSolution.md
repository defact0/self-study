Practice Test - Deploy Network Solution

- https://uklabs.kodekloud.com/topic/practice-test-deploy-network-solution-2/

---

Q1. In this practice test we will install `weave-net` POD networking solution to the cluster. Let us first inspect the setup.

We have deployed an application called `app` in the default namespace. What is the state of the pod?

- `Not Running`

```shell
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-74ff55c5b-6fnt5                1/1     Running   0          49m
coredns-74ff55c5b-bmqp9                1/1     Running   0          49m
etcd-controlplane                      1/1     Running   0          49m
kube-apiserver-controlplane            1/1     Running   0          49m
kube-controller-manager-controlplane   1/1     Running   0          49m
kube-proxy-srg7p                       1/1     Running   0          49m
kube-scheduler-controlplane            1/1     Running   0          49m
```

---

Q2. Inspect why the POD is not running

- `No Network Configured`

---

Q3. Deploy `weave-net` networking solution to the cluster.

Replace the default IP address and subnet of `weave-net` to the `10.32.0.0/16`. Please check the official weave installation and configuration guide which is available at the top right panel.

```shell
# ---------------------------
# weave-net 설치
root@controlplane:~# kubectl apply -f "https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d '\n')&env.IPALLOC_RANGE=10.32.0.0/16"
serviceaccount/weave-net created
clusterrole.rbac.authorization.k8s.io/weave-net created
clusterrolebinding.rbac.authorization.k8s.io/weave-net created
role.rbac.authorization.k8s.io/weave-net created
rolebinding.rbac.authorization.k8s.io/weave-net created
daemonset.apps/weave-net created

# ---------------------------
# weave-net 설치 확인
root@controlplane:~# kubectl get po -n kube-system | grep weave
weave-net-m9fp9                        2/2     Running   0          24s
```

