Practice Test - Pods

- https://uklabs.kodekloud.com/topic/practice-test-pods-2/

---

Q1. How many `pods` exist on the system?

```shell
root@controlplane:~# kubectl get all
NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   2m53s
root@controlplane:~# 
```

- 생성된 Pod는 없다!

---

Q2. Create a new pod with the `nginx` image.

- Image name: nginx

```shell
root@controlplane:~# kubectl run nginx --image=nginx
pod/nginx created
root@controlplane:~# kubectl get pod
NAME    READY   STATUS              RESTARTS   AGE
nginx   0/1     ContainerCreating   0          7s
root@controlplane:~# watch kubectl get pod
root@controlplane:~# kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          36s
root@controlplane:~# 
```

---

Q3. How many pods are created now?

> Note: We have created a few more pods. So please check again.

```shell
root@controlplane:~# kubectl get pod
NAME            READY   STATUS    RESTARTS   AGE
newpods-kbrxk   1/1     Running   0          62s
newpods-n7mjq   1/1     Running   0          62s
newpods-wxtl7   1/1     Running   0          62s
nginx           1/1     Running   0          114s
root@controlplane:~# 
```

- 생성된 Pod는 4개

---

Q4. What is the image used to create the new pods?

- You must look at one of the new pods in detail to figure this out.

```shell
root@controlplane:~# kubectl get pod
NAME            READY   STATUS    RESTARTS   AGE
newpods-7bv2s   1/1     Running   0          45s
newpods-bqrjc   1/1     Running   0          44s
newpods-pmtxk   1/1     Running   0          44s
nginx           1/1     Running   0          50s
root@controlplane:~# kubectl describe pod newpods-7bv2s | grep -i image
    Image:         busybox
    Image ID:      docker-pullable://busybox@sha256:0f354ec1728d9ff32edcd7d1b8bbdfc798277ad36120dc3dc683be44524c8b60
  Normal  Pulling    65s   kubelet            Pulling image "busybox"
  Normal  Pulled     51s   kubelet            Successfully pulled image "busybox" in 14.518060579s
root@controlplane:~# 
```

- newpods 를 만드는데 사용한 이미지는 "busybox" 이다.

  

---

Q5. Which nodes are these pods placed on?

- You must look at all the pods in detail to figure this out.

```shell
root@controlplane:~# kubectl get pod -o wide
NAME            READY   STATUS    IP           NODE           NOMINATED NODE   READINESS GATES
newpods-kbrxk   1/1     Running   10.244.0.6   controlplane   <none>           <none>
newpods-n7mjq   1/1     Running   10.244.0.5   controlplane   <none>           <none>
newpods-wxtl7   1/1     Running   10.244.0.7   controlplane   <none>           <none>
nginx           1/1     Running   10.244.0.4   controlplane   <none>           <none>
root@controlplane:~# 
```

- Node 항목을 보면 `controlplane` 이라고 출력된다.

---

Q6. How many containers are part of the pod webapp?

- Note: We just created a new POD. Ignore the state of the POD for now.

```shell
root@controlplane:~# kubectl get pod webapp 
NAME     READY   STATUS         RESTARTS   AGE
webapp   1/2     ErrImagePull   0          63s
root@controlplane:~# 
```

- 정답은 2개이다. (Pod의 상태는 신경 쓰지말라는 조건이 있다)

---

Q7. What images are used in the new `webapp` pod?

- You must look at all the pods in detail to figure this out.

```shell
root@controlplane:~# kubectl describe pod webapp 
Name:         webapp
Namespace:    default
Priority:     0
Node:         controlplane/10.31.238.6
Start Time:   Fri, 20 Aug 2021 16:11:39 +0000
Labels:       <none>
Annotations:  <none>
Status:       Pending
IP:           10.244.0.8
IPs:
  IP:  10.244.0.8
Containers:
  nginx:
    Container ID:   docker://515d41e0a59d...
    Image:          nginx
# 생략....
  agentx:
    Container ID:   
    Image:          agentx
```

- `Containers.Image` 항목을 보면 이미지는 nginx 와 agentx를 사용한 것을 알 수 있다.

---

Q8. What is the state of the container `agentx` in the pod `webapp`?

- Wait for it to finish the `ContainerCreating` state

```shell
root@controlplane:~# kubectl describe pod webapp 
# 생략....
  agentx:
    Container ID:   
    Image:          agentx
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
# 생략....
Failed to pull image "agentx": rpc error: code = Unknown desc = Error response from daemon: pull access denied for agentx, repository does not exist or may require 'docker login': denied: requested access to the resource is denied
```

- `State` 부분을 보면 `Waiting` 인 것을 확인 할 수 있다.

---

Q9. Why do you think the container `agentx` in pod `webapp` is in error?

- Try to figure it out from the events section of the pod.
- Q8의 내용을 참고하면
  해당 이미지가 존재하지 않거나 docker login이 요구된다.
  `A Docker image with this name doesn't exist on Docker Hub`

---

Q10. What does the READY column in the output of the `kubectl get pods` command indicate?

- `Running Containers in POD/Total Containers in POD`

---

Q11. Delete the `webapp` Pod.

- Once deleted, wait for the pod to fully terminate.

```shell
root@controlplane:~# kubectl get pods
NAME            READY   STATUS             RESTARTS   AGE
newpods-7bv2s   1/1     Running            0          15m
newpods-bqrjc   1/1     Running            0          15m
newpods-pmtxk   1/1     Running            0          15m
nginx           1/1     Running            0          15m
webapp          1/2     ImagePullBackOff   0          13m
root@controlplane:~# kubectl delete pod webapp 
pod "webapp" deleted
root@controlplane:~# kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
newpods-7bv2s   1/1     Running   1          17m
newpods-bqrjc   1/1     Running   1          17m
newpods-pmtxk   1/1     Running   1          17m
nginx           1/1     Running   0          17m
root@controlplane:~# 
```

---

Q12. Create a new pod with the name `redis` and with the image `redis123`.

- Use a pod-definition YAML file. And yes the image name is wrong!
  - Name: redis
  - Image Name: redis123

```shell
# YAML 파일로 정의한 다음에 Pod를 생성하라고 조건이 있다.
root@controlplane:~# kubectl run redis --image=redis123 --dry-run=client -o yaml > pod.yaml

# pod.yaml 가 생성된 것을 확인 할 수 있다.
root@controlplane:~# ls
pod.yaml  sample.yaml
root@controlplane:~# vi pod.yaml 

# pod.yaml을 apply
root@controlplane:~# kubectl apply -f pod.yaml 
pod/redis created

# redis pod의 상태 확인 - 이미지가 잘못되어 있어 당연히 정상상태가 아니게 된다.
root@controlplane:~# kubectl get pod redis
NAME    READY   STATUS             RESTARTS   AGE
redis   0/1     ImagePullBackOff   0          10s
root@controlplane:~# 

```

---

Q13. Now change the image on this pod to `redis`.

- Once done, the pod should be in a `running` state.
  - Name: redis
  - Image Name: redis

```shell
# redis pod를 edit 하면 바로 vim 화면으로 넘어간다.
root@controlplane:~# kubectl edit pod redis

# redis pod 수정을 하고 저장종료 한다.
spec:
  containers:
#  - image: redis123
  - image: redis
  
# 저장하고 종료하면 바로 수정사항이 반영된다.
pod/redis edited
root@controlplane:~# kubectl get pod redis
NAME    READY   STATUS    RESTARTS   AGE
redis   1/1     Running   0          4m28s
root@controlplane:~# 

```



