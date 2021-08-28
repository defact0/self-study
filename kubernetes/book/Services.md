### :ship: 네트워킹

> 쿠버네티스에서 Service 리소스는 네트워크를 담당한다.

- YAML 형태로 리소스를 정의
- Pod IP와 다른 독자적인 IP를 부여받아 서비스의 끝점(Endpoint)를 제공
- 라벨링 시스템을 통해 Pod로 트래픽 전달 (=로드 밸런서 처럼 동작)

왜, Service 리소스가 있는 걸까?

> Pod 리소스는 불안정한 자원으로 여긴다.
> 필요하면 쉽게 생성했다가 쉽게 삭제 가능한 리소스 이기 때문이다.

이러한 Pod의 생명주기와 상관 없이 안정적인 Endpoint를 제공하는 Service리소스가 등장하게 되었다.

- 리버스 프록시와 같은 역할 수행 ([참고](https://firework-ham.tistory.com/23))

  > Client & Server 구조에서 Server로 요청되는 것을 대신 받아 원래의 Server로 전달해 주는 대리 서버
  > Server로 요청되는 부하를 분산, 보안을 높일 수 있다.

- <u>Pod의 IP가 변경되더라도 사용자 입장에서는 Service 리소스를 통해 동일한 IP로 접근 가능</u>

  - Pod의 트래픽 분산처리로 인하여 안정성과 가용성을 높일 수 있다.

서비스 탐색(Service Discovery)

- Service 리소스의 이름을 기반으로 DNS 참조 가능
- service 정의 yaml 살펴보기
  - `spec.ports.port`는 service의 포트들을 정의
  - `spec.ports.protocol`은 사용하는 프로토콜 지정
  - `spec.ports.targetPort`은 트래픽을 전달할 컨테이너
  - `spec.selector.run`은 트래픽을 전달할 컨테이너 라벨 선택
    - 느슨한 연결관계(loosely coupled) = 간접 참조를 위함

생성된 Service 리소스 조회

```shell
kubectl get service
# service 이름이 myservice으로 생성됨을 가정

# 테스트 전용 Pod 생성
kubectl run client --image nginx
kubectl exec client -- curl 10.42.0.226       # Pod IP로 접근
kubectl exec client -- curl 10.43.152.73:8080 # Service IP로 접근(CLUSTER-IP)
kubectl exec client -- curl myservice:8080    # Service 이름(DNS주소)로 접근
```

- DNS의 이름이 단순히 myservice가 아니라 `myservice.default.svc.cluster.local`로 나오는 것을 확인 할 수 있다. (nslookup 으로 조회)
  - 전체 도메인 주소를 나타냄

Service 도메인 주소 법칙

```log
<서비스 이름>.<네임 스페이스>.svc.cluster.local
```

 클러스터 DNS 서버

- 쿠버네티스에서 제공하는 DNS 서버가 있다

  - /etc/resolv.conf

    ```shell
    # 로컬 호스트가 아닌 Pod의 DNS 설정 확인
    kubectl exec client -- cat /etc/resolv.conf
    
    # kube-system 조회 (CLUSTER-IP 확인)
    kubectl get svc -- kube-system
    kubectl get svc -- kube-system --show-labels
    kubectl get svc -- kube-system -l k8s-app=kube-dns
    ```

    - `coredns`는 쿠버네티스에서 제공하는 클러스터 DNS 서버

Service 종류

- **ClusterIP**

  - 기본 타입

  - endpoint는 쿠버네티스트 내부에서만 접근가능(외부에서 접근불가)

    - 직접 트래픽을 전달 받는 경우가 드물다
    - ClusterIP를 기반으로 더 복잡한 네트워킹 수행하도록 함

  - service를 생성

    ```shell
    # cluster-ip service 생성 (Pod도 같이 생성)
    kubectl run cluster-ip --image nginx --expose --port 80 \
        --dry-run=client -o yaml > cluster-ip.yaml
    vi cluster-ip.yaml
    kubectl apply -f cluster cluster-ip.yaml
    
    # cluster-ip service 조회
    kubectl get svc cluster-ip -o yaml | grep type
    kubectl exec client -- curl -s cluster-ip
    ```

    

- **NodePort**

  - 도커 컨테이너 포트 매핑과 비슷함
    - 로컬 호스트의 특정 포트를 Service의 특정 포트와 매핑시켜 외부 트래픽을 Service까지 전달
  - yaml 파일 내용
    - `spec.type: Nodeport` 신규 추가
    - `spec.ports.nodePort: 30080` 호스트(노드)의 포트 지정
      - NodePort range는 30000~32767 이다.

- **LoadBalancer**

  - <u>클라우드 플랫폼의 LoadBalancer 서비스를 Service 리소스에 연결</u>
  - 노드 앞단에 LoadBalancer를 위치시키고, 각 노드로 트래픽을 분산할 수 있게 LoadBalancer Type을 제공
    - 보안적인 측면에서, 서버의 노드포트 대역을 외부에 공개할 필요가 없다.
    - 각각의 서버 IP를 직접 알 필요가 없다. 로드밸런서의 IP 또는 도메인만 알고 있으면 된다.
  - yaml 파일 내용
    - `spec.type: LoadBalancer`
  - EXTERNAL-IP 생성
    - `kubectl get svc load-bal` 확인 시 EXTERBAL-IP 부분에 IP정보가 출력됨

- `ExternalName`

  - 외부 DNS 주소에 클러스터 내부에서 사용할 별칭을 만든다.

  - `abc-svc`를 `abc.com` 으로 연결  할 수 있는 서비스 끝점을 생성 해보자

    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
      name: abc-svc
    spec:
      type: ExternalName
      externalName: abc.com
    ```

  - ExternalName은 쿠버네티스 클러스터에 편입되지 않는 외부 서비스에 쿠버네티스 네트워킹 기능을 연결하고 싶은 경우 사용

**리눅스 커널의 netfilter**

- kube-proxy는 netfilter를 이용하여 커널레벨에서 특정 트래픽을 중간에 가로채어 다른 곳으로 라우팅 함
- 모든 노드에서 동일한 NodePort로 원하는 서비스에 접근할 수 있게 제공

네트워크 모델 특징

- 각 Node간 NAT 없이 통신 가능
- 각 Pod간 NAT 없이 통신 가능
- Node와 Pod간 NAT 없이 통신 가능
- 각 Pod는 공유의 IP를 부여받음
- 각 Pod IP 네트워크 제공자(network provider)를 통해 할당
- Pod IP는 클러스터 내부 어디서든 접근 가능

네트워크 모델 장점

- 모든 리소스(Node, Pod)가 다른 모든 리소스(Node, Pod, Service)를 고유의 IP로 접근 가능
- NAT 통신의 오류에 대해 신경 쓸 필요 없음
- 새로운 프로토콜 정의 없이 기존의 TCP,UDP,IP 프로토콜 이용
- Pod끼리 네트워킹이 어느 노드에서든지 동일하게 동작
  - 종속성이 없기 때문에 이식성이 높음



