

연습환경

- https://labs.play-with-k8s.com/

- controlplane node 1개, worker node 1개 환경 설정

  ```shell
  ## controlplane setting...
  kubeadm init --apiserver-advertise-address $(hostname -i) --pod-network-cidr 10.5.0.0/16
  kubectl apply -f https://raw.githubusercontent.com/cloudnativelabs/kube-router/master/daemonset/kubeadm-kuberouter.yaml
  
  ## worker node setting...
  kubeadm join 192.168.0.8:6443 --token s3c32x.j2hxtu1z0fsqvvej \
      --discovery-token-ca-cert-hash sha256:503ab43b56289e6fc26fa33cb85e99a379ce8e3a9d210bcfbda50a6595afff7c 
  ```

  - hostname을 변경하면 kubeadm 관련 오류가 발생할 수 있다.
  - 터미널 텍스트 복사 = Ctrl + Insert
  - 터미널 텍스트 붙여넣기 + Shift + Insert

  ```shell
  ## 설정 완료 상태
  [node1 ~]$ kubectl get nodes 
  NAME    STATUS   ROLES                  AGE   VERSION
  node1   Ready    control-plane,master   84s   v1.20.1
  node2   Ready    <none>                 29s   v1.20.1
  ```

---

**Pod 리소스**

```shell
## YAML을 사용하여 image=jenkins로 jenkins-manual Pod 생성
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: jenkins-manual
spec:
  containers:
  - name: jenkins
    image: jenkins
    ports:
    - containerPort: 8080
EOF

## jenkins 포드에서 curl 명령어로 localhost:8080 접속
kubectl exec jenkins-manual -- curl 127.0.0.1:8080 -s

## jenkins 포트를 8888으로 포트포워딩
kubectl port-forward jenkins-manual 8888:8080
kubectl logs jenkins-manual
```

---

[**Liveness & Readiness**](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)

```shell
## exec-liveness
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: liveness-exec
spec:
  containers:
  - name: liveness
    image: k8s.gcr.io/busybox
    args:
    - /bin/sh
    - -c
    - touch /tmp/healthy; sleep 30; rm -rf /tmp/healthy; sleep 600
    livenessProbe:
      exec:
        command:
        - cat
        - /tmp/healthy
      initialDelaySeconds: 5
      periodSeconds: 5
EOF

## 이벤트 확인을 위해 describe로 확인
kubectl describe pod liveness-exec

## liveness-http
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  labels:
    test: liveness
  name: liveness-http
spec:
  containers:
  - name: liveness
    image: k8s.gcr.io/liveness
    args:
    - /server
    livenessProbe:
      httpGet:
        path: /healthz
        port: 8080
        httpHeaders:
        - name: Custom-Header
          value: Awesome
      initialDelaySeconds: 3
      periodSeconds: 3
EOF


## tcp-liveness-readiness
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: goproxy
  labels:
    app: goproxy
spec:
  containers:
  - name: goproxy
    image: k8s.gcr.io/goproxy:0.1
    ports:
    - containerPort: 8080
    readinessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 10
    livenessProbe:
      tcpSocket:
        port: 8080
      initialDelaySeconds: 15
      periodSeconds: 20
EOF
```

---

**레이블 추가/생성/삭제/필터링**

```shell
## pod-01
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: http-go
  labels:
    creation_method: manual
    env: prod
spec:
  containers:
  - name: http-go
    image: gasbugs/http-go
    ports:
    - containerPort: 8080
      protocol: TCP
EOF

## pod-02
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: http-go-v3
  labels:
    creation_method: manual
spec:
  containers:
  - name: http-go
    image: gasbugs/http-go
    ports:
    - containerPort: 8080
      protocol: TCP
EOF

## get
kubectl get pod
kubectl get pod --show-labels

## 대문자 L로 검색하면 원하는 컬럼만 추려서 출력
kubectl get pod -L env
kubectl get pod -L creation_method

## 만들어진 Pod에 레이블 추가
kubectl label pod http-go test=foo

## 만들어진 Pod에 레이블 수정
kubectl label pod http-go test=foo1 --overwrite

## 필요없는 레이블 삭제
## 레이블 key에 -를 붙인다.
kubectl label pod http-go test-

## 레이블 검색
kubectl get pod -l '!env'
kubectl get pod -l 'env=prod,creation_method=manual'
```

---

**레이블과 셀렉터 연습**

```shell
## nginx pod
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
  - name: nginx
    image: nginx
    ports:
    - containerPort: 80
      protocol: TCP
EOF

## 포트포워딩 테스트
kubectl port-forward nginx 80:80

## 웹 브라우저에서 http://127.0.0.1 으로 연결 테스트

## label 검색
kubectl get pod -l app=nginx
## app이라는 Column 추가하여 출력
kubectl get pod -l app=nginx -L app
## label 추가
kubectl label pod nginx team=dev1
kubectl get pod --show-labels
```

---

**[ReplicaSet](https://kubernetes.io/ko/docs/concepts/workloads/controllers/replicaset/) 연습**

```shell
## yaml
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: rs-nginx
spec:
  replicas: 3
  selector:
    matchLabels:
      tier: rs-nginx
  template:
    metadata:
      labels:
        tier: rs-nginx
    spec:
      containers:
      - name: nginx
        image: nginx
        ports:
        - containerPort: 80
EOF

## 생성확인
kubectl get pod
kubectl get rs
```

----

[**Deployment**](https://kubernetes.io/ko/docs/concepts/workloads/controllers/deployment/)

```shell
cat << EOF | kubectl apply -f -
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deploy-jenkins
  labels:
    app: jenkins-test
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jenkins-test
  template:
    metadata:
      labels:
        app: jenkins-test
    spec:
      containers:
      - name: jenkins
        image: jenkins
        ports:
        - containerPort: 8080
EOF

## 생성 상태 전체 보기
kubectl get all

## Pod 복구 확인
kubectl delete pod <deploy-jenkins-xxxxx>

## label
kubectl get pod --show-labels
kubectl label pod <pod이름> <labels이름>-

## replicas 갯수를 5개로 확장
kubectl scale deploy <deploy이름> --replicas=5
## edit 명령어로 replicas 수정이 가능하다.
```

---

**롤링 업데이트와 롤백 연습**

```shell
## 기존 리소스 전체 삭제
kubectl delete all --all

## deploy 리소스 생성
kubectl create deploy alpine-deploy --image=alpine:3.4 --dry-run=client -o yaml > deploy.yaml

vim deploy.yaml
# replicas: 10
# strategy.type: RollingUpdate
# strategy.rollingUpdate.maxSurge: 50%
# strategy.rollingUpdate.maxUnavailable: 50%

## 히스토리 기록
kubectl apply -f deploy.yaml --record

## 히스토리 확인
kubectl rollout history deploy alpine-deploy

## 이미지 업데이트
kubectl edit deploy alpine-deploy --record
# alpine:3.4 -> alpine:3.5


## 롤백하기 (revision 1으로)
kubectl rollout undo deploy alpine-deploy --to-revision=1
# history를 다시 확인하면 1번이 사라지고 제일 큰 번호로 추가된 것을 확인 할 수 있다.
```

----

**네임스페이스 연습**

```shell
## namespaces 확인
kubectl get ns
kubectl get pod -n kube-system
kubectl get pod --all-namespaces

## 네임스페이스 생성
kubectl create ns ns-jenkins --dry-run=client -o yaml > ns.yaml

vim ns.yaml
# pod을 추가한다.
apiVersion: v1
kind: Namespace
metadata:
  name: ns-jenkins
---
apiVersion: v1
kind: Pod
metadata:
  name: jenkins
  namespace: ns-jenkins
spec:
  containers:
  - name: jenkins
    image: jenkins
    ports:
    - containerPort: 8080

kubectl apply -f ns.yaml

# 순서대로 네임스페이스 리소스 부터 생성되어야 한다.

kubectl get pod -n ns-jenkins
kubectl get pod --all-namespaces
kubectl get pod --all-namespaces | grep coredns


```

---

**Serivce**

- 서비스를 생성하는 가장 쉬운 방법
- YAML 파일로 관리하는게 좋다.
- ClusterIP
  - 서비스 리소스를 만들면 생성된다.
  - 다수의 포드를 하나의 서비스로 묶어서 관리
- 서비스 세션 고정하기
  - 다수의 포드로 구성하면 웹서비스의 세션이 유지되지 않음
  - 처음 들어왔던 클라이언트 IP를 그대로 유지해주는 방법이 필요
  - `sessionAffinity: ClientIP` 옵션을 추가
- 외부IP 연결설정 방법
  - service와 endpoints 리소스 모두 생성 필요

```shell
## deployment 리소스 생성
kubectl create http-go-svc --image=gasbugs/http-go --dry-run=client -o yaml > deploy.yaml
vi deploy.yaml
# sepc.containers.ports.containerPort: 8080 추가
# service 검색하여 yaml 내용 추가
# service에서 port: 80, targetPort: 8080 설정
kubectl apply -f deploy.yaml

kubectl describe svc http-go-svc
# Endpoints 부분에 Running 상태에 있는 Pod들의 IP주소들을 볼 수 있다.
```

---

**NodePort**

서비스 노출하는 세 가지 방법

- NodePort: 노드의 자체 포트를 사용하여 포드로 리다이렉션
- LoadBalancer: 외부 게이트웨이를 사용해 노드 포트로 리다이렉션
  - 클라우드 서비스의 리소스를 통해 사용가능
- Ingress: 하나의 IP 주소를 통해 여러 서비스를 제공하는 특별한 메커니즘



