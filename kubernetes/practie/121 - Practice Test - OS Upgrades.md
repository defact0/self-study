Practice Test - OS Upgrades

- https://uklabs.kodekloud.com/topic/practice-test-os-upgrades-2/

---

Q1. Let us explore the environment first. How many nodes do you see in the cluster?

```shell
root@controlplane:~# kubectl get nodes
NAME           STATUS   ROLES                  AGE     VERSION
controlplane   Ready    control-plane,master   5m17s   v1.20.0
node01         Ready    <none>                 4m37s   v1.20.0
```

- 2

---

Q2. How many applications do you see hosted on the cluster?

```shell
root@controlplane:~# kubectl get deployments
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
blue   3/3     3            3           17s
```

- 1

---

Q3. Which nodes are the applications hosted on?

```shell
root@controlplane:~# kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP           NODE     NOMINATED NODE   READINESS GATES
blue-746c87566d-7fgpn   1/1     Running   0          52s   10.244.1.3   node01   <none>           <none>
blue-746c87566d-p2w47   1/1     Running   0          52s   10.244.1.4   node01   <none>           <none>
blue-746c87566d-xh69m   1/1     Running   0          52s   10.244.1.2   node01   <none>           <none>
```

- `node01`

---

Q4. We need to take `node01` out for maintenance. Empty the node of all applications and mark it unschedulable.

- Node node01 Unschedulable
- Pods evicted from node01

```shell
root@controlplane:~# kubectl drain node01 --ignore-daemonsets
node/node01 cordoned
WARNING: ignoring DaemonSet-managed Pods: kube-system/kube-flannel-ds-tmcvg, kube-system/kube-proxy-4tfwj
evicting pod default/blue-746c87566d-xh69m
evicting pod default/blue-746c87566d-7fgpn
evicting pod default/blue-746c87566d-p2w47
pod/blue-746c87566d-xh69m evicted
pod/blue-746c87566d-p2w47 evicted
pod/blue-746c87566d-7fgpn evicted
node/node01 evicted
```

---

Q5. What nodes are the apps on now?

```shell
root@controlplane:~# kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
blue-746c87566d-rw2c6   1/1     Running   0          46s   10.244.0.5   controlplane   <none>           <none>
blue-746c87566d-vxkmv   1/1     Running   0          46s   10.244.0.6   controlplane   <none>           <none>
blue-746c87566d-zqzk8   1/1     Running   0          46s   10.244.0.4   controlplane   <none>           <none>
```

- `controlplane`
  - Q4에서 node01에 `drain` 명령을 내렸기 때문에 해당 결과가 나오는 것이다.

---

Q6. The maintenance tasks have been completed. Configure the node `node01` to be schedulable again.

- 
  Node01 is Schedulable

```shell
root@controlplane:~# kubectl uncordon node01
node/node01 uncordoned
```

- Q4에서 node01에 `drain` 설정을 원래 상태로 복귀

---

Q7. How many pods are scheduled on `node01` now?

```shell
root@controlplane:~# kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE    IP           NODE           NOMINATED NODE   READINESS GATES
blue-746c87566d-rw2c6   1/1     Running   0          4m4s   10.244.0.5   controlplane   <none>           <none>
blue-746c87566d-vxkmv   1/1     Running   0          4m4s   10.244.0.6   controlplane   <none>           <none>
blue-746c87566d-zqzk8   1/1     Running   0          4m4s   10.244.0.4   controlplane   <none>           <none>
```

- node01에 있는 Pod는 0개이다.

---

Q8. Why are there no pods on `node01`?

- Only when new pods are created they will be scheduled

---

Q9. Why are the pods placed on the `controlplane` node?

```shell
root@controlplane:~# kubectl describe node controlplane | grep -i  taint
Taints:             <none>
```

- controlplane node does not have any taints

---

Q10. Time travelling to the next maintenance window…

- ok

---

Q11. We need to carry out a maintenance activity on `node01` again. Try draining the node again using the same command as before: `kubectl drain node01 --ignore-daemonsets`

Did that work?

- No

```shell
root@controlplane:~# kubectl drain node01 --ignore-daemonsets
node/node01 cordoned
error: unable to drain node "node01", aborting command...

There are pending nodes to be drained:
 node01
error: cannot delete Pods not managed by ReplicationController, ReplicaSet, Job, DaemonSet or StatefulSet (use --force to override): default/hr-app
```

---

Q12. Why did the drain command fail on node01? It worked the first time!

- there is a pod in node01 which is not part of a replicaset

---

Q13. What is the name of the POD hosted on node01 that is not part of a replicaset?

```shell
root@controlplane:~# kubectl get pods -o wide
NAME                    READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
blue-746c87566d-rw2c6   1/1     Running   0          12m     10.244.0.5   controlplane   <none>           <none>
blue-746c87566d-vxkmv   1/1     Running   0          12m     10.244.0.6   controlplane   <none>           <none>
blue-746c87566d-zqzk8   1/1     Running   0          12m     10.244.0.4   controlplane   <none>           <none>
hr-app                  1/1     Running   0          5m45s   10.244.1.5   node01         <none>           <none>
```

- hr-app

---

Q14. What would happen to `hr-app` if `node01` is drained forcefully?

> A forceful drain of the node will delete any pod that is not part of a replicaset.

- hr-app will be lost forever

---

Q15. Oops! We did not want to do that! `hr-app` is a critical application that should not be destroyed. We have now reverted back to the previous state and re-deployed `hr-app` as a deployment.

- ok

---

Q16. `hr-app` is a critical app and we do not want it to be removed and we do not want to schedule any more pods on node01.
Mark `node01` as `unschedulable` so that no new pods are scheduled on this node.

- Make sure that `hr-app` is not affected.
  - Node01 Unschedulable
  - hr-app still running on node01?

```shell
root@controlplane:~# kubectl cordon node01
node/node01 cordoned
```



