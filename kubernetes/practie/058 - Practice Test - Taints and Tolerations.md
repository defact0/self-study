Practice Test - Taints and Tolerations

- https://uklabs.kodekloud.com/topic/practice-test-taints-and-tolerations-2/

---

Q1. How many `nodes` exist on the system?

- Including the `controlplane` node.

```shell
root@controlplane:~# kubectl get node
NAME           STATUS   ROLES                  AGE     VERSION
controlplane   Ready    control-plane,master   6m1s    v1.20.0
node01         Ready    <none>                 5m18s   v1.20.0
```

- 2개의 node가 존재한다

---

Q2. Do any taints exist on `node01` node?

```shell
root@controlplane:~# kubectl describe node node01 | grep -i taint 
Taints:             <none>
```

- NO

---

Q3. Create a taint on `node01` with key of `spray`, value of `mortein` and effect of `NoSchedule`

- 
  Key = spray
- Value = mortein
- Effect = NoSchedule

```shell
# taint 설정
root@controlplane:~# kubectl taint node node01 spray=mortein:NoSchedule
node/node01 tainted

# 설정 확인
root@controlplane:~# kubectl describe node node01 | grep -i taint 
Taints:             spray=mortein:NoSchedule
```

---

Q4. Create a new pod with the `NGINX` image and pod name as `mosquito`.

- 
  Image name: nginx

```shell
# pod 생성
root@controlplane:~# kubectl run mosquito --image=nginx                
pod/mosquito created

# pod 생성 확인
root@controlplane:~# kubectl get pod
NAME       READY   STATUS    RESTARTS   AGE
mosquito   0/1     Pending   0          21s
```

---

Q5. What is the state of the POD?

- `Pending` 상태이다.

---

Q6. Why do you think the pod is in a pending state?

```shell
root@controlplane:~# kubectl describe pod mosquito 
Name:         mosquito
Namespace:    default
Priority:     0
Node:         <none>
Labels:       run=mosquito
Annotations:  <none>
Status:       Pending
IP:           
IPs:          <none>
Containers:
  mosquito:
    Image:        nginx
    Port:         <none>
    Host Port:    <none>
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-lbzvr (ro)
Conditions:
  Type           Status
  PodScheduled   False 
Volumes:
  default-token-lbzvr:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-lbzvr
    Optional:    false
QoS Class:       BestEffort
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason            Age                From               Message
  ----     ------            ----               ----               -------
  Warning  FailedScheduling  28s (x3 over 97s)  default-scheduler  0/2 nodes are available: 1 node(s) had taint {node-role.kubernetes.io/master: }, that the pod didn't tolerate, 1 node(s) had taint {spray: mortein}, that the pod didn't tolerate.
root@controlplane:~# 
```

- `POD Mosquito cannot tolerate taint Mortein` 의 이유로 Pod가 Pending 상태이다.

---

Q7. Create another pod named `bee` with the `NGINX` image, which has a toleration set to the taint `mortein`.

- Image name: nginx
- Key: spray
- Value: mortein
- Effect: NoSchedule
- Status: Running

```shell
# yaml 파일 생성
kubectl run bee --image=nginx --dry-run=client -o yaml > bee.yaml

# yaml 옵션 보기
kubectl explain pod --recursive | less
# tolerations 항목 참고 하기
root@controlplane:~# kubectl explain pod --recursive | grep -A5 tolerations
      tolerations       <[]Object>
         effect <string>
         key    <string>
         operator       <string>
         tolerationSeconds      <integer>
         value  <string>
         
# bee.yaml 수정하기
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: bee
  name: bee
spec:
  containers:
  - image: nginx
    name: bee
    resources: {}
  tolerations:
  - effect: NoSchedule
    key: spray
    operator: Equal
    value: mortein

# Pod 생성
root@controlplane:~# kubectl apply -f bee.yaml 
pod/bee created

root@controlplane:~# kubectl get pod -w
NAME       READY   STATUS    RESTARTS   AGE
bee        1/1     Running   0          22s
mosquito   0/1     Pending   0          11m
```

---

Q8. Notice the `bee` pod was scheduled on node `node01` despite the taint.

```shell
root@controlplane:~# kubectl get pod -o wide
NAME       READY   STATUS    RESTARTS   AGE    IP           NODE     NOMINATED NODE   READINESS GATES
bee        1/1     Running   0          103s   10.244.1.2   node01   <none>           <none>
mosquito   0/1     Pending   0          13m    <none>       <none>   <none>           <none>
```

- 확인했으면 ok 버튼을 누르고 9번 문제로 이동한다.

---

Q9. Do you see any taints on `controlplane` node?

```shell
root@controlplane:~# kubectl get node
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   33m   v1.20.0
node01         Ready    <none>                 32m   v1.20.0

root@controlplane:~# kubectl describe nodes controlplane | grep -i taint
Taints:             node-role.kubernetes.io/master:NoSchedule
root@controlplane:~# 

```

- Taints 부분을 확인하면 NoSchedule으로 설정되어 있다.  `Yes - NoSchedule`를 선택

---

Q10. Remove the taint on `controlplane`, which currently has the taint effect of `NoSchedule`.

- Node name: controlplane

```shell
# 현재 상태는 taint 설정이 되어 있다.
root@controlplane:~# kubectl describe nodes controlplane | grep -i taint
Taints:             node-role.kubernetes.io/master:NoSchedule

# 마지막에 (-)를 붙이면 remove 하는 작업을 수행한다.
root@controlplane:~# kubectl taint node controlplane node-role.kubernetes.io/master:NoSchedule-
node/controlplane untainted

# 설정을 재 확인한다.
root@controlplane:~# kubectl describe nodes controlplane | grep -i taint
Taints:             <none>
```

---

Q11. What is the state of the pod `mosquito` now?

```shell
root@controlplane:~# kubectl get pod
NAME       READY   STATUS    RESTARTS   AGE
bee        1/1     Running   0          16m
mosquito   1/1     Running   0          28m
```

- `Running` 상태이다.

---

Q12. Which node is the POD `mosquito` on now?

```shell
root@controlplane:~# kubectl get pod -o wide 
NAME       READY   STATUS    RESTARTS   AGE   IP           NODE        
bee        1/1     Running   0          17m   10.244.1.2   node01      
mosquito   1/1     Running   0          28m   10.244.0.4   controlplane
```

- `controlplane`에 있다.



