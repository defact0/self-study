Practice Test - Labels and Selectors

- https://uklabs.kodekloud.com/topic/practice-test-labels-and-selectors-2/

---

Q1. We have deployed a number of PODs. They are labelled with `tier`, `env` and `bu`. How many PODs exist in the `dev` environment?

- Use selectors to filter the output

```shell
# 전체 라벨 출력
kubectl get pods --show-labels

# 특정 라벨 출력
kubectl get pods -l env=dev

# 특정 라벨 출력 갯수 출력
kubectl get pods -l env=dev --no-headers | wc -l
# 7
```

- `dev`이라는 라벨을 가진 Pod의 개수는 7개이다.

---

Q2. How many PODs are in the `finance` business unit (`bu`)?

```shell
# 전체 라벨 확인
root@controlplane:~# kubectl get pod --show-labels
NAME          READY   STATUS    RESTARTS   AGE    LABELS
app-1-l99xh   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-qd4m9   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-tvzvh   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-zzxdf   1/1     Running   0          5m9s   bu=finance,env=prod,tier=frontend
app-2-jdlkg   1/1     Running   0          5m9s   env=prod,tier=frontend
auth          1/1     Running   0          5m9s   bu=finance,env=prod
db-1-2glzs    1/1     Running   0          5m9s   env=dev,tier=db
db-1-h4425    1/1     Running   0          5m9s   env=dev,tier=db
db-1-j49ph    1/1     Running   0          5m9s   env=dev,tier=db
db-1-vwkcw    1/1     Running   0          5m9s   env=dev,tier=db
db-2-pc5nd    1/1     Running   0          5m9s   bu=finance,env=prod,tier=db

# bu=finance 개수 확인
root@controlplane:~# kubectl get pod -l bu=finance --no-headers | wc -l
6
```

- `finance` 이라는 라벨을 가진 Pod는 6개 이다.

---

Q3. How many objects are in the `prod` environment including PODs, ReplicaSets and any other objects?

```shell
# 전체 라벨 확인
root@controlplane:~# kubectl get pod --show-labels
NAME          READY   STATUS    RESTARTS   AGE    LABELS
app-1-l99xh   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-qd4m9   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-tvzvh   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-zzxdf   1/1     Running   0          5m9s   bu=finance,env=prod,tier=frontend
app-2-jdlkg   1/1     Running   0          5m9s   env=prod,tier=frontend
auth          1/1     Running   0          5m9s   bu=finance,env=prod
db-1-2glzs    1/1     Running   0          5m9s   env=dev,tier=db
db-1-h4425    1/1     Running   0          5m9s   env=dev,tier=db
db-1-j49ph    1/1     Running   0          5m9s   env=dev,tier=db
db-1-vwkcw    1/1     Running   0          5m9s   env=dev,tier=db
db-2-pc5nd    1/1     Running   0          5m9s   bu=finance,env=prod,tier=db

# prod 라벨을 전체 리소스 개수 확인
root@controlplane:~# kubectl get all -l env=prod --no-headers | wc -l
7
```

- `prod` 이라는 라벨을 가진 리소스의 개수는 7개이다.

---

Q4. Identify the POD which is part of the `prod` environment, the `finance` BU and of `frontend` tier?

```shell
# 전체 라벨 확인
root@controlplane:~# kubectl get pod --show-labels
NAME          READY   STATUS    RESTARTS   AGE    LABELS
app-1-l99xh   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-qd4m9   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-tvzvh   1/1     Running   0          5m9s   bu=finance,env=dev,tier=frontend
app-1-zzxdf   1/1     Running   0          5m9s   bu=finance,env=prod,tier=frontend
app-2-jdlkg   1/1     Running   0          5m9s   env=prod,tier=frontend
auth          1/1     Running   0          5m9s   bu=finance,env=prod
db-1-2glzs    1/1     Running   0          5m9s   env=dev,tier=db
db-1-h4425    1/1     Running   0          5m9s   env=dev,tier=db
db-1-j49ph    1/1     Running   0          5m9s   env=dev,tier=db
db-1-vwkcw    1/1     Running   0          5m9s   env=dev,tier=db
db-2-pc5nd    1/1     Running   0          5m9s   bu=finance,env=prod,tier=db

# env=prod | bu=finance | tier=frontend 조건으로 검색해라
root@controlplane:~# kubectl get pods -l env=prod,bu=finance,tier=frontend
NAME          READY   STATUS    RESTARTS   AGE
app-1-zzxdf   1/1     Running   0          13m

root@controlplane:~# kubectl get pods -l env=prod,bu=finance,tier=frontend --show-labels
NAME          READY   STATUS    RESTARTS   AGE   LABELS
app-1-zzxdf   1/1     Running   0          13m   bu=finance,env=prod,tier=frontend
```

- 위 조건을 만족하는 Pod는 `app-1-zzxdf` 이다.

---

Q5. A ReplicaSet definition file is given `replicaset-definition-1.yaml`. Try to create the replicaset. There is an issue with the file. Try to fix it.

- ReplicaSet: replicaset-1
- Replicas: 2

```shell
# 제공되는 yaml 파일을 사용했을 경우, 아래와 같이 오류가 발생한다.
root@controlplane:~# ls
replicaset-definition-1.yaml
root@controlplane:~# kubectl apply -f replicaset-definition-1.yaml 
The ReplicaSet "replicaset-1" is invalid: spec.template.metadata.labels: Invalid value: map[string]string{"tier":"nginx"}: `selector` does not match template `labels`

# yaml 파일을 수정한다.
apiVersion: apps/v1
kind: ReplicaSet
metadata:
   name: replicaset-1
spec:
   replicas: 2
   selector:
      matchLabels:
        tier: frontend
   template:
     metadata:
       labels:
        #tier: nginx
        tier: frontend
     spec:
       containers:
       - name: nginx
         image: nginx

# 정상적으로 생성되었다.
root@controlplane:~# kubectl apply -f replicaset-definition-1.yaml 
replicaset.apps/replicaset-1 created

root@controlplane:~# kubectl get rs
NAME           DESIRED   CURRENT   READY   AGE
app-1          3         3         3       17m
app-2          1         1         1       17m
db-1           4         4         4       17m
db-2           1         1         1       17m
replicaset-1   2         2         1       24s
```

- `selector`와 `template`에 있는 라벨을 일치시켜야 한다.



