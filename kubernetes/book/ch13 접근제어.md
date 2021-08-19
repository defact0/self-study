### :ship: 접근제어

> 접근제어는 누가 접근하고 있으며 어떤 권한을 가지고 접근하는지 확인하여 정책에 따라 허가 여부를 결정하는 일연의 과정이다.

과정

1. Authentication
   - 누가 접근하고 있는지 신분 확인
2. Authorization
   - 어떤 권한을 가지고 있는지 확인
3. Admission Control
   - 요청 내용이 적절한지(valid) 확인
   - `LimitRage`, `ResourceQuota`

---

사용자 인증 (Authentication)

- 인증방식
  1. HTTP Authentication
  2. X.509 Certificate
  3. OpenID Connection
  4. Webhook 인증
  5. Proxy 인증
- HTTP Basic Authentication
  - HTTP 을 통해 인증
  - KUBECONFIG
    - 마스터 API 서버와 통신하기 위해 필요한 정보 파일
    - `$HOME/.kube/config`에 위치
- X.509 Certificate
  - HTTPS 을 통해 인증
  - 쿠버네티스가 인증한 사용자 인증서를 사용하여 접근
    - CA (Certificate Authority)
      - 인증서 발급(Issuer)
    - CSR (Certificate Signing Request)
      - CA로 부터 인증서 서명 요청하는 문서
    - 사용자 인증서는 cfssl 툴을 통해 생성

---

역할 기반 접근 제어(RBAC)

- Authorization 단계 이후 역할 기반 접근 제어(Role Based Access Control) 사용자 권한 관리
  - Role (ClusterRole)
    - 어떤 권한을 소유하고 있는지
  - Subjects
    - Role 부여대상
  - RoleBinding (ClusterRoleBinding)
    - Role과 Subject의 연결(Binding)

---

Role (ClusterRole)

- Role 리소스
  - 네임스페이스 안에서 역할을 정의
- ClusterRole 리소스
  - 클러스터 레벨로 역할을 정의
  - `metadata`에 따로 `namespace`를 입력하지 않는다.

> 1. `Role` or `ClusterRole`를 먼저 만든다.
> 2. `RoleBinding` or `ClusterRoleBinding`을 만든다.
>    - Role = 작업범위가 `네임스페이스`
>    - ClusterRole = 작업범위가 `클러스터`

---

Subjects

- Subjects는 Role을 부여 받을 객체

  - User / Group / ServiceAccount

    - User = 개념적으로 존재, Common Name(CN)
    - Group = 개념적으로 존재, Organization(O)

  - ServiceAccount

    - 명시적으로 구현되어 있는 리소스

      ```shell
      kubectl get serviceaccount
      ```

    - 네임스페이스 레벨에서 동작

    - Pod 와 쿠버네티스와 통신할 때 사용하는 신원(Identity) 용도로 사용

---

네트워크 접근 제어 (Network Policy)

- Pod의 네트워크 접근을 제어할 수 있는 매커니즘
- 일부 제품만 지원
  - Weave, Calico

쿠버네티스 네트워크 기본 정책

- 클러스터에 네트워크 정책이 설정되어 있지 않다
- 설정이 없으면 네임스페이스의 모든 트래픽이 열려 있다
- 1개의 네트워크 정책이라도 설정 되면 정책의 영향을 받는 Pod에 대해서 해당 네트워크 정책 이외의 나머지 트래픽은 전부 막힌다.(default-deny)

네트워크 구성

- Private Zone
  - 전체 인바운드 트래픽을 차단, 외부 트래픽이 들어올 수 없게 private zone 생성
    - `ingress: []` 설정의 의미는 허용하는 인바운드 정책이 없다.
- Egress
  - 아웃바운드 트래픽 제어
- AND & OR 조건 비교
  - AND 조건
    - `from property`리스트 원소를 2개의 `podSelector`로 선언
  - OR 조건
    - `ingress property`아래의 각각 `from`으로 선언

---



