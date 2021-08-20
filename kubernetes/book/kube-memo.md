kubernetes memo

CKA 시험에서 선언적 방식보다는 커맨드 명령으로 작업을 처리하는 것이 시간 절약을 할 수 있게 한다.

```shell
# Pod -----------------------------------------------------------------
# nginx 포드 만들기
kubectl run nginx --image=nginx

# Pod manifest yaml
kubectl run --generator=run-pod/v1 nginx --image=nginx --dry-run -o yaml

# Deployment -----------------------------------------------------------
# deployment 1
kubectl run --generator=deployment/v1beta1 nginx --image=nginx --dry-run =o yaml

# deployment 2
kubectl create deployment nginx --image=nginx --dry-run -o yaml

# 임시적인 yaml 파일 생성 + 복제본 4개 설정
kubectl run --generator=deployment/v1beta1 nginx --image=nginx --dry-run --replicas=4 -o yaml

# 이미지 변경
kubectl set image deployment nginx nginx=nginx:1.18

# Service ---------------------------------------------------------------
# redis-service 이름의 ClusterIP 서비스를 포트 6379에서 서비스하도록 생성 
# (라벨 선택기 자동으로 지정)
kubectl expose pod redis --port=6379 --name redis-service --dry-runn -o yaml

# 또는
kubectl create service clusterip redis --tcp=6379:6379 --dry-run -o yaml

# nginx 이름의 NodePort 서비스를 노드 포트 30080에서 
# nginx 포드의 80번 포트를 서비스하도록 생성
#  - 이 경우 노드 포트 선택 불가
kubectl expose pod nginx --port=80 --name nginx-service --dry-run -o yaml
#  - 이 경우 노드 포트 셀렉터 사용 불가
kubectl create service nodeport nginx --tcp=80:80 --node-port=30090 --dry-run -o yaml

# clusterip
kubectl create service clusterip nginx --tcp:80:80 --dry-run=client -o yaml

# nodeport
kubectl create service nodeport nginx --tcpL80:30080 --dry-run=client -o yaml

# DNS -------------------------------------------------------------------------
<서비스이름>.<네임스페이스>.svc.cluster.local

# UPGRADE ---------------------------------------------------------------------
# master node -> worker node
kubeadm upgrade plan
kubectl drain <nodename>
apt install kubeadm=1.19.0-00
kubeadm upgrade apply <버전이름>
kubeadm updrade node
apt installl kubelet=1.19.0-00

```



---

- etcd port = 2379
- 포드 1개당 컨테이너 1개로 운영하는 것이 보통
  - 컨테이너가 2개 들어가는 경우는 파일 시스템 공유가 필요한 경우
  - 사이드카 패턴 적용시(로그 처리)
- worker node가 일시적으로 네트워크 단절이 일어나게 되면 쿠버네티스에서는 즉각 반응하지 않는다.
  - 즉각 반응하게 되면 불필요한 작업이나 리소스 소모가 발생
  - 보통 5분 정도 유예기간을 가진다.
- create vs apply
  - `kubectl create ~` 최초 생성
  - `kubectl apply ~` 수정 처리(만들어 진 것)

```shell
# 생성된 Pod에 포트포워딩 설정하기
kubectl portforward mypod 8080:80

# Pod에 주석 입력
# kubectl annotate pod mypod <key>=<value>
kubectl annotate pod mypod app=myweb

# Watch 모드
kubectl get pod -w

```

---

서비스 어카운트 ([링크](https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/))

- Pod가 쿠버네티스 API와 통신을 하기 위해 파드에 할당되는 ID 이다.
- 서비스 어카운트에 권한을 부여하여 쿠버네티스 API 통신을 할 수 있다.
- 서비스 어카운트 생성 시 시크릿이 생성된다.
  - 암호화된 데이터를 저장하는 리소스
  - 서비스 어카운트의 토큰 저장

RBAC (Role-Based Access Control, [링크](https://kubernetes.io/docs/reference/access-authn-authz/rbac/))

- 역할기반으로 API 접근을 관리한다.
  - 서비스 어카운트에 권한 관리를 바인딩(Binding)이라고 한다.
  - Role, ClusterRole 두가지로 분류
    - Role 특정 네임스페이스
      - RoleBinding
    - ClusterRole 전체 클러스터
      - ClusterRoleBinding

클러스터 업그레이드 ([링크](https://kubernetes.io/ko/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/))

```log
1) 마스터 노드 drain
2) 마스터 노드의 kubeadm 업그레이드
3) 마스터 노드의 kubectl, kubelet 업그레이드
4) 마스터 노드 uncordon
5) 워커 노드 drain
6) 워커 노드의 kubeadm 업그레이드
7) 워커 노드의 kubectl, kubelet 업그레이드(kubectl이 없을 경우 kubelet만 업그레이드)
8) 워커 노드 uncordon
```

CKA 요약 - https://github.com/jonnung/cka-practice

```shell
# Create an NGINX Pod
kubectl run nginx --image=nginx

# Generate POD Manifest YAML file (-o yaml). Don't create it(--dry-run)
kubectl run nginx --image=nginx -o yaml --dry-run=client > nginx_pod.yaml

# Create a deployment
kubectl create deployment nginx --image=nginx

# Generate Deployment YAML file (-o yaml). Don't create it(--dry-run)
kubectl create deployment nginx --image=nginx -o yaml --dry-run=client

# Create a Service named redis-service of type ClusterIP to expose pod redis on port 6379
kubectl expose pod redis --port=6379 --name redis-service --dry-run=client -o yaml
# 위 경우 자동으로 redis POD의 labels을 selector로 지정된다.
kubectl create service clusterip redis --tcp=6379:6379 -o yaml --dry-run=client
# 이렇게 Service를 만드는 경우 POD의 labels을 selectors에 지정되지 않지만 app=redis라는 labels을 추정하여 selectors로 지정된다.

# Create a Service named nginx of type NodePort to expose pod nginx's port 80 on port 30080 on the nodes:
kubectl expose pod nginx --port=80 --name nginx-service --type=NodePort --dry-run=client -o yaml
# 이 명령어에서 NodePort는 적용되지 않는다. 
kubectl create service nodeport nginx --tcp=80:80 --node-port=30080 --dry-run=client -o yaml
```

