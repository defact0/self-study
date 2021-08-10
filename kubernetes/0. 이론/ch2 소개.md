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



