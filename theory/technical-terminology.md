**마이크로 서비스 아키텍쳐 (MSA, Micro Service Architecture)**

> 하나의 큰 어플리케이션을 여러개의 작은 어플리케이션으로 쪼개어 변경과 조합이 가능하도록 만든 아키텍쳐

장점

- 추가 및 수정사항 반영이 빠르다.
- 기능별로 효율적인 처리가 가능하다.

단점

- 서로간의 통신에러가 작을 수 있다.
- 서비스간의 장애추적이 어렵다.

`반대개념 = 모놀리식(monolithic) 아키텍쳐`

---

**DHCP (Dynamic Host Configuration Protocol)**

> 네트워크에 연결된 PC에 자동으로 네임 서버 주소, IP 주소, 게이트웨이 주소를 할당해 주는 것을 의미하고 해당 클라이언트에게 일정 기간 임대를 하는 동적 주소 할당 프로토콜 이다.

장점

- IP를 효율적으로 사용
- IP 충돌을 예방

단점

- DHCP 서버가 다운되면 IP할당에 문제가 발생

---

**DNS (Domain Name System)**

> 네트워크에서 도메인이나 호스트 이름을 숫자로 된 IP 주소로 해석해 주는 TCP/IP Network Service인 DNS가 등장

- UDP와 TCP 포트 53번

  을 사용

  - UDP: 일반적인 DNS 조회
  - TCP: Zone Transfer(영역 전송)와 512Byte를 초과하는 DNS패킷을 전송해야 할 경우

- **Recursive DNS 서버**: 동일한 작업을 조건이 만족할때까지 반복적으로 처리한다.

- **Authoritative DNS 서버**: 관리/위임받은 도메인을 가지고 있는 네임서버를 말한다. (질의에 대한 응답만 수행)

**Root DNS/Local DNS**

전세계에 13대의 Root DNS 서버가 구축되어 있다고 한다.

미국 10대, 일본/네덜란드/노르웨이에 각각 1대씩 분포

국내에는 Root DNS 서버에 대한 미러 서버를 3대 운용중이라고 한다.

Local DNS의 경우 일반적으로 DHCP 서버로부터 IP 주소를 할당받을 때 DNS 주소도 함께 받는다.

**DDNS(Dynamic DNS)**

- 실시간으로 DNS 갱신
- 도메인 IP가 유동적인 경우 일반 DNS 주소 할당하면 사용자 IP가 바뀌는 순간 문제 발생
- 일반적으로 **유동 IP** 사용하는 인터넷 사용자들이 개인 서버나 NAS 구축 시 이용

---

**CDN (Contents Delivery Network)**

- 지리,물리적으로 떨어져 있는 사용자에게 컨텐츠를 더 빠르게 제공할 수 있는 기술
- 느린 응답속도 / 다운로딩 타임 을 극복하기 위한 기술
- CDN을 사용함으로써 서버의 트래픽 부하 및 비용을 줄이고 사용자에게 빠른 서비스 제공도 가능하다. 장애 확률도 낮춰 줄 수 있다.

**작동원리**

1. 최초 요청은 서버로 부터 컨텐츠를 가져와 고객에게 전송하며 동시에 CDN캐싱장비에 저장한다.
2. 두번째 이후 모든 요청은 CDN 업체에서 지정하는 해당 컨텐츠 만료 시점까지 CDN캐싱장비에 저장된 컨텐츠를 전송한다.
3. 자주사용하는 페이지에 한해서 CDN장비에서 캐싱이 되며, 해당 컨텐츠 호출이 없을 경우 주기적으로 삭제된다.
4. 서버가 파일을 찾는 데 실패하는 경우 CDN 플랫폼의 다른 서버에서 콘텐츠를 찾아 엔드유저에게 응답을 전송한다.
5. 콘텐츠를 사용할 수 없거나 콘텐츠가 오래된 경우, CDN은 서버에 대한 요청을 프록시로 작동하여 향후 요청에 대해 응답할 수 있도록 새로운 콘텐츠를 저장한다.

**필요기술**

- Load Balance
- 컨텐츠를 배포하는 기술
- CDN의 트래픽을 감지하는 기술

**CDN 캐싱방식**

- Static Caching
  - Origin Server에 있는 Content를 미리 Cache Server에 복사
- Dynamic Caching
  - 미리 복사하지 않고 Origin Server로 부터 다운로드
  - 일정 시간 이후 자료가 삭제될 수 있다

**CDN으로 전송가능한 컨텐츠**

- 디지털화될 수 있는 모든 데이터

**CDN서비스 이용방법**

- 소스코드상에서 이미지 링크나 리다이렉트등 CDN을 서비스를 이용할 도메인을 호출 하는 경우 도메인의 주소를 CDN 업체장비의 주소로 이미지를 호출하는 경로로 변경 한다.
- 서비스 신청 대상 도메인이 서버(Origin Server)를 바라보게끔 CDN장비주소로 연결 해주는 작업을 해야한다.

---

**DAS**

> 서버와 저장 장치를 직접 연결
> 소형 규모에 적합

- 안전성과 성능보장
- 제한된 확장성

**NAS**

> 서버와 저장장치가 네트워크로 연결
> 중규모에 적합

- 저렴한 비용, 간단히 적용가능, 파일공유 가능
- 네트워크가 불안정할 경우 트래픽 문제가 발생

**SAN**

> 서버와 저장장치를 광채널 스위치(Fiber Channel Switch)를 통해 고속 연결한 데이터 전용망
> 대규모에 적합

- 높은 처리속도
- 높은 비용, 관리부담 가중

---

**IaaS**

> 확장성이 높고 자동화된 컴퓨팅 리소스를 가상화하여 제공

- 제품
  - AWS, Azure, GCP
- 장점
  - 고정비 없음 / 자원 즉시 소비 / 확장 또는 축소가 자유로움

**PaaS**

> 주로 응용 프로그램을 개발할 때 필요한 플랫폼을 제공

- 제품
  - AWS Elastic Beanstalk, Windows Azure, Heroku, Google App Engine
- 장점
  - 비용감소 / 개발 및 배포 빠름 / 유지관리가 쉬움

**SaaS**

> 사용자에게 제공되는 소프트웨어를 가상화하여 제공

- 제품
  - Google Apps, Dropbox, Salesforce, WhaTap
- 장점
  - 비용감소 / 즉시사용 / 물리적 자원 필요 없음
- 단점
  - 커스텀마이징이 어렵다

---

**절차지향(Procedural Programming)**

> 순차적인 처리, 프로그램 전체가 유기적으로 연결되도록 만드는 프로그램 기법

장점

- 컴퓨터의 처리구조와 유사해 실행속도가 빠름

단점

- 유지보수가 어려움
- 실행 순서가 정해져 있으므로 코드의 순서가 바뀌면 동일한 결과를 보장하지 않음
- 디버깅이 어려움

**객체지향(Object Oriented Programming)**

> 실제 세계를 모델링 하여 개발하는 방법
> 3대 특성 = 캡슐화, 상속, 다형성

장점

- 코드의 재활용성이 높음
- 코딩이 절차지향보다 간편
- 디버깅이 쉬움

단점

- 처리속도가 절차지향보다 느림
- 설계에 많은 시간소요가 들어감

---

**캡슐화**

- 데이터와 알고리즘을 하나로 묶는 작업
- 관련 변수와 함수는 외부에서 쉽게 접근하지 못하도록 정보은닉을 하는 것이 핵심 (=getter,setter)

**상속**

- 상속은 이미 작성된 클래스를 이어 받아서 새로운 클래스를 생성하는 기법으로 기존 코드를 재활용해서 사용하는 것을 의미
- 객체지향 방법의 큰 장점중 하나 (=this, super)

**다형성**

- 다형성이란 하나의 이름(방법)으로 많은 상황에 대처하는 기법
- 개념적으로 동일한 작업을 하는 함수들에게 똑같은 이름을 부여할 수 있으므로 코드가 더 간단해 지는 효과 (=오버로딩, 오버라이딩)

---

**해시맵**

> 병렬처리를 하지 않거나 자원의 동기화를 고려하지 않는 상황에 사용

- 데이터 저장은 느리지만 많은 양의 데이터를 검색하는데 뛰어남
- map을 구현했으므로 key, value를 묶어서 하나의 데이터(entry)로 저장
- key 중복 허용이 안되고 value는 중복 허용
- key, value는 null을 허용하기 때문에 데이터가 누락되어도 문제되지 않음

**해시테이블**

> 병렬처리를 하면서 자원의 동기화를 고려해야 하는 상황에서 사용

- 빠르게 데이터를 검색할 수 있는 자료구조
- 배열에 고유한 index 생성, 값이 저장되는 곳은 버킷이나 슬롯

---

**프로세스(Process)**

- 실행 중인 하나의 프로그램을 의미
- 기본적으로 프로세스당 최소 1개의 스레드를 가지고 있다
- 프로세스는 각각 독릭된 메모리 영역(Code, Data, Stack, Heap)을 할당 받는다
- 한 프로세스가 다른 프로세스의 자원에 접근하려면
  프로세스 간의 통신(IPC, inter-process communication)을 사용한다.

**스레드(Thread)**

- 스레드는 한 프로세스 내에서 동작되는 여러 실행의 흐름으로, 프로세스 내의 주소 공간이나 자원들(힙 공간 등)을 같은 프로세스 내에 스레드 끼리 공유하면서 실행된다.
- 스레드는 프로세스 내에서 각각 Stack만 따로 할당받고, Code, Data, Heap 영역은 공유한다.

**멀티 프로세스**

> 다수의 프로세스를 실행

장점

- 하나의 프로세스가 비정상적으로 종료되더라도 다른 프로세스가 영향을 받지 않음
- 멀티 스레드 처럼 동기화 작업이 별도로 필요하지 않음

단점

- 자원 소모, 메모리 낭비, 문맥 교환으로 인한 비효율성
- IPC 통신으로 인한 비용

**멀티 스레드**

> 하나의 프로세스를 다수의 실행 단위로 나누어 실행

장점

- 문맥교환에 소비되는 시간을 줄일 수 있다.
  (스택 영역만 문맥교환이 일어남)
- 자원을 공유하기 때문에 메모리 낭비를 줄임

단점

- 동기화 작업이 필요
- 하나의 스레드가 비정상적으로 종료 시, 다른 스레드도 종료될 수 있다.

---

**가상화**

- 하이퍼바이저라는 SW를 이용하여 물리버신에서 가상머신을 만드는 프로세스
- 대상은 CPU, 메모리, 스토리지, 네트워크 등
  - 장점
    - 자원활용, 공간확보, 발열관리, 비용절감
  - 단점
    - 제조사 CPU에 종속 가능성
    - CPU 사용량이 많은 경우 이득이 없다
- 가상화 타입
  - 하이퍼바이저형 가상화
    - Type-1 가상화
      - HW에 직접 가상화 운영
      - 호스트 OS 없음
      - 적은 오버헤드, 리소스 관리가 유연
  - 호스트 가상화
    - Type-2 가상화
      - 호스트 OS에서 버추얼머신 설치 후 OS를 동작
      - OS가 두개 이상 들어가기 때문에 오버헤드 발생
  - 컨테이너 가상화
    - OS 레벨 가상화
    - 컨테이너 엔진으로 어플리케이션 실행 환경 격리
    - Docker
  
- 하드웨어 가상화 유무
  - HW 가상화 = 전 가상화
  - HW 가상화 없음 = 반 가상화

---

**컨테이너 (Container)**

> 컨테이너는 리눅스 기술을 사용하여 선박의 컨테이너 처럼 프로세스가 사용하는 자원을 격리 하는 것

- 가벼움
  - 배포 시간 단축
- 탄력성
  - 어느 환경에서든지 구동 가능
  - 개발 및 배포가 쉬워짐
- 유지 관리 효율
  - 로컬 OS에 적용된 패치는 모든 컨테이너에 적용된다.

---

**도커 (Docker)**

IT 소프트웨어인 "Docker”는 **Linux 컨테이너**를 만들고 사용할 수 있도록 하는 오픈소스 가상화 플랫폼 입니다.컨테이너를 매우 가벼운 **모듈식** 가상 머신처럼 다룰 수 있습니다. 
또한 컨테이너를 구축, 배포, 복사하고 한 환경에서 다른 환경으로 이동하는 등 **유연**하게 사용할 수 있어, 애플리케이션을 클라우드에 최적화하도록 지원합니다.

---

**쿠버네티스 (Kubernetes)**

- 2014 년 구글이 오픈 소스 공개
- 구글이 컨테이너 운영 노하우가 담긴 오픈소스
- 고대 그리스어로 항해사라는 의미를 가짐
- 다수의 컨테이너를 자동으로 운영하기 위한 오케스트레이션 도구

- **쿠버네티스 마스터**
  - 컨트롤러 매니저: 워커 노드 관리
  - API 서버: 워커 노드와 통신용
  - 스케줄러: 워커 노드에 포드 할당
  - Etcd: 클러스터 상태 및 설정 정보 저장소
- **워커 노드**
  - 포드: 작업 단위, 하나 이상의 컨테이너 포함
  - Kube-Proxy: 컨테이너간 네트워킹 및 로드밸런싱
  - Kubelet: 마스터 API와 통신하는 에이전트

---

쿠키와 세션

> Connectionless 하고 Stateless 한 HTTP 프로토콜을 사용하면서 Server가 Client를 **식별**할 수 있는 방법이 필요했고 쿠키와 세션을 사용하게 되었다.

**쿠키 (Cookie)**

쿠키는 클라이언트에 저장되는 **키와 값**이 들어 있는 작은 데이터 파일이다. 
쿠키에는 이름, 값, 만료 날짜, 경로 정보가 들어있다. 

쿠키는 **일정 시간동안** 데이터를 저장할 수 있어서 **로그인 상태를 유지**하거나 사용자 정보를 **일정 시간 동안 유지**해야 하는 경우에 주로 사용된다.

**세션 (Session)**

세션은 서버 메모리에 저장되는 정보다. 
서버에 저장되기 때문에 쿠키와는 달리 사용자 정보가 노출되지 않는다.

로그인 처리 과정을 순차적으로 보면,

1. 사용자가 로그인 페이지에 id / pw를 입력하고 로그인 버튼 클릭
2. 서버에서 사용자가 보낸 id / pw 정보를 확인하고 존재하는 사용자면 서버 메모리에 유일한 세션 ID를 생성하고 사용자 id와 매핑 정보를 저장
3. 클라이언트에 세션 ID를 쿠키로 저장
4. 요청시 마다 서버는 Request Header의 쿠키 정보(세션 ID)를 확인하고 세션 ID와 매핑되는 id의 사용자로 인식 

세션은 서버 메모리에 저장되지만 세션 역시 클라이언트에 쿠키로 저장된다는 것이 중요하다.

---

**LDAP (Lightweight Directory Access Protocol)**

인터넷 기반의 분산 디렉터리 서비스를 제공하는 공개된 프로토콜

**디렉터리 서비스**는?
이름을 기준으로 대상을 찾아 조회하거나 편집할 수 있는 서비스
DNS도 디렉터리 서비스의 일종, DNS는 도메인 이름으로 IP 주소를 조회

- 장점 : **쓰기 편하고**, **분산 구조**의 시스템에서 정보 **검색 비용이 적게** 든다는 장점이 있다.
- 단점 : **중간자 공격** 등의 문제가 있을 수 있다.

**Lightweight** 하다.

- 이 의미는 사용하기 간편하다는 의미가 아니라 통신 네트워크 대역폭 상의 가벼움을 의미 인터넷 프로토콜로 데이터를 조금만 주고 받아도 되게끔 설계되었다고 한다.
- LDAP의 요청의 99%는 검색에 대한 요청
- 디렉토리 안에는 연락처, 사용자, 파일, code 등 무엇이든 넣을 수 있고, insert, update 보다는 검색 요청에 특화되어 있다.

---

**스택 (Stack)**

스택(stack) 다음과 같은 성질을 갖는 자료형입니다.

- 데이터를 집어넣을 수 있는 선형(linear) 자료형입니다.
- **나중에 집어넣은 데이터가 먼저 나옵니다.** 
  이 특징을 줄여서 LIFO(Last In First Out)라고 부릅니다.
- 데이터를 집어넣는 push, 데이터를 추출하는 pop, 맨 나중에 집어넣은 데이터를 확인하는 peek 등의 작업을 할 수 있습니다.

스택은 서로 관계가 있는 여러 작업을 연달아 수행하면서 **이전의 작업 내용을 저장해 둘 필요가 있을 때** 널리 사용됩니다.

---

**큐 (Queue)**

큐(queue)는 다음과 같은 성질을 갖는 자료형입니다.

- 데이터를 집어넣을 수 있는 선형(linear) 자료형입니다.
- **먼저 집어넣은 데이터가 먼저 나옵니다.** 
  이 특징을 줄여서 FIFO(First In First Out)라고 부릅니다.
- 데이터를 집어넣는 enqueue, 데이터를 추출하는 dequeue 등의 작업을 할 수 있습니다.

큐는 **순서대로 처리해야 하는 작업을 임시로 저장해두는** **버퍼(buffer)**로서 많이 사용됩니다.

---

**트리 (Tree)**

**정의 :** Root를 중심으로 하위 노드들을 가지며 가지처럼 뻗어나가는 비선형, 비순환 구조

**사용처:**

- 검색: log(n)의 효율
- 인덱스: [B 트리](https://itwiki.kr/w/B_트리), [AVL 트리](https://itwiki.kr/w/AVL_트리), [T 트리](https://itwiki.kr/w/T_트리) 등
- 정렬: [Heap](https://itwiki.kr/w/힙) 구조 이용

----

**힙(heap)**

- 컴퓨터의 기억 장소에서 그 일부분이 [프로그램](http://terms.naver.com/entry.nhn?docId=833746&ref=y)들에 **할당되었다가 회수되는 작용이** [**되풀이**](http://terms.naver.com/entry.nhn?docId=823741&ref=y)되는 영역. 
- 스택 영역은 엄격하게 [후입 선출](http://terms.naver.com/entry.nhn?docId=827509&ref=y)(LIFO) 방식으로 운영되는 데 비해 
  힙은 프로그램들이 요구하는 블록의 크기나 요구/횟수 순서가 **일정한 규칙이 없다는 점**이 다르다. 
- 대개 히프의 기억 장소는 [지시자](http://terms.naver.com/entry.nhn?docId=858694&ref=y)(pointer) 변수를 통해 동적으로 할당받고 돌려준다.  이는 [연결 목록](http://terms.naver.com/entry.nhn?docId=848383&ref=y)이나 나무, 그래프 등의 동적인 [자료 구조](http://terms.naver.com/entry.nhn?docId=850544&ref=y)를 만드는 데 꼭 필요한 것이다.

---

**프로세스의 메모리 영역**

- Code
  - 코드 자체를 구성하는 메모리 영역 (프로그램 명령)
- Data
  - 전역변수, 정적변수, 배열 등 (초기화된 데이터)
- stack
  - 지역변수, 매개변수, 리턴 값 (임시 메모리 영역)
- Heap
  - 동적 할당 시 사용 (new(), mallock() 등)

---

**로드 밸런서 (load balancer)**

컴퓨터 네트워크 기술의 일종으로 여러 컴퓨터 자원들에게 작업을 나누는 것을 의미한다. 가용성 및 응답시간을 최적화 시킬 수 있다.

종류

- L2 = MAC 주소 기반
- L3 = IP 주소 기반
- L4 = TCP, UDP 기반
- L7 = HTTP, HTTPS, FTP 기반

동작 알고리즘

- Round Robin
  - 요청을 순서대로 돌아가며 배정
  - 세션이 오래 지속되지 않는 경우 적합
- 최소 리스폰 타임
  - 가장 짧은 응답시간을 보이는 서버에 우선 배정
  - 세션이 길어지는 경우 적합
- IP 해시 방식
  - IP주소를 특정 서버로 매핑하여 요청 처리
  - 항상 같은 서버로 연결 보장

---

**BGP (Border Gateway Protocol)** 

서로다른 AS(autonomous system) 사이에서 사용 되는 라우팅 프로토콜이다.
ISP 업체 연결하거나, 두개이상 ISP 동시 접속할때 (Multihoming), 
BGP 를 사용 한다.

- 라우팅정보를 유니캐스트 방식으로 전송한다. 
- TCP 179번을 사용함 ( 신뢰성 있는 통신을 함 )

---

**RDB**

관계형 데이터베이스며,
대표적으로 Mysql, Oracle 등이 가장 많이 알려진 RDB입니다.

특징

1) 테이블(Table) 마다 스키마(Schema)를 정의해야 됩니다.
2) 데이터 타입과 제약(Constraint)를 통해서 데이터의 정확성을 보장합니다.
3) SQL 질의문을 통해 요청을 처리합니다.
4) 성능을 높이려면 하드웨어(H/W)를 고성능으로 교체해야 된다. (Scale Up)
5) 고성능 하드웨어는 가격이 비싸기 때문에, RDB의 성능을 높이거나 확장하기 어렵기 때문에 확장성에 좋지 않습니다.

---

**NoSQL(Not only SQL)**

mongoDB의 경우 문서(document)형 데이터베이스로 많이 알려진 DB중 하나입니다. 또한 AWS DynamoDB 도 마찬가지로 NoSQL 중에 하나이다.

특징

1. RDB의 확장성 이슈를 해결하기 위해 나온 데이터베이스 모델입니다.
2. 분산 컴퓨팅 활용이 목적이고, 이것을 통해 비교적 저렴한 가격으로 DB 성능을 높일 수 있습니다. (Scale Out)
3. 여러 개의 테이블이 아닌, 큰 테이블 하나만을 사용합니다.
4. 가장 많이 쓰이는 NoSQL의 방식은 key-value방식으로 데이터를 관리합니다.
5. SQL 질의문을 사용하지 않습니다.
6. Schema-less (구조 변경이 용이하고, 데이터 형식이 다양하며, 바꾸기 쉬우며, 정확성 보다는 데이터 양이 중요한 빅데이터(Big Data)에 사용합니다.
7. 대표적으로 MongoDB(document-oriented), redies(key-value) 등이 있습니다.

---

**In-Memory DB**

In-Memory DB의 경우에는 NoSQL 방식에 속하는 데이터베이스 이며, key-value방식을 사용하고 있습니다.

특징
1) Memory의 가격이 용량 대비, 충분히 낮아지면서 빠른 데이터베이스 성능을 위해서 등장했습니다.
2) 디스크(Disk) 대신 메모리(Memory)를 사용함으로써, 
     I/O(input/output)의 성능을 높여줍니다.
3) 대표적으로 Redis 및 LMDB 등이 있습니다.

레디스(Redis)

- 인메모리 데이터베이스
- Key-Value 데이터 저장소

---

**고가용성(High Availability)**

정보 시스템이 상당히 오랜 기간 동안 지속적으로 정상 운영이 가능한 성질을 말한다. 고가용성을 제공하기 위해서 주로 2개의 서버를 연결하는 방식을 사용한다. 2개로 묶인 서버 중 1대의 서버에서 장애가 발생하면, 다른 서버가 즉시 그 업무를 대신 수행하므로, 시스템 장애를 불과 몇 초만에 복구할 수 있다.

- Active-Standby = 둘다 하나만 운영
- Active-Active = 둘다 운영

----

**3Tier Architecture(3계층 구조)**

3계층 구조(3 Tier Architecture)란 프레젠테이션 로직,비즈니스 로직, 데이터베이스 로직을 각각 다른 플랫폼 상에서 구현한 것이다.

- Client = 사용자 인터페이스, Front-end
- Application = 정보처리 규칙을 가짐, Back-end
- Data = 주로 데이터베이스를 가리킨다. Back-end

---

**DevOps란 무엇인가?**

DevOps는 Dev(개발)과 Ops(운영)이 합쳐진 용어입니다.
개발과 운영의 경계를 허물고 통합한다고 할 수 있습니다.
점차 기술 발전 속도가 빨라지면서 개발과 운영이 분리되어 생기는 병목을 없애고자 DevOps를 도입하는 기업들이 늘어나고 있습니다.

올바른 DevOps 문화를 위해 서비스 혹은 S/W LifeCycle 에서 반복적인 일들을 자동화 하고,팀간의 차이를 기술적으로 해소시키는 담당하는 사람

- 문화(Culture) - 사람, 서비스, S/W 라이프 싸이클
- 자동화(Automation) - 프로그래밍, 자동화 툴, 네트워크 등
- 측정(Measurement) - 테스트 및 데이터를 통한 추론
- 공유(Sharing) - 어떤 문제를 최단 시간의 해결하는 방법.
- 축적(File up and Pile up) - 재반복할 수 있는 이 문제에서 정확하게 회고하고, 축적해 나가는 것.

---

**클라우드 컴퓨팅(Cloud Computing)**

네트워크를 통해 다양한 IT리소스와 어플리케이션을 온디맨드로 제공하는 서비스

- IT리소스:서버, 스토리지,네트워크와 같은 IT의 기반 자원
- 온디맨드:요구사항에 따라 즉시 제공/공급 하는 방식(주문형)

---

**탄력성**

기본적인 클라우드의 속성 중 하나이며 최소한의 마찰로 리소스를 스케일링 가능하게 하는 특징

특히, 리소스를 서비스 양에 맞게 즉각적으로 늘리고 줄이는 프로세스를 자동화 하고 이용률을 높이는 작업을 적용한다.

----

**탄력성 있는 구성**

- 탄력성을 구현하기 위해 배포 절차를 자동화하고 구성을 간소화하는 프로세스 구성 필요
- 사용자의 개입 없이 확장 필요
- 실 사용량에 부합되는 자원을 제공
- 자원의 효율성과 비용 효율성을 가져온다.

**동시성 있는 구성**

- 클라우드에서는 동시성을 구현하는데 어렵지 않음
  - 동일한 시점에 데이터를 저장하면서 요청을 수행하는 작업을 실행가능
- 클라우드는 작업을 병렬화하고 자동화 할 수 있음

---

**웹 스케일**

글로벌 수준의 대규모의 환경에서도 높은 품질의 서비스를 영속적으로 제공하며 비즈니스의 요구사항에 맞춰 신속하고 안정적으로 IT자원을 설계, 구축 및 관리하는 패턴

---

**장애 요소(SPOF, Single Point Of Failure)**

단일 장애요소, 시스템 단일 구성 요소가 동작하지 않았을 때 전체 시스템에 영향을 주는 요소

> 클라우드 환경에서 설계를 할 때 장애가 발생 한다는 가정 하에 보수적으로 설계를 진행하고, 장애로부터 자동으로 복구, 복원이 가능하도록 시스템을 디자인 한다.

---

**Failover**

EIP(Elastick IP)와 Disk를 별도로 관리 가능하여 정상적인 상태의 서버로 대체

----

**부트스트랩(Bootstrap)**

자체 동작에 의해서 어떤 소정의 상태로 이행하도록 설정하는 방법

---

**멀티 테넌시(Multi-tenancy)**

특정 단위의 사용자들이 특정자원들 혹은 어플리케이션들의 무리적인 자원을 공유하며 서로의 환경에 대해 논리적으로 분리하고 접근을 제어하며 사용하는 구성환경


