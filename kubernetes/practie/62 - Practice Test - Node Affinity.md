Practice Test - Node Affinity

- https://uklabs.kodekloud.com/topic/practice-test-node-affinity-3/

---

Q1. How many Labels exist on node node01?

```shell
root@controlplane:~# kubectl get nodes node01 --show-labels
NAME     STATUS   ROLES    AGE    VERSION   LABELS
node01   Ready    <none>   8m9s   v1.20.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux
```

- 5 개의 label이 있다.

---

Q2. What is the value set to the label `beta.kubernetes.io/arch` on `node01`?

- `beta.kubernetes.io/arch=amd64` 부분을 확인해 보면, `amd64` 가 정답이다.

---

Q3. Apply a label `color=blue` to node `node01`

- color = blue

```shell
# 변경 이전 확인
root@controlplane:~# kubectl get nodes node01 --show-labels
NAME     STATUS   ROLES    AGE   VERSION   LABELS
node01   Ready    <none>   11m   v1.20.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux

# node에 라벨추가
root@controlplane:~# kubectl label nodes node01 color=blue
node/node01 labeled

# 변경 이후 확인
root@controlplane:~# kubectl get nodes node01 --show-labels
NAME     STATUS   ROLES    AGE   VERSION   LABELS
node01   Ready    <none>   11m   v1.20.0   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,color=blue,kubernetes.io/arch=amd64,kubernetes.io/hostname=node01,kubernetes.io/os=linux
```

---

Q4. Create a new deployment named `blue` with the `nginx` image and 3 replicas.

- Name: blue
- Replicas: 3
- Image: nginx

```shell
root@controlplane:~# kubectl create deployment blue --image=nginx
deployment.apps/blue created

root@controlplane:~# kubectl scale deployment blue --replicas=3
deployment.apps/blue scaled

root@controlplane:~# kubectl get deployments.apps blue 
NAME   READY   UP-TO-DATE   AVAILABLE   AGE
blue   0/3     3            0           28s
```

---

Q5. Which nodes `can` the pods for the `blue` deployment be placed on?

- Make sure to check taints on both nodes!

```shell
root@controlplane:~# kubectl describe node controlplane | grep -i taints
Taints:             <none>
root@controlplane:~# kubectl describe node node01 | grep -i taints
Taints:             <none>
```

- taint 설정이 없기 때문에 `controlplane and node01` 둘 중 하나에 노드에 pod가 생성된다.

---

Q6. Set Node Affinity to the deployment to place the pods on `node01` only.

- Name: blue
- Replicas: 3
- Image: nginx
- NodeAffinity: requiredDuringSchedulingIgnoredDuringExecution
- Key: color
- values: blue

```shell
# blue 디플로이먼트에 nodeaffinity 추가
root@controlplane:~# kubectl get deployments.apps blue -o yaml > blue.yaml
root@controlplane:~# vi blue.yaml 

# addinity 추가
# 들여쓰기 같은 것을 주의해야 한다.
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: color
                operator: In
                values:
                - blue
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx

# 기존에 있던 디플로이먼트 삭제
root@controlplane:~# kubectl delete deployments.apps blue 
deployment.apps "blue" deleted

# 수정된 yaml 파일 적용
root@controlplane:~# kubectl apply -f blue.yaml 
deployment.apps/blue created

```

- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#node-affinity

---

Q7. Which nodes are the pods placed on now?

```shell
root@controlplane:~# kubectl get pod -o wide
NAME                    READY   STATUS    RESTARTS   AGE   IP            NODE  
blue-566c768bd6-2727n   1/1     Running   0          96s   10.244.1.27   node01
blue-566c768bd6-4nxqk   1/1     Running   0          96s   10.244.1.26   node01
blue-566c768bd6-wfh8n   1/1     Running   0          96s   10.244.1.25   node01
```

- `node01`

---

Q8. Create a new deployment named `red` with the `nginx` image and `2` replicas, and ensure it gets placed on the `controlplane` node only.

- Use the label - `node-role.kubernetes.io/master` - set on the controlplane node.
  - Name: red
  - Replicas: 2
  - Image: nginx
  - NodeAffinity: requiredDuringSchedulingIgnoredDuringExecution
  - Key: node-role.kubernetes.io/master
  - Use the right operator

```shell
# deployment 생성
kubectl create deployment red --image=nginx --dry-run=client -o yaml > red.yaml

# red.yaml 편집
vi red.yaml

# Replicas: 2
# requiredDuringSchedulingIgnoredDuringExecution 추가
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: red
  name: red
spec:
  replicas: 2
  selector:
    matchLabels:
      app: red
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: red
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role.kubernetes.io/master
                operator: Exists
      containers:
      - image: nginx
        name: nginx
        resources: {}
status: {}
  
# 수정된 yaml 파일 적용
root@controlplane:~# kubectl apply -f red.yaml 
deployment.apps/red created

# 생성된 deployments 확인
root@controlplane:~# kubectl get deployments.apps -o wide
NAME   READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES   SELECTOR
blue   3/3     3            3           12m   nginx        nginx    app=blue
red    2/2     2            2           42s   nginx        nginx    app=red

root@controlplane:~# kubectl get pods -o wide | grep red
red-5cbd45ccb6-bwxpc    1/1     Running   0          29s     10.244.0.7    controlplane
red-5cbd45ccb6-rzggk    1/1     Running   0          29s     10.244.0.8    controlplane
```





