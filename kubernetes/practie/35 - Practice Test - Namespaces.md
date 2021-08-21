Practice Test - Namespaces

- https://uklabs.kodekloud.com/topic/practice-test-namespaces-2/

---

Q1. How many Namespaces exist on the system?

```shell
root@controlplane:~# kubectl get namespaces 
NAME              STATUS   AGE
default           Active   5m41s
dev               Active   26s
finance           Active   26s
kube-node-lease   Active   5m44s
kube-public       Active   5m44s
kube-system       Active   5m45s
manufacturing     Active   26s
marketing         Active   26s
prod              Active   26s
research          Active   26s

# no-headers 옵션으로 순수하게 ns 리스트만 출력하게 한다.
# 그리고 wc -l 옵션으로 카운트를 세서 출력하게 한다.
root@controlplane:~# kubectl get ns --no-headers | wc -l
10
```

---

Q2. How many pods exist in the `research` namespace?

```shell
# research 이라는 네임스페이스의 pod를 출력
root@controlplane:~# kubectl get pod -n research 
NAME    READY   STATUS             RESTARTS   AGE
dna-1   0/1     Completed          5          3m59s
dna-2   0/1     CrashLoopBackOff   5          3m58s

# research의 Pod리스트를 헤더 없이 출력
root@controlplane:~# kubectl get pod -n research --no-headers 
dna-1   0/1   Completed          5     4m6s
dna-2   0/1   CrashLoopBackOff   5     4m5s

# research의 Pod 개수만 출력
root@controlplane:~# kubectl get pod -n research --no-headers  | wc -l
2
```

---

Q3. Create a POD in the `finance` namespace.

- Use the spec given below.
  - Name: redis
  - Image Name: redis

```shell
# finance 네임스페이스 생성할 redis yaml 파일 생성
root@controlplane:~# kubectl run redis --image=redis -n finance --dry-run=client -o yaml > redis.yaml 

# yaml 파일 적용
root@controlplane:~# kubectl apply -f redis.yaml 
pod/redis created

# yaml 적용 확인
root@controlplane:~# kubectl get pod -n finance 
NAME      READY   STATUS    RESTARTS   AGE
payroll   1/1     Running   0          9m23s
redis     1/1     Running   0          7s
```

---

Q4. Which namespace has the `blue` pod in it?

```shell
root@controlplane:~# kubectl get pod --all-namespaces | grep blue
marketing       blue                                   1/1     Running            0          11m
```

- `blue` pod는 `marketing` namespace에 있다.

---

Q5 - Q6. 

Access the Blue web application using the link above your terminal

- From the UI you can ping other services

What DNS name should the Blue application use to access the database `db-service` in its own namespace - `marketing`.

- You can try it in the web application UI. Use port `6379`.

```shell
root@controlplane:~# kubectl get svc -n marketing 
NAME           TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
blue-service   NodePort   10.108.111.180   <none>        8080:30082/TCP   20m
db-service     NodePort   10.96.207.103    <none>        6379:32718/TCP   20m
root@controlplane:~# 
```

- `6379` 포트 설정이 되어 있는 `db-service`을 선택한다.

---

Q7. What DNS name should the Blue application use to access the database 'db-service' in the 'dev' namespace

- You can try it in the web application UI. Use port 6379.

```shell
root@controlplane:~# kubectl get svc -n dev
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
db-service   ClusterIP   10.105.188.38   <none>        6379/TCP   20m
```

- db-service.dev.svc.cluster.local

> Service 도메인 주소 법칙은 다음과 같다.
> `<서비스 이름>.<네임 스페이스>.svc.cluster.local`

