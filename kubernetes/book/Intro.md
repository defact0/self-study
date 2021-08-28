### :ship: 쿠버네티스 소개

쿠버네티스란?

- 여러 서버로 구성된 클러스터 환경을 관리하기 위한 오케스트레이션(Orchestration) 플랫폼
- 컨테이너는 호스트 운영체제를 공유 한다.
- CNCF (Cloud Native Computing Foundation) 재단의 첫번째 프로젝트 (구글이 기증함)
- 쿠버네티스를 데이터 센터 운영체제라고 정의한다.

바라는 상태(Desired State)

- 에어컨을 예를 들면 현재 온도, 사용자 희망 온도가 있다.
  - 쿠버네티스에서 사용자의 요청에 따라 희망하는 상태를 맞추기 위해 작업을 수행한다.
- 이런 작업을 통해 자가 치유를 할 수 있다.

컨트롤러(Controller)

- 현재 상태를 바라는 상태로 변경하는 주체
- control-loop라는 루프를 돌며 리소스를 지속적으로 모니터링

쿠버네티스 리소스(Resource)

- 모든 것들을 리소스(Resource)로 표현, 각각의 역할이 있다.
- 기본 리소스는 Pod (최소 실행 단위)

선언형 커맨드(Declarative Command)

- 사용자가 바라는 상태를 선언적으로 기술하여 명령을 내리는 방법 (What) 
  - 예를 들면 html이 선언형 커맨드, 무엇을 수행해야 하는지 선언이 있다.
  - YAML 형식을 이용하여 선언형 명령을 내린다. (= YAML 정의서)
    - 설정을 전부 작성할 필요가 없다. 없는 것은 자동으로 만들기 때문에
  - 반대개념은 명령형(Imperative) 커맨드 (How)
    - 예를 들면 sql 쿼리가 명령형 커맨드

네임스페이스(Namespace)

- 클러스터를 논리적으로 분리하는 개념
- 네임스페이스 레벨 리소스 vs 클러스터 레벨 리소스
  - 네임 스페이스 리소스
    - 특정 네임스페이스 안에 속하여 존재
    - 대부분의 리소스가 포함
    - 자유롭게 추가, 삭제 가능
  - 클러스터 리소스
    - Node, PersistentVolume, StorageClass

라벨&셀렉터(Label&Selector)

- 리소스 질의 체계
- 라벨링 시스템은 key-value 형식의 태그정보
- 태깅한 리소스를 찾기 위해 셀렉터를 사용하여 특정 key-value를 가진 리소스만 추출
- 쿠버네티스는 리소스간의 관계가 느슨하게 연결(loosely coupled)되어 유연한 구조를 가짐

서비스 탐색

- 클러스터내에서 통신을 위해 어디서든 접근 가능한 서비스 끝점(Service Endpoint)가 필요
  - 서비스 끝점(Service Endpoint)를 통해 다른 컨테이너와 통신 가능
- 서비스 끝점(Service Endpoint)정보를 알아내는 것이 서비스 탐색(Service Discovery)
  - DNS기반 탐색지원, 도메인 주소를 기반으로 서비스 접근
  - Service 라는 리소스를 사용

설정관리

- 필요한 설정값 및 민감 정보(credentials)를 플랫폼 레벨에서 관리지원
- ConfigMap 또는 Secret이라는 리소스로 설정들을 관리

쿠버네티스 마스터

- 핵심 컴포넌트들이 존재
  - kube-apiserver
    - 핵심 역할, 모든 이벤트에 대한 응답
  - etcd
    - 분산형 key-value 저장소
  - kube-scheduler
    - 컨테이너 스케쥴링 담당
  - kube-controller-manager
    - control-loop를 돌며 현재 상태(current state)와 바라는 상태(desired state)를 비교
    - 전반적인 리소스의 라이프사이클 담당
  - cloud-controller-manager
    - 클라우드 플랫폼에 특화된 리소스 제어

쿠버네티스 노드

- 마스터로 부터 명령을 전달 받아 컨테이너를 실행
  - kubelet
    - 노드 관리자, 메인 컴포넌트, 마스터로 부터 상세 명세(spec)를 받아 실행
    - 지속적인 모니터링
    - api 서버와 통신하며 리소스 정보를 서로 주고 받음
  - kube-proxy
    - 네트워크 프록시
    - 서비스 마다 개별 IP 부여, 클러스터 내/외부의 트래픽을 Pod로 패킷을 라우팅
  - container runtime
    - 컨테이너 실행 환경
    - CRI(Container Runtime Interface) 규약을 지켜야 한다.

쿠버네티스의 장점

- 실행 환경 고립화
- 리소스 관리
- 스케줄링
- 프로세스 관리
- 통합 설정 관리
- 손쉬운 장애 대응
- 자동 확장
- 하이브리드 클라우드 운영
- 자가 치유
- 데이터 스토리지 관리
- 배포 자동화

컨테이너 실행

```shell
# kubectl run <NAME> --image <IMAGE>
kubectl run mynginx --image nginx
```

- [nginx](https://opentutorials.org/module/384/3462)에 대해 알고 싶으면 클릭!

컨테이너 조회

```shell
kubectl get pod

# Pod의 상세정보
kubectl get pod mynginx -o yaml

# Pod의 IP정보
kubectl get pod -o wide
```

컨테이너 상세정보

```shell
# kubectl describe pod <NAME>
kubectl describe pod mynginx
```

- get과 다른 점은 Pod에 대한 Events 기록까지 확인

컨테이너 로깅

```shell
# kubectl logs <NAME>
kubectl logs -f mynginx
```

- -f 옵션은 종료되지 않고 계속 로그가 출력

컨테이너 명령 전달

```shell
# kubectl exec <NAME> -- <CMD>
kubectl exec mynginx -- apt-get update
kubectl exec -it mynginx -- bash
```

- 명령어 전달시 구분자(--)로 전달할 명령을 구분한다.
- -it 옵션을 사용하여 컨테이너 내부로 접속

컨테이너와 호스트간 파일복사

```shell
# kubectl cp <TARGET> <SOURCE>
kubectl cp /etc/passwd mynginx:/tmp/passwd

# 복사 확인
kubectl exec mynginx -- ls /tmp/passwd
kubectl exec mynginx -- cat /tmp/passwd
```

컨테이너 정보 수정

```shell
# kubectl edit pod <NAME>
kubectl edit pod myngix
```

- 수정 내용이 바로 컨테이너에 반영된다.

컨테이너 삭제

```shell
# kubectl delete pod <NAME>
kubectl delete pod mynginx

# Clean up
kubectl delete pod --all
```

선언형 명령 정의서(YAML) 기반의 컨테이너 생성

```shell
# kubectl apply -f <FILE_NAME>
kubectl apply -f mynginx.yaml
```

- <FILE_NAME>부분에 인터넷에 위치한 yaml 경로를 입력해도 적용된다.
- apply 명령은 멱등성 보장, 여러번 실행하더라도 yaml 정의서에 있는 내용과 동일한 결과

Service 리소스

```shell
kubectl get service
kubectl describe service kubernetes
```

Node 리소스

```shell
kubectl get node
kubectl describe node master
```

Namespace 리소스

```shell
kubectl get namespace
kubectl describe namespace kube-system
```

- namespace 종류
  - default
  - kube-system
  - kube-public
  - kube-node-lease

```shell
kubectl run mynginx-ns --image nginx --namespace kube-system

# [Tip] namespace 옵션은 n으로 줄여써도 된다.
# kube-system 네임스페이스에서 Pod 확인
kubectl get pod mynginx-ns -n kube-system

# kube-system 네임스페이스에 있는 mynginx-ns Pod 삭제
kubectl delete pod mynginx -n kube-system
```

- 네임스페이스 옵션을 안쓰면 default 네임스페이스로 동작한다.

자동완성

- kubectl 명령을 매번 입력이 불편하여 명령어를 자동완성시켜주는 스크립트를 제공해 준다.
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#enable-kubectl-autocompletion

즉석 리소스 생성

- YAML 명령 정의서를 cat &  here document 명령 조합으로 즉석으로 리소스 생성

```shell
cat << EOF | kubectl apply -f -
# YAML 내용
EOF
```

리소스 특정 정보 추출

- --jsonpath 옵션 사용, 특정 정보만 골라서 출력

```shell
kubectl get node master -o jsonpath="{.status.addresses[0].address}"

# 모든 노드의 외부IP를 조회
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'
```

모든 리소스 조회

```shell
kubectl api-resources
kubectl api-resources --namespaced=true
```

리소스 정의 설명

```shell
kubectl explain pods
```

클러스터 상태 확인

- health check, 트러블 슈팅 시 사용

```shell
# 쿠버네티스 API서버 작동 여부 확인
kubectl cluster-info

# 전체 노드 상태 확인
kubectl get node

# 쿠버네티스 핵심 컴포넌트의 Pod 상태 확인
kubectl get pod -n kube-system
```

클라이언트 설정 파일

- KUBECONFIG ($HOME/.kube/config) 설정 파일 참조

```shell
# kubectl config <SUBCOMMAND>
kubectl config view
```

- 크게 3가지 영역으로 구분된다.
  - clusters
  - users
  - contexts

