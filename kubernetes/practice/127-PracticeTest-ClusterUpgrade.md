Practice Test - Cluster Upgrade

- https://uklabs.kodekloud.com/topic/practice-test-cluster-upgrade-process-2/

---

Q1. This lab tests your skills on **upgrading a kubernetes cluster**. We have a production cluster with applications running on it. Let us explore the setup first.

- What is the current version of the cluster?

```shell
root@controlplane:~# kubectl get nodes
NAME           STATUS   ROLES    AGE   VERSION
controlplane   Ready    master   16m   v1.19.0
node01         Ready    <none>   15m   v1.19.0
```

- `v1.19.0`

---

Q2. How many nodes are part of this cluster?

- Including master and worker nodes

```shell
root@controlplane:~# kubectl get nodes
NAME           STATUS   ROLES    AGE   VERSION
controlplane   Ready    master   16m   v1.19.0
node01         Ready    <none>   15m   v1.19.0
```

- 2

---

Q3. How many nodes can host workloads in this cluster?

- Inspect the applications and taints set on the nodes.

```shell
root@controlplane:~# kubectl describe nodes  controlplane | grep -i taint
Taints:             <none>
root@controlplane:~# kubectl describe nodes  node01 | grep -i taint
Taints:             <none>
```

- 2

---

Q4. How many applications are hosted on the cluster?

- Count the number of deployments.

```shell
root@controlplane:~# kubectl get deployments.apps
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
blue   5/5     5            5           2m58s
```

- 1

---

Q5. What nodes are the pods hosted on?

```shell
root@controlplane:~# kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
blue-746c87566d-88hsv   1/1     Running   0          3m23s   10.244.0.4   controlplane   <none>           <none>
blue-746c87566d-9qqd5   1/1     Running   0          3m23s   10.244.0.5   controlplane   <none>           <none>
blue-746c87566d-b77qn   1/1     Running   0          3m23s   10.244.1.2   node01         <none>           <none>
blue-746c87566d-jpzml   1/1     Running   0          3m23s   10.244.1.4   node01         <none>           <none>
blue-746c87566d-wh24j   1/1     Running   0          3m23s   10.244.1.5   node01         <none>           <none>
simple-webapp-1         1/1     Running   0          3m23s   10.244.1.3   node01         <none>           <none>
```

- `controlplane,node01`

---

Q6. You are tasked to upgrade the cluster. User's accessing the applications must not be impacted. And you cannot provision new VMs. What strategy would you use to upgrade the cluster?

- `Upgrade one node at a time while moving the workloads to the other`

---

Q7. What is the latest stable version available for upgrade?

- Use the `kubeadm` tool

```shell
root@controlplane:~# kubeadm upgrade plan
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
...
Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       AVAILABLE
kubelet     2 x v1.19.0   v1.19.14

Upgrade to the latest version in the v1.19 series:

COMPONENT                 CURRENT   AVAILABLE
kube-apiserver            v1.19.0   v1.19.14
kube-controller-manager   v1.19.0   v1.19.14
kube-scheduler            v1.19.0   v1.19.14
kube-proxy                v1.19.0   v1.19.14
CoreDNS                   1.7.0     1.7.0
etcd                      3.4.9-1   3.4.9-1

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.19.14
...
```

- `v1.19.14` 으로 업그레이드 가능하다.

---

Q8. We will be upgrading the master node first. Drain the master node of workloads and mark it `UnSchedulable`

- Master Node: SchedulingDisabled

```shell
root@controlplane:~# kubectl drain controlplane --ignore-daemonsets
node/controlplane cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/kube-flannel-ds-q8wgm, kube-system/kube-proxy-bmns5
evicting pod kube-system/coredns-f9fd979d6-65slz
evicting pod default/blue-746c87566d-88hsv
evicting pod kube-system/coredns-f9fd979d6-czbhn
evicting pod default/blue-746c87566d-9qqd5
pod/blue-746c87566d-88hsv evicted
pod/blue-746c87566d-9qqd5 evicted
pod/coredns-f9fd979d6-65slz evicted
pod/coredns-f9fd979d6-czbhn evicted
node/controlplane evicted
```

---

Q9. Upgrade the `controlplane` components to exact version `v1.20.0`

- Upgrade kubeadm tool (if not already), then the master components, and finally the kubelet. Practice referring to the kubernetes documentation page. Note: While upgrading kubelet, if you hit dependency issue while running the `apt-get upgrade kubelet` command, use the `apt install kubelet=1.20.0-00` command instead
  - 
    controlplane Upgraded to v1.20.0
  - controlplane Kubelet Upgraded to v1.20.0

```shell
#
# apt update
#
root@controlplane:~# apt update
Get:2 https://download.docker.com/linux/ubuntu bionic InRelease [64.4 kB]
Get:3 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
...

#
# install kubeadm=1.20.0-00
#
root@controlplane:~# apt install kubeadm=1.20.0-00
Reading package lists... Done
Building dependency tree       
Reading state information... Done
....


#
# kubeadm upgrade apply v1.20.0
#
root@controlplane:~# kubeadm upgrade apply v1.20.0
[upgrade/config] Making sure the configuration is correct:
...


#
# apt install kubelet=1.20.0-00
#
root@controlplane:~# apt install kubelet=1.20.0-00
Reading package lists... Done
Building dependency tree       
Reading state information... Done
...


#
# restart kubelet
#
root@controlplane:~# systemctl restart kubelet



#
# controlplane v1.20.0
#
root@controlplane:~# kubectl get nodes
NAME           STATUS                     ROLES                  AGE   VERSION
controlplane   Ready,SchedulingDisabled   control-plane,master   34m   v1.20.0
node01         Ready                      <none>                 33m   v1.19.0
```

---

Q10. Mark the `controlplane` node as "Schedulable" again

- 
  Master Node: Ready & Schedulable

```shell
root@controlplane:~# kubectl uncordon controlplane
node/controlplane uncordoned
```

---

Q11. Next is the worker node. `Drain` the worker node of the workloads and mark it `UnSchedulable`

- Worker node: Unschedulable

```shell
root@controlplane:~# kubectl drain node01 --ignore-daemonsets
node/node01 cordoned
error: unable to drain node "node01", aborting command...

There are pending nodes to be drained:
 node01
error: cannot delete Pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet (use --force to override): default/simple-webapp-1
```

---

Q12. Upgrade the worker node to the exact version `v1.20.0`

- 
  Worker Node Upgraded to v1.20.0
- Worker Node Ready

```shell
#
# node01 으로 접속
# 
root@controlplane:~# ssh node01
Welcome to Ubuntu 18.04.5 LTS (GNU/Linux 5.4.0-1051-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

#
# apt update
#
root@node01:~# apt update
Get:1 http://security.ubuntu.com/ubuntu bionic-security InRelease [88.7 kB]
Get:3 https://download.docker.com/linux/ubuntu bionic InRelease [64.4 kB]   ...

#
# nstall kubeadm=1.20.0-00
#
root@node01:~# apt install kubeadm=1.20.0-00
Reading package lists... Done
Building dependency tree       
Reading state information... Done

#
# kubeadm upgrade node
#
root@node01:~# kubeadm upgrade node
[upgrade] Reading configuration from the cluster...

#
# apt install kubelet=1.20.0-00
#
root@node01:~# apt install kubelet=1.20.0-00
Reading package lists... Done
Building dependency tree       
Reading state information... Done

#
# systemctl restart kubelet
#
root@node01:~# systemctl restart kubelet

#
# node01 업데이트 결과 확인
#
root@node01:~# exit
logout
Connection to node01 closed.
root@controlplane:~# kubectl get nodes
NAME           STATUS                     ROLES                  AGE   VERSION
controlplane   Ready                      control-plane,master   40m   v1.20.0
node01         Ready,SchedulingDisabled   <none>                 39m   v1.20.0
```

---

Q13. Remove the restriction and mark the worker node as schedulable again.

- Worker Node: Schedulable

```shell
root@controlplane:~# kubectl uncordon node01
node/node01 uncordoned
```





