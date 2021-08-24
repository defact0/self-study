Practice Test - ReplicaSets

- https://uklabs.kodekloud.com/topic/practice-test-replicasets-2/

---

Q1. How many PODs exist on the system?

- In the current(default) namespace.

```shell
root@controlplane:~# kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   4m24s
root@controlplane:~# 
```

- 시스템에 Pod는 존재하지 않는다.

---

Q2. How many ReplicaSets exist on the system?

- In the current(default) namespace.
- Q1에서 확인하였을 때 `ReplicaSets ` 역시 존재하지 않는다.

---

Q3. How about now? How many ReplicaSets do you see?

- We just made a few changes!

```shell
# 테스트 환경이 변하였기 때문에 재 확인을 한다.
# replicasets를 써도 되고 축약해서 rs를 명령해도 된다.
root@controlplane:~# kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       76s
```

- ReplicaSets 은 `new-replica-set` 1개가 있음을 확인 할 수 있다.

---

Q4. How many PODs are DESIRED in the `new-replica-set`?

- Q3 내용을 보면 `DESIRED `는 4개 인 것을 확인 할 수 있다.

---

Q5. What is the image used to create the pods in the `new-replica-set`?

```shell
# Pod 리스트를 확인 한다.
root@controlplane:~# kubectl get pod
NAME                    READY   STATUS             RESTARTS   AGE
new-replica-set-55thj   0/1     ImagePullBackOff   0          5m38s
new-replica-set-pf6kw   0/1     ImagePullBackOff   0          5m38s
new-replica-set-v44lx   0/1     ImagePullBackOff   0          5m38s
new-replica-set-whszw   0/1     ImagePullBackOff   0          5m38s

# new-replica-set와 관련된 Pod 중 하나를 describe 한다.
root@controlplane:~# kubectl describe pod new-replica-set-55thj | grep -i image
    Image:         busybox777
    Image ID:      
      Reason:       ImagePullBackOff
  Normal   Pulling    4m34s (x4 over 5m54s)  kubelet            Pulling image "busybox777"
  Warning  Failed     4m33s (x4 over 5m53s)  kubelet            Failed to pull image "busybox777": rpc error: code = Unknown desc = Error response from daemon: pull access denied for busybox777, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
  Warning  Failed     4m33s (x4 over 5m53s)  kubelet            Error: ErrImagePull
  Warning  Failed     4m10s (x7 over 5m52s)  kubelet            Error: ImagePullBackOff
  Normal   BackOff    41s (x22 over 5m52s)   kubelet            Back-off pulling image "busybox777"
root@controlplane:~# 
```

- 사용된 image는 `busybox777` 인 것을 확인 할 수 있다.

---

Q6. How many PODs are READY in the `new-replica-set`?

- READY 상태 인것은 존재하지 않는다.

---

Q7. Why do you think the PODs are not ready?

```shell
"busybox777": rpc error: code = Unknown desc = Error response from daemon: pull access denied for busybox777, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
```

- Q5에서 작업 중에 확인할 수 있는데 그 이유는
   `The image BUSYBOX777 doesn't exist` 이다.

---

Q8. Delete any one of the 4 PODs.

```shell
# 4개의 Pod 중에 아무거나 1개만 지운다.
root@controlplane:~# kubectl get pod
NAME                    READY   STATUS             RESTARTS   AGE
new-replica-set-55thj   0/1     ErrImagePull       0          10m
new-replica-set-pf6kw   0/1     ImagePullBackOff   0          10m
new-replica-set-v44lx   0/1     ImagePullBackOff   0          10m
new-replica-set-whszw   0/1     ImagePullBackOff   0          10m

# Pod 1개를 지정하여 삭제
root@controlplane:~# kubectl delete pod new-replica-set-55thj 
pod "new-replica-set-55thj" deleted
```

---

Q9. How many PODs exist now?

```shell
root@controlplane:~# kubectl get pod
NAME                    READY   STATUS             RESTARTS   AGE
new-replica-set-gk9w8   0/1     ErrImagePull       0          61s
new-replica-set-pf6kw   0/1     ImagePullBackOff   0          12m
new-replica-set-v44lx   0/1     ImagePullBackOff   0          12m
new-replica-set-whszw   0/1     ImagePullBackOff   0          12m
root@controlplane:~# 
```

- 아까 지웠던 `new-replica-set-55thj` Pod 대신 새로 생성된 Pod 이 있어 4개의 Pod이 존재하는 상태

---

Q10. Why are there still 4 PODs, even after you deleted one?

- `ReplicaSet ensures that desired number of PODs always run`
  - ReplicaSet 특성(desired state) 때문에 Pod를 지워도 계속 Pod 4개가 유지된다.

---

Q11. Create a ReplicaSet using the `replicaset-definition-1.yaml` file located at `/root/`.

- There is an issue with the file, so try to fix it.
  - Name: replicaset-1

```shell
# replicaset-definition-1.yaml 파일을 확인한다.
root@controlplane:~# ls
replicaset-definition-1.yaml  replicaset-definition-2.yaml  sample.yaml

# replicaset-definition-1.yaml를 apply 시도하지만 오류가 발생한다.
root@controlplane:~# kubectl apply -f replicaset-definition-1.yaml 
error: unable to recognize "replicaset-definition-1.yaml": no matches for kind "ReplicaSet" in version "v1"

# replicaset-definition-1.yaml 를 수정한다.
root@controlplane:~# vi replicaset-definition-1.yaml
  # apiVersion: v1
  apiVersion: apps/v1
  
# replicaset-definition-1.yaml를 apply 다시 시도한다.
root@controlplane:~# kubectl apply -f replicaset-definition-1.yaml 
replicaset.apps/replicaset-1 created
```

---

Q12. Fix the issue in the `replicaset-definition-2.yaml` file and create a `ReplicaSet` using it.

- This file is located at `/root/`.
- Name: replicaset-2

```shell
# replicaset-definition-2.yaml 파일 확인
root@controlplane:~# ls
replicaset-definition-1.yaml  replicaset-definition-2.yaml  sample.yaml
root@controlplane:~# 

# replicaset-definition-2.yaml apply 시도
root@controlplane:~# kubectl apply -f replicaset-definition-2.yaml 
The ReplicaSet "replicaset-2" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"tier":"nginx"}: `selector` does not match template `labels`
root@controlplane:~# 


# replicaset-definition-2.yaml 수정
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-2
spec:
  replicas: 2
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
#       tier: nginx
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx

# 정상 생성 확인
root@controlplane:~# kubectl apply -f replicaset-definition-2.yaml 
replicaset.apps/replicaset-2 created
root@controlplane:~# kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       54m
replicaset-1      2         2         2       11m
replicaset-2      2         2         2       35s
root@controlplane:~# 
```

---

Q13. Delete the two newly created ReplicaSets - `replicaset-1` and `replicaset-2

- Delete: replicaset-2
- Delete: replicaset-1

```shell
root@controlplane:~# kubectl delete rs replicaset-1
replicaset.apps "replicaset-1" deleted
root@controlplane:~# kubectl delete rs replicaset-2
replicaset.apps "replicaset-2" deleted
root@controlplane:~# 
root@controlplane:~# kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       55m
```

---

Q14. Fix the original replica set `new-replica-set` to use the correct `busybox` image.

- Either delete and recreate the ReplicaSet or Update the existing ReplicaSet and then delete all PODs, so new ones with the correct image will be created.
  - Replicas: 4

```shell
root@controlplane:~# kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       57m

# Image가 busybox777 인 것을 확인할 수 있다.
root@controlplane:~# kubectl describe rs new-replica-set 
Name:         new-replica-set
Namespace:    default
Selector:     name=busybox-pod
Labels:       <none>
Annotations:  <none>
Replicas:     4 current / 4 desired
Pods Status:  0 Running / 4 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  name=busybox-pod
  Containers:
   busybox-container:
    Image:      busybox777
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      echo Hello Kubernetes! && sleep 3600
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age   From                   Message
  ----    ------            ----  ----                   -------
  Normal  SuccessfulCreate  57m   replicaset-controller  Created pod: new-replica-set-pf6kw
  Normal  SuccessfulCreate  57m   replicaset-controller  Created pod: new-replica-set-55thj
  Normal  SuccessfulCreate  57m   replicaset-controller  Created pod: new-replica-set-v44lx
  Normal  SuccessfulCreate  57m   replicaset-controller  Created pod: new-replica-set-whszw
  Normal  SuccessfulCreate  46m   replicaset-controller  Created pod: new-replica-set-gk9w8
root@controlplane:~# 

# new-replica-set 수정
root@controlplane:~# kubectl edit rs new-replica-set

# image 값 수정
    spec:
      containers:
      - command:
        - sh
        - -c
        - echo Hello Kubernetes! && sleep 3600
#        image: busybox777
        image: busybox
        

root@controlplane:~# kubectl get pod
NAME                    READY   STATUS             RESTARTS   AGE
new-replica-set-b66q7   0/1     ImagePullBackOff   0          5m46s
new-replica-set-bnv85   0/1     ImagePullBackOff   0          4m56s
new-replica-set-mgtrc   0/1     ImagePullBackOff   0          5m46s
new-replica-set-wgxrv   0/1     ImagePullBackOff   0          5m46s

root@controlplane:~# kubectl delete pod new-replica-set-b66q7 
pod "new-replica-set-b66q7" deleted
root@controlplane:~# kubectl delete pod new-replica-set-bnv85 
pod "new-replica-set-bnv85" deleted
root@controlplane:~# kubectl delete pod new-replica-set-mgtrc 
pod "new-replica-set-mgtrc" deleted
root@controlplane:~# kubectl delete pod new-replica-set-wgxrv 
pod "new-replica-set-wgxrv" deleted

root@controlplane:~# kubectl get pod
NAME                    READY   STATUS    RESTARTS   AGE
new-replica-set-5s5rl   1/1     Running   0          84s
new-replica-set-5wsfk   1/1     Running   0          3m45s
new-replica-set-jpqj9   1/1     Running   0          3m25s
new-replica-set-srmbf   1/1     Running   0          2m18s
root@controlplane:~# 
```

---

Q15. Scale the ReplicaSet to 5 PODs.

- Use `kubectl scale` command or edit the replicaset using `kubectl edit replicaset`.
  - Replicas: 5

```shell
# root@controlplane:~# kubectl get rs
# NAME              DESIRED   CURRENT   READY   AGE
# new-replica-set   4         4         0       57m

# 기존에 있던 replicas 갯수를 수정해라
root@controlplane:~# kubectl scale replicaset --replicas=5 new-replica-set 
replicaset.apps/new-replica-set scaled

root@controlplane:~# kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   5         5         5       15m
```

---

Q16. Now scale the ReplicaSet down to 2 PODs.

- Use the `kubectl scale` command or edit the replicaset using `kubectl edit replicaset`.
  - Replicas: 2

```shell
# root@controlplane:~# kubectl get rs
# NAME              DESIRED   CURRENT   READY   AGE
# new-replica-set   5         5         5       15m

# replicas 개수를 2로 설정 한다.
root@controlplane:~# kubectl scale replicaset --replicas=2 new-replica-set 
replicaset.apps/new-replica-set scaled

# 2개로 설정된 것을 확인 할 수 있다.
root@controlplane:~# kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   2         2         2       20m
root@controlplane:~# 

```





