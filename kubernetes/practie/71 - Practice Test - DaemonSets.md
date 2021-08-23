Practice Test - DaemonSets

- https://uklabs.kodekloud.com/topic/practice-test-daemonsets-2/

---

Q1. How many `DaemonSets` are created in the cluster in all namespaces?

```shell
root@controlplane:~# kubectl get ds --all-namespaces 
NAMESPACE     NAME              DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kube-system   kube-flannel-ds   1         1         1       1            1           <none>                   5m10s
kube-system   kube-proxy        1         1         1       1            1           kubernetes.io/os=linux   5m13s
```

- DaemonSets이 2개가 있다.

---

Q2. Which namespace are the `DaemonSets` created in?

- Q1를 참고하면 데몬셋 네임스페이스는 모두 `kube-system`에 적용되어 있다.

---

Q3. Which of the below is a `DaemonSet`?

- `kube-flannel-ds` 이다.

---

Q4. On how many nodes are the pods scheduled by the **DaemonSet** `kube-proxy`

```shell
NAME           STATUS   ROLES                  AGE     VERSION
controlplane   Ready    control-plane,master   9m52s   v1.20.0

root@controlplane:~# kubectl -n kube-system get pod | grep proxy
kube-proxy-hz2wv                       1/1     Running   0          10m

root@controlplane:~# kubectl -n kube-system get pod -o wide | grep proxy
kube-proxy-hz2wv                       1/1     Running   0          10m   10.20.139.9   controlplane   <none>           <none>
```

- pod가 controlplane에 1개가 스케줄링 되어 있음을 확인할 수 있다.

---

Q5. What is the image used by the POD deployed by the `kube-flannel-ds` **DaemonSet**?

```shell
root@controlplane:~# kubectl -n kube-system describe ds kube-flannel-ds | grep -i image
    Image:      quay.io/coreos/flannel:v0.13.1-rc1
    Image:      quay.io/coreos/flannel:v0.13.1-rc1
```

- Image는 `quay.io/coreos/flannel:v0.13.1-rc1`을 쓰고 있다.

---

Q6. Deploy a **DaemonSet** for `FluentD` Logging.

- Name: elasticsearch
- Namespace: kube-system
- Image: k8s.gcr.io/fluentd-elasticsearch:1.20

```shell
# DaemonSet을 만들기 위해서 yaml 파일 생성
# - 솔루션 영상에서는 deployment 템플릿 기반으로 만든다.
root@controlplane:~# kubectl create deployment elasticsearch --image=k8s.gcr.io/fluentd-elasticsearch:1.20 --dry-run=client -o yaml > elastic.yaml

# yaml 파일 수정
apiVersion: apps/v1
kind: DaemonSet
metadata:
  labels:
    app: elasticsearch
  name: elasticsearch
  namespace: kube-system
spec:
  selector:
    matchLabels:
      app: elasticsearch
  template:
    metadata:
      labels:
        app: elasticsearch
    spec:
      containers:
      - image: k8s.gcr.io/fluentd-elasticsearch:1.20
        name: fluentd-elasticsearch

# apply
root@controlplane:~# kubectl apply -f elastic.yaml 
daemonset.apps/elasticsearch created

# 적용 상태 확인하기
root@controlplane:~# kubectl -n kube-system get ds elasticsearch 
NAME            DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
elasticsearch   1         1         1       1            1           <none>          52s
```

- https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/#create-a-daemonset