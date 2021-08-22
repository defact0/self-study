Practice Test - Manual Scheduling

- https://uklabs.kodekloud.com/topic/practice-test-manual-scheduling-2/

> kube-scheduler 가 없는 상태에서 진행하는 연습이다.

---

Q1. A pod definition file `nginx.yaml` is given. Create a pod using the file.

- Only create the POD for now. We will inspect its status next.
- Pod nginx Created

```shell
# Pod를 생성할 수 있는 yaml 파일이 제공해 준다. 이것을 사용해서 생성해라

root@controlplane:~# ls
nginx.yaml  sample.yaml

root@controlplane:~# kubectl apply -f nginx.yaml 
pod/nginx created
```

---

Q2. What is the status of the created POD?

```shell
root@controlplane:~# kubectl get pod
NAME    READY   STATUS    RESTARTS   AGE
nginx   0/1     Pending   0          64s
```

- Pod의 상태가 `Pending` 이다.

---

Q3. Why is the POD in a pending state?

- Inspect the environment for various kubernetes control plane components.

```shell
root@controlplane:~# kubectl get pod -n kube-system 
NAME                                   READY   STATUS    RESTARTS   AGE
coredns-74ff55c5b-4qdzd                1/1     Running   0          15m
coredns-74ff55c5b-htnqb                1/1     Running   0          15m
etcd-controlplane                      1/1     Running   0          15m
kube-apiserver-controlplane            1/1     Running   0          15m
kube-controller-manager-controlplane   1/1     Running   0          15m
kube-flannel-ds-q57fr                  1/1     Running   0          15m
kube-flannel-ds-skl8x                  1/1     Running   0          14m
kube-proxy-hbx7q                       1/1     Running   0          14m
kube-proxy-hv4h9                       1/1     Running   0          15m
```

- kube-system 네임스페이스의 Pod를 확인해 보니 스케쥴러가 없다. 그래서 정답은 `No Scheduler Present`

---

Q4. Manually schedule the pod on `node01`.

- Delete and recreate the POD if necessary.
  - Status: Running
  - Pod: nginx

```shell
# -----------------------------------------------------------------
# controlplane 노드에 스케줄러가 없기 때문에 수동으로 Pod를 생성해야 한다.
# -----------------------------------------------------------------
# 기존에 생성한 Pod 삭제
kubectl delete pod nginx

# yaml 파일 수정
vi nginx.yaml

# spec.nodeName 추가
# root@controlplane:~# kubectl get node
# NAME           STATUS   ROLES                  AGE   VERSION
# controlplane   Ready    control-plane,master   18m   v1.20.0
# node01         Ready    <none>                 18m   v1.20.0
---
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: node01
  containers:
  -  image: nginx
     name: nginx

# apply
root@controlplane:~# kubectl apply -f nginx.yaml 
pod/nginx created

# get pod
root@controlplane:~# kubectl get pod -w 
NAME    READY   STATUS              RESTARTS   AGE
nginx   0/1     ContainerCreating   0          11s
nginx   1/1     Running             0          21s
```

---

Q5. Now schedule the same pod on the `controlplane` node.

- Delete and recreate the POD if necessary.
  - Status: Running
  - Pod: nginx
  - Node: controlplane?

```shell
# -----------------------------------------------------------------
# controlplane 노드에 Pod를 생성하기?
# -----------------------------------------------------------------
# 기존에 생성된 Pod 지우기
root@controlplane:~# kubectl delete pod nginx 
pod "nginx" deleted

# node 체크
root@controlplane:~# kubectl get node
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   25m   v1.20.0
node01         Ready    <none>                 24m   v1.20.0

# yaml 파일 수정
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: controlplane
  containers:
  -  image: nginx
     name: nginx
     
# apply
root@controlplane:~# kubectl apply -f nginx.yaml 
pod/nginx created

# 옵션을 확장 시켜보면 ngix pod는 controlplane에서 만들어지는 것을 확인 할 수 있다.
root@controlplane:~# kubectl get pod -o wide -w
NAME    READY   STATUS              IP       NODE           NOMINATED NODE   READINESS GATES
nginx   0/1     ContainerCreating   <none>   controlplane   <none>           <none>
nginx   1/1     Running             10.244.0.4   controlplane   <none>           <none>





```

