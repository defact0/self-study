AWS Certified Cloud Practitioner

---

**클라우드 배포 모델**

- 클라우드 기반 배포
  - 애플리케이션 전부 클라우드에서 실행
- 온프레미스 배포
  - 프라이빗 클라우드 배포라고도 하며, 
    레거시 인프라와 달리 가상화 및 관리 기술이 통합되어 리소스 사용률을 높임
- 하이브리드 배포
  - 클라우드 리소스를 온프레미스 인프라와 연결

---

**클라우드 컴퓨팅이란?**

- 인터넷을 통해 IT 리소스와 애플리케이션을 온디맨드로 제공 (`종량 과금제`)

---

**Amazon Elastic Compute Cloud(Amazon EC2)**

- 동작방식
  - 시작
    - 인스턴스 시작 / 네트워크 트래픽 제어 / 보안설정
  - 연결
    - 인스턴스에 연결
  - 사용
    - 명령을 통해 SW, 스토리지, 파일복사 및 정리
- 인스턴스 유형
  - 범용 인스턴스
    - 리소스를 균형있게 제공
  - 컴퓨팅 최적화 인스턴스
    - 고성능 프로세서 제공
    - 배치 처리
  - 메모리 최적화 인스턴스
    - 고성능 데이터베이스에 적합
  - 엑셀러레이티드 컴퓨팅 인스턴스
    - 부동소수점 수 계산, 그래픽 처리, 데이터 패턴 일치
  - 스토리지 최적화 인스턴스
    - 데이터 웨어하우징 애플리케이션에 적합
- 요금
  - 온디맨드
    - 선결제, 최소약정 없음 / 사용 시간에 대해서만 비용 발생
  - Amazon EC2 Savings Plans
    - 1년 또는 3년 기간동안 일정한 사용량을 약정 / 온디맨드 요금 대비 72% 절감
  - 예약 인스턴스
    - 온디맨드를 사용시 적용되는 할인 옵션
  - 스팟 인스턴스
    - 시작, 종료가 자유롭거나 중단을 견딜 수 있는 워크로드에 적합 / 고객 설문조사 데이터 처리 작업
  - 전용 호스트
    - 가장 많은 비용 / 사용자 전용 물리서버
- Amazon EC2 Auto Scaling
  - 인스턴스를 자동으로 조정, 가용성을 효과적으로 유지
  - 접근 방식
    - 동적 조정
      - 수요 변화에 대응
    - 예측 조정
      - 예측된 수요에 따라 인스턴스를 자동으로 예약

---

**Elastic Load Balancing**

- 들어오는 애플리케이션 트래픽을 여러 리소스에 자동으로 분산하는 AWS 서비스
- 단일 Amazon EC2 인스턴스가 전체 워크로드를 처리하지 않아도 되도록 보장

---

**메시징 및 대기열**

- 모놀리식 애플리케이션
  - 모든 요소를 포함 / 장애가 발생하면 전체 장애가 발생할 수 있다.
- 마이크로 서비스
  - 단일 구성 요소에 장애가 발생하여도 가용성을 유지할 수 있도록 설계
  - Amazone SNS / Amazon SQS

---

**Amazon Simple Notification Service(Amazon SNS)**

- 게시/구독 서비스, 구독자 마다 필요한 맞춤형 정보만 전달

**Amazon Simple Queue Service(Amazon SQS)**

- 메시지 대기열 서비스, 은행 창구처럼 번호표 대기열 처리

---

**서버리스 컴퓨팅**

- AWS Lambda
  - 서버를 프로비저닝하거나 관리할 필요 없이 코드를 실행할 수 있는 서비스
  - 코드를 실행하는 동안에만 요금 발생
- Amazon Elastic Container Service(Amazon ECS)
  - 컨테이너식 애플리케이션을 실행하고 확장할 수 있는 확장성이 뛰어난 고성능 컨테이너 관리 시스템
- Amazon Elastic Kubernetes Service(Amazon EKS)
  - Kubernetes를 실행하는 데 사용할 수 있는 완전 관리형 서비스
- AWS Fargate
  - 컨테이너용 서버리스 컴퓨팅 엔진으로, Amazon ECS와 Amazon EKS에서 작동
  - AWS Fargate는 자동으로 서버 인프라를 관리 / 관련 리소스에 대해서만 비용발생

---

글로벌 인프라 및 안정성

- 리전(Region)
  - 고려사항
    - 데이터 거버넌스 및 법적 요구 사항 준수
    - 고객과의 근접성
    - 리전 내에서 사용 가능한 서비스
    - 요금
- 가용 영역
  - 리전 내의 단일 데이터 센터 또는 데이터 센터 그룹
  - 일부 가용 영역 장애가 발생하더라도 다른 가용 영역이 서비스를 유지시켜 준다.
- 엣지 로케이션
  - Amazon CloudFront가 더 빠른 콘텐츠 전송을 위해 고객과 가까운 위치에 콘텐츠 사본을 캐시하는 데 사용하는 사이트
    - Amazon CloudFront는 글로벌 콘텐츠 전송 서비스

---

**AWS 리소스를 프로비저닝하는 방법**

- AWS Management Console
  - 서비스 액세스 및 관리를 위한 웹 기반 인터페이스
- AWS 명령줄 인터페이스(AWS CLI)
  - 명령줄에서 직접 여러 AWS 서비스를 제어
- 소프트웨어 개발 키트(SDK)
  - API를 통해 AWS 서비스를 간편하게 사용

---

**AWS Elastic Beanstalk**

사용자가 코드 및 구성을 제공하면 아래와 같은 리소스를 배포한다.

- 용량 조절 / 로드 밸런싱 / 자동 조정 / 상태 모니터링

---

**AWS CloudFormation**

- 인프라를 코드로 취급, 코드를 작성하여 환경구축을 할 수 있다.

---

**AWS Outposts**

- AWS 인프라 및 서비스를 온프레미스 데이터 센터로 확장

---

**Amazon Virtual Private Cloud(Amazon VPC)**

- AWS 클라우드의 격리된 섹션을 프로비저닝할 수 있다.
- 가상 네트워크를 여러 리소스로 구성할 수 있다.
- 서브넷은 리소스를 포함할 수 있는 VPC 섹션

---

**가상 프라이빗 게이트 웨이**

- VPC 내의 비공개 리소스에 액세스하기 위함
- 가상 프라이빗 네트워크(VPN) 연결 설정이 필요

---

**AWS Direct Connect**

- 데이터 센터와 VPC 간에 비공개 전용 연결 서비스

---

**서브넷(subnet)**

- 퍼블릭 서브넷
  - 누구나 리소스에 액세스 가능
- 프라이빗 서브넷
  - 고객의 개인정보나 주문내역 같은 정보를 액세스하기 위함
  - VPC 내에서 서브넷 끼리 서로 통신 가능 (public <--> private)
- VPC의 네트워크 트래픽
  - 데이터 요청은 패킷으로 전송(데이터 단위)
  - 패킷이 서브넷 을 통해 이동하려면 권한이 필요한데 네트워크 ACL를 통해 제어

---

**네트워크 ACL (액세스 제어 목록)**

- 가상 방화벽, 인바운드 아웃바운드 트래픽을 제어
- 기본 ACL는 모든 트래픽 허용
- 사용자 ACL은 모든 트래픽을 거부, 추가하면서 허용
- **상태 비저장 패킷 필터링**
  - 아무것도 기억하지 않고 서브넷 경계를 통과하는 패킷만 확인
