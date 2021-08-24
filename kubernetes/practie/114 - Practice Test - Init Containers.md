Practice Test - Init Containers

- https://uklabs.kodekloud.com/topic/practice-test-init-containers-2/

---

Q1. Identify the pod that has an `initContainer` configured.

```shell
root@controlplane:~# kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
blue    1/1     Running   0          108s
green   2/2     Running   0          108s
red     1/1     Running   0          108s

#
# Init Containers
#
root@controlplane:~# kubectl describe pod blue | grep -i "init"
Init Containers:
  init-myservice:
  Initialized       True 
  Normal  Created    3m35s  kubelet            Created container init-myservice
  Normal  Started    3m35s  kubelet            Started container init-myservice
  
#
# No Init Containers
#
root@controlplane:~# kubectl describe pod green | grep -i "init"
  Initialized       True 
root@controlplane:~# kubectl describe pod red | grep -i "init"
  Initialized       True 
root@controlplane:~# 
```

- `blue` Pod가 Init Containers 설정이 되어 있다.

---

Q2. What is the image used by the `initContainer` on the `blue` pod?

```sshell
root@controlplane:~# kubectl describe pod blue | grep -i "image"
    Image:         busybox
    Image ID:      docker-pullable://busybox@sha256:...
    Image:         busybox:1.28
    Image ID:      docker-pullable://busybox@sha256:...
  Normal  Pulling    7m4s   kubelet            Pulling image "busybox"
  Normal  Pulled     7m3s   kubelet            Successfully pulled image "busybox" in 1.62232283s
  Normal  Pulled     6m56s  kubelet            Container image "busybox:1.28" already present on machine
```

- 컨테이너 이미지는 `busybox`를 사용한다.

---

Q3. What is the state of the `initContainer` on pod `blue`

```shell
root@controlplane:~# kubectl describe pod blue                  
Name:         blue
...
Init Containers:
  init-myservice:
    ...
    State:          Terminated
```

- `Init Containers.State` 상태를 보면 `Terminated` 인 것을 확인 할 수 있다.

---

Q4. Why is the `initContainer` terminated? What is the reason?

```shell
Init Containers:
  init-myservice:
...
    State:          Terminated
      Reason:       Completed
      Exit Code:    0
```

- `Reason`이 Completed 으로 출력되기 때문에 문제의 정답은
  - `The process completed successfully`

---

Q5. We just created a new app named `purple`. How many `initContainers` does it have?

```shell
root@controlplane:~# kubectl describe pod purple 

Init Containers:
  warm-up-1:
  ...
  warm-up-2:
  ...
```

- `Init Containers`는 `warm-up-1`와 `warm-up-2` 두개가 있다.

---

Q6. What is the state of the POD?

```shell
root@controlplane:~# kubectl describe pod purple 
Name:         purple
...
Status:       Pending
```

- `Status: Pending`

---

Q7. How long after the creation of the POD will the application come up and be available to users?

```shell
# kubectl describe pod purple 을 통해
# warm-up-1, 2의 command 옵션을 보면 아래와 같다.
warm-up-1: sleep 600
warm-up-2: sleep 1200

# 두개를 합치면 1800 이고 1분 = 60
# 1800 / 60 = 30분 이된다.
```

- `30 Minutes`

---

Q8. Update the pod `red` to use an `initContainer` that uses the `busybox` image and `sleeps for 20` seconds

- Delete and re-create the pod if necessary. But make sure no other configurations change.
  - 
    Pod: red
  - initContainer Configured Correctly

```shell
# -------------------------------------------
# delete pod red
# -------------------------------------------
root@controlplane:~# kubectl get pod red -o yaml > red.yaml
root@controlplane:~# kubectl delete pod red
pod "red" deleted

# -------------------------------------------
# vi red.yaml 
# -------------------------------------------
---
apiVersion: v1
kind: Pod
metadata:
  name: red
  namespace: default
spec:
  containers:
  - command:
    - sh
    - -c
    - echo The app is running! && sleep 3600
    image: busybox:1.28
    name: red-container
  initContainers:
  - image: busybox
    name: red-initcontainer
    command: 
      - "sleep"
      - "20"
      
# -------------------------------------------
# apply red.yaml 
# -------------------------------------------
root@controlplane:~# kubectl apply -f red.yaml 
pod/red created
```

---

Q9. A new application `orange` is deployed. There is something wrong with it. Identify and fix the issue.

- Once fixed, wait for the application to run before checking solution.

```shell
# -------------------------------------------
# orange 포드의 상태 확인
# -------------------------------------------
root@controlplane:~# kubectl get pod
NAME     READY   STATUS                  RESTARTS   AGE
blue     1/1     Running                 0          21m
green    2/2     Running                 0          21m
orange   0/1     Init:CrashLoopBackOff   1          27s
purple   0/1     Init:1/2                0          18m
red      1/1     Running                 0          84s

# -------------------------------------------
# orange 포드의 상세 상태 확인
# -------------------------------------------
root@controlplane:~# kubectl describe pod orange 
Name:         orange
...
Init Containers:
  init-myservice:
...
    Command:
      sh
      -c
      sleeeep 2;
    State:          Terminated
      Reason:       Error
      Exit Code:    127

# -------------------------------------------
# edit pod orange
#  - edit를 시도하면 tmp 폴더에 임시파일로 만든다.
#  - 이유는 잘 모르겠다.
# -------------------------------------------
root@controlplane:~# kubectl edit pod orange
error: pods "orange" is invalid
A copy of your changes has been stored to "/tmp/kubectl-edit-mg9gt.yaml"
error: Edit cancelled, no valid changes were saved.
root@controlplane:~# vi /tmp/kubectl-edit-mg9gt.yaml

# -------------------------------------------
# 기본의 orange 포드 삭제하고, 새로운 orange 포드를 생성한다.
# -------------------------------------------
root@controlplane:~# kubectl delete pod orange 
pod "orange" deleted
root@controlplane:~# kubectl apply -f /tmp/kubectl-edit-mg9gt.yaml
pod/orange created
root@controlplane:~# 

# -------------------------------------------
# orange 포드의 상태 확인
# -------------------------------------------
root@controlplane:~# kubectl get pod
NAME     READY   STATUS     RESTARTS   AGE
blue     1/1     Running    0          31m
green    2/2     Running    0          31m
orange   1/1     Running    0          59s
```

