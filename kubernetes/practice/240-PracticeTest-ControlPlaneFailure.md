Practice Test - Control Plane Failure

- https://uklabs.kodekloud.com/topic/practice-test-control-plane-failure-2/

---

Q1. The cluster is broken again. We tried deploying an application but it's not working. Troubleshoot and fix the issue.

- Start looking at the deployments.

```shell
root@controlplane:~# kubectl get deployments.apps 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
app    0/1     1            0           2m
root@controlplane:~# kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
app-586bddbc54-c99gd   0/1     Pending   0          2m12s
```

- Pod의 상태가 `Pending` 이다.

```shell
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS             RESTARTS   AGE
coredns-74ff55c5b-jnw5g                1/1     Running            0          10m
coredns-74ff55c5b-qt52q                1/1     Running            0          10m
etcd-controlplane                      1/1     Running            0          10m
kube-apiserver-controlplane            1/1     Running            0          10m
kube-controller-manager-controlplane   1/1     Running            0          10m
kube-flannel-ds-6c5fl                  1/1     Running            0          10m
kube-proxy-2pj9s                       1/1     Running            0          10m
kube-scheduler-controlplane            0/1     CrashLoopBackOff   4          3m2s
```

- kube-system 네임스페이스를 확인해 보니 스케쥴러가 문제가 있는 것을 확인 할 수 있다.

```shell
root@controlplane:~# kubectl -n kube-system describe pod kube-scheduler-controlplane 
Name:                 kube-scheduler-controlplane
Namespace:            kube-system
....
Events:
  Type     Reason          Age                    From     Message
  ----     ------          ----                   ----     -------
  Normal   SandboxChanged  3m58s                  kubelet  Pod sandbox changed, it will be killed and re-created.
  Warning  Failed          3m57s                  kubelet  Error: Error response from daemon: Conflict. The container name "/k8s_kube-scheduler_kube-scheduler-controlplane_kube-system_c16cbe912154274ec7a48147f6950a2f_0" is already in use by container "85a5b88f34df2165206ba96161637dc58b8a3496c8f45322df29e85d1bf58972". You have to remove (or rename) that container to be able to reuse that name.
  Normal   Pulled          3m11s (x6 over 3m59s)  kubelet  Container image "k8s.gcr.io/kube-scheduler:v1.20.0" already present on machine
  Normal   Created         3m11s (x5 over 3m59s)  kubelet  Created container kube-scheduler
  Warning  Failed          3m11s (x5 over 3m58s)  kubelet  Error: failed to start container "kube-scheduler": Error response from daemon: OCI runtime create failed: container_linux.go:367: starting container process caused: exec: "kube-schedulerrrr": executable file not found in $PATH: unknown
  Warning  BackOff         2m33s (x7 over 3m54s)  kubelet  Back-off restarting failed container
```

- kube-scheduler-controlplane의 이벤트 로그를 확인해 보면
  - starting container process caused: exec: "kube-schedulerrrr" 이라는 것을 확인 할 수 있다.
  - 그 이어서 PATH라는 환경 변수에 까지 영향이 발생한 것을 알 수 있다.
    executable file not found in $PATH: unknown

```shell
# ------------------------------------------------------
# /etc/kubernetes/manifests/kube-scheduler.yaml 에서
# kube-schedulerrrr -> kube-scheduler 으로 수정한다.
root@controlplane:~# cd /etc/kubernetes/manifests/
root@controlplane:/etc/kubernetes/manifests# ls
etcd.yaml  kube-apiserver.yaml  kube-controller-manager.yaml  kube-scheduler.yaml
root@controlplane:/etc/kubernetes/manifests# vi kube-scheduler.yaml

# ---------------------------------
# pod의 상태가 running 으로 정상이다.
root@controlplane:/etc/kubernetes/manifests# kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
app-586bddbc54-c99gd   1/1     Running   0          8m32s
```

---

Q2. Scale the deployment `app` to 2 pods.

- Scale Deployment to 2 PODs

```shell
root@controlplane:~# kubectl get deployments.apps
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
app    1/1     1            1           10m

root@controlplane:~# kubectl scale deployment app --replicas=2
deployment.apps/app scaled

root@controlplane:~# kubectl get deployments.apps
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
app    1/2     1            1           12m
```

---

Q3. Even though the deployment was scaled to 2, the number of `PODs` does not seem to increase. Investigate and fix the issue.

- Inspect the component responsible for managing `deployments` and `replicasets`.
- Fix issue
- Wait for deployment to actually scale

```shell
# -----------------------------------------------------
# kube-system 네임스페이스를 확인한다.
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS             RESTARTS   AGE
kube-controller-manager-controlplane   0/1     CrashLoopBackOff   5          3m40s


root@controlplane:~# kubectl -n kube-system logs kube-controller-manager-controlplane 
Flag --port has been deprecated, see --secure-port instead.
I0829 23:18:41.875837       1 serving.go:331] Generated self-signed cert in-memory
stat /etc/kubernetes/controller-manager-XXXX.conf: no such file or directory

root@controlplane:~# vi /etc/kubernetes/manifests/kube-controller-manager.yaml
# 아래와 같은 내용을 확인하였고 이것을 올바르게 수정해야 한다.
# --kubeconfig=/etc/kubernetes/controller-manager-XXXX.conf
# 해당 디렉토리 경로에 파일이름을 보면 controller-manager.conf 으로 수정해야 함을 알 수 있다.
# root@controlplane:~# ls /etc/kubernetes/ -la
# -rw------- 1 root root 5603 Aug 29 22:57 controller-manager.conf

# -----------------------------------------------------
# kube-system 네임스페이스를 확인한다.
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS    RESTARTS   AGE
kube-controller-manager-controlplane   1/1     Running   0          104s

# -----------------------------------------------------
# replicas=2 설정한 상태로 정상 적용된 것을 확인 할 수 있다.
root@controlplane:~# kubectl get pod
NAME                   READY   STATUS    RESTARTS   AGE
app-586bddbc54-8vrb8   1/1     Running   0          102s
app-586bddbc54-c99gd   1/1     Running   0          20m
root@controlplane:~# kubectl get deployments.apps 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
app    2/2     2            2           20m
```

----

Q4. Something is wrong with scaling again. We just tried scaling the deployment to 3 replicas. But it's not happening.

- Fix Issue
- Wait for deployment to actually scale

```shell
# -----------------------------------------------------
# kube-controller-manager-controlplane에 문제가 발생 했음을 확인 할 수 있다.
root@controlplane:~# kubectl -n kube-system get pod
NAME                                   READY   STATUS             RESTARTS   AGE
kube-controller-manager-controlplane   0/1     CrashLoopBackOff   2          60s

# -----------------------------------------------------
# 로그에서 CA 파일을 찾을 수 없다라고 한다.
root@controlplane:~# kubectl -n kube-system logs kube-controller-manager-controlplane
Flag --port has been deprecated, see --secure-port instead.
I0829 23:28:33.746905       1 serving.go:331] Generated self-signed cert in-memory
unable to load client CA file "/etc/kubernetes/pki/ca.crt": open /etc/kubernetes/pki/ca.crt: no such file or directory

# -----------------------------------------------------
# kube-controller-manager.yaml 을 수정한다.
root@controlplane:~# vi /etc/kubernetes/manifests/kube-controller-manager.yaml

# k8s-certs 이름의 volumes에서 path 경로가 이상한 것을 알 수 있다.
# /etc/kubernetes/pki/ 으로 수정한다.
#  - hostPath:
#      path: /etc/kubernetes/WRONG-PKI-DIRECTORY
#      type: DirectoryOrCreate
#    name: k8s-certs

# -----------------------------------------------------
# deployment to 3 replicas 상태를 확인 할 수 있다.
root@controlplane:~# kubectl get all
NAME                       READY   STATUS    RESTARTS   AGE
pod/app-586bddbc54-8vrb8   1/1     Running   0          10m
pod/app-586bddbc54-bn4xg   1/1     Running   0          71s
pod/app-586bddbc54-c99gd   1/1     Running   0          29m

NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app   3/3     3            3           29m

NAME                             DESIRED   CURRENT   READY   AGE
replicaset.apps/app-586bddbc54   3         3         3       29m
```

