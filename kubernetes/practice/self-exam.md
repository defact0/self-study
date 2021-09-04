

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

레이블 추가/생성/삭제/필터링

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

##

```

