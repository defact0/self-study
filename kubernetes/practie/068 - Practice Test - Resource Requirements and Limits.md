Practice Test - Resource Requirements and Limits

- https://uklabs.kodekloud.com/topic/practice-test-resource-limits-2/

---

Q1. A pod called `rabbit` is deployed. Identify the CPU requirements set on the Pod

- in the current(default) namespace

```shell
root@controlplane:~# kubectl get pod
NAME     READY   STATUS             RESTARTS   AGE
rabbit   0/1     CrashLoopBackOff   2          57s

root@controlplane:~# kubectl describe pod rabbit 
Name:         rabbit
Namespace:    default
..
Containers:
  cpu-stress:
...
    Limits:
      cpu:  2
    Requests:
      cpu:        1
...
```

- `Requests` 부분을 보면 CPU 1 개가 설정되어 있다.

---

Q2. Delete the `rabbit` Pod.

- Once deleted, wait for the pod to fully terminate.
  - Delete Pod rabbit

```shell
root@controlplane:~# kubectl delete pod rabbit 
pod "rabbit" deleted

root@controlplane:~# kubectl get pod
No resources found in default namespace.
```

---

Q3. Another pod called `elephant` has been deployed in the default namespace. It fails to get to a running state. Inspect this pod and identify the `Reason` why it is not running.

```shell
root@controlplane:~# kubectl get pod
NAME       READY   STATUS             RESTARTS   AGE
elephant   0/1     CrashLoopBackOff   1          17s

root@controlplane:~# kubectl describe pod elephant 
Name:         elephant
...
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
...
```

- `Last State.Reason = OOMKilled` 인 것을 확인 할 수 있다.
  - `State.Reason`의 값을 보고 오판하면 안된다.

---

Q4. The status `OOMKilled` indicates that it is failing because the pod ran out of memory. Identify the memory limit set on the POD.

```shell
root@controlplane:~# kubectl get pod
NAME       READY   STATUS             RESTARTS   AGE
elephant   0/1     CrashLoopBackOff   2          30s

root@controlplane:~# kubectl describe pod elephant 
Name:         elephant
Namespace:    default
Priority:     0
Node:         controlplane/10.20.0.9
Start Time:   Sun, 22 Aug 2021 13:28:48 +0000
Labels:       <none>
Annotations:  <none>
Status:       Running
IP:           10.244.0.5
IPs:
  IP:  10.244.0.5
Containers:
  mem-stress:
    Container ID:  docker://5ce3439598f21d3960ed26d190c52dbce430b48b858bc376feefd63da51d3408
    Image:         polinux/stress
    Image ID:      docker-pullable://polinux/stress@sha256:b6144f84f9c15dac80deb48d3a646b55c7043ab1d83ea0a697c09097aaad21aa
    Port:          <none>
    Host Port:     <none>
    Command:
      stress
    Args:
      --vm
      1
      --vm-bytes
      15M
      --vm-hang
      1
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    1
      Started:      Sun, 22 Aug 2021 13:29:10 +0000
      Finished:     Sun, 22 Aug 2021 13:29:10 +0000
    Ready:          False
    Restart Count:  2
    Limits:
      memory:  10Mi
    Requests:
      memory:     5Mi
    Environment:  <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from default-token-hmj4c (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             False 
  ContainersReady   False 
  PodScheduled      True 
Volumes:
  default-token-hmj4c:
    Type:        Secret (a volume populated by a Secret)
    SecretName:  default-token-hmj4c
    Optional:    false
QoS Class:       Burstable
Node-Selectors:  <none>
Tolerations:     node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                 node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  42s                default-scheduler  Successfully assigned default/elephant to controlplane
  Normal   Pulled     37s                kubelet            Successfully pulled image "polinux/stress" in 3.25458762s
  Normal   Pulled     35s                kubelet            Successfully pulled image "polinux/stress" in 223.698622ms
  Normal   Pulling    20s (x3 over 40s)  kubelet            Pulling image "polinux/stress"
  Normal   Created    20s (x3 over 37s)  kubelet            Created container mem-stress
  Normal   Started    20s (x3 over 37s)  kubelet            Started container mem-stress
  Normal   Pulled     20s                kubelet            Successfully pulled image "polinux/stress" in 201.92456ms
  Warning  BackOff    2s (x5 over 33s)   kubelet            Back-off restarting failed container
```

- `ok` 버튼을 눌러 넘어간다.

---

Q5. The `elephant` pod runs a process that consume 15Mi of memory. Increase the limit of the `elephant` pod to 20Mi.

- Delete and recreate the pod if required. Do not modify anything other than the required fields.
  - Pod Name: elephant
  - Image Name: polinux/stress
  - Memory Limit: 20Mi

```shell
# elephant 포트를 yaml 파일로 저장한다.
root@controlplane:~# kubectl get pod elephant -o yaml > pod.yaml
root@controlplane:~# vi pod.yaml

# limit.memory = 10 -> 20Mi 으로 수정
    image: polinux/stress
    imagePullPolicy: Always
    name: mem-stress
    resources:
      limits:
        memory: 20Mi
        
# elephant 포드 삭제
root@controlplane:~# kubectl delete pod elephant 
pod "elephant" deleted

# 수정한 yaml 파일 적용
root@controlplane:~# kubectl apply -f pod.yaml 
pod/elephant created

# 생성 확인
root@controlplane:~# kubectl get pod -w
NAME       READY   STATUS    RESTARTS   AGE
elephant   1/1     Running   0          9s
```

---

Q6. Inspect the status of POD. Make sure it's running

- `ok` 버튼을 누르고 다음으로 넘어간다.

---

Q7. Delete the `elephant` Pod.

- Once deleted, wait for the pod to fully terminate.

```shell
root@controlplane:~# kubectl delete pod elephant 
pod "elephant" deleted

root@controlplane:~# kubectl get pod
No resources found in default namespace.
```



