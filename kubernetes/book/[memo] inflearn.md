kubernetes memo

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

Pod

- 생성된 Pod에 포트포워딩 설정하기

  ```shell
  kubectl portforward mypod 8080:80
  ```

  

- Pod에 주석 입력

  ```shell
  # kubectl annotate pod mypod <key>=<value>
  kubectl annotate pod mypod app=myweb
  ```

  

- Watch 모드

  ```shell
  kubectl get pod -w
  ```

  

---

디플로이먼트 소개와 연습문제
