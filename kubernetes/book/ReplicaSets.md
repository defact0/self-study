### :ship: 컨트롤러

> 리소스의 생명주기에 따라 미리 정해진 작업을 수행하는 주체
> : 현재 상태(current state)와 바라는 상태(desired state)에 대해 알아야 한다.

에어컨을 예시로 들자면 현재 온도, 희망 온도가 있다.

- 에어컨 = 컨트롤러
- 현재 온도 =  current state
- 희망 온도 = desired state

에어컨은 지속적으로 돌면서 사용자의 희망 온도 요청에 따라 <u>현재 온도가 희망 온도가 동일해 지도록 작업을 수행</u> 

ReplicaSet

- Pod를 복제(replicate)한다.

  - 1개의 Pod에 문제가 발생하더라도 다른 Pod를 이용할 수 있도록
  - 안정적인 서비스 운영을 위해 가용성을 높이는 역할을 담당

- yaml 정의서

  ```yaml
  apiVersion: apps/v1
  kind: replicaSet
  metadata:
    name: myreplicaset
  spec:
    replicas: 2
    selector:
      matchLabels:
        run: nginx-rs
      template:
        metadata:
          labels:
            run: nginx-rs
        spec:
          containers:
          - name: nginx
            image: nginx
  ```

  - `replicas` 복제할 Pod의 개수 정의
  - `selector.matchLabels` 라벨링 시스템을 이용하여 Pod를 선택
  - `template` 복제할 Pod를 정의

- ReplicaSet 명령

  ```shell
  # 조회
  kubectl get replicaset
  
  # 개수 늘리기
  #   kubectl scale rs --replicas <number> <name>
  kubectl scale rs --replicas 4 myreplicaset
  
  # 전부 삭제
  kubectl delete rs --all
  ```

  - Deployment 리소스도 ReplicaSet 리소스를 사용한다.
  - `replicas`에 의해 생성된 Pod를 하나 삭제해도 그 갯수는 원상복구 한다.

Deployment

- 롤링 업데이트를 지원하고 롤릴 업데이트 되는 Pod의 비율을 조정할 수 있다.
- 업데이트 히스토리를 저장하고 다시 롤백할 수 있는 기능 제공
- ReplicaSet과 마찬가지로 Pod의 개수를 늘릴 수 있다. (scale out)
- 배포 상태를 확인할 수 있다.

```yaml
apiVersion: app/v1
kind: Deployment
metadata:
  name: mydeploy
spec:
  replicas: 10
  selector:
    matchLabels:
      run: nginx
    strategy:
      type: RollingUpdate
      rollingUpdate:
        maxUnavailable: 25%
        maxSurge: 25%
    template:
      metadata:
        labels:
          run: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.7.9     
```

- `strategy.type` 배포전략 종류를 선택
  - RollingUpdate
    - 점진적으로 업데이트
    - `strategy.rollingUpdate.maxUnavailable`
      - 최대 중단 Pod 허용 개수(or비율)
      - 약 2개(소수점 내림)
    - `strategy.rollingUpdate.maxSurge`
      - 최대 초과 Pod 허용 개수(or 비율)
      - 약 3개(소수점 올리)
    - 위 설정대로 하면 최소 8개, 최대 13개 까지 Pod가 점진적으로 업데이트가 된다.
  - Recreate
    - 일시적으로 전체 Pod가 삭제되고 새로운 Pod가 생성

```shell
# Deployment 리소스 생성, record 옵션 추가 사용
kubectl apply --record -f mydeploy.yaml

# Deployment 정보
kubectl get deployment

# ReplicaSet 정보
kubectl get rs
# Pod 정보
kubectl get pod
```

- Deployment : 배포담당
- ReplicaSet : 복제담당
- Pod : 컨테이너 실행 담당

롤링 업데이트 작업

- nginx 버전을 1.7.9 에서 1.9.1로 업그레이드

```shell
# 이미지 주소 변경
# kubectl set image deployment <NAME> <CONTAINER_NAME>=<IMAGE>

# nginx 업데이트
kubectl set image deployment mydeploy nginx=nginx:1.9.1 --record

# 배포상태 확인
kubectl rollout status deployment mydeploy

# 특정 Pod의 이미지 tag 정보 확인
kubectl get pod mydeploy-xxx-xxx -o yaml | grep "image: nginx"
```

- 한번에 모든 Pod가 업데이트가 되는 것이 아닌 점진적으로 새로운 Pod가 생성된다.
- Service 리소스의 안정된 서비스 끝점을 통해 중단 없이 어플리케이션을 배포할 수 있다.

롤링 업데이트 롤백

- 이전 작업이 잘못되어 신규 Pod가 비정상 상태
- maxUnavailable 옵션으로 인하여 8개의 Running 상태의 Pod를 유지 중

```shell
# 지금까지 배포 히스토리를 확인
kubectl rollout history deployment mydeploy

# 롤백
kubectl rollout undo deployment mydeploy

# 확인
kubectl rollout history deployment mydeploy
kubectl get deployment mydeploy -o yaml | grep image

# 배포 버전(revision)을 명시하여 롤백
kubectl rollout undo deployment mydeploy --to-revision=1
```

- `--record` 옵션을 붙인 이유가 `rollout history`에서 실제 사용한 명령을 기록, 옵션이 없으면 `<NONE>`으로 표시
- `rollout undo` 명령을 통해 이전 배포상태로 롤백

배포된 Pod의 개수 조절하기

```shell
# kubectl scale deployment --replicas <NUMBER> <NAME>
kubectl scale deployment mydeploy --replicas=5

# 확인
kubectl get pod

# 직접 YAML 파일 수정
kubectl edit deploy mydeploy
```

쿠버네티스 리소스 컨셉

- 컨테이너를 실행하는 Pod
- 네트워킹을 책임지는 Service
- 복제를 담당하는 ReplicaSet
- 배포를 관리하는 Deployment

StatefulSet

- 상태정보를 저장하는 application에서 사용하는 리소스
- Deployment와 다른 점은 Pod의 순서와 고유성을 보장
  - 고유의 Pod 식별자가 필요한 경우
  - 명시적으로 Pod마다 저장소가 지정되어야 하는 경우
- Pod끼리의 순서에 민감한 application
- application이 순서대로 업데이트 되어야 하는 경우

> StatefulSet은 Pod 끼리 명시적으로 순서와 식별자를 부여받는 점

```shell
kubectl get statefulset # 축약시, sts
```

DeamonSet

- 모든 노드에 동일한 Pod를 실행시키고자 할 때 사용하는 리소스
  - 리소스 모니터링, 로그 수집기 등으로 사용
- `spec.selector.matchLabels` 라벨링 시스템을 이용하여 노드에서 노드 실행될 Pod를 선택
- `spec.template` 모든 노드에서 생성될 Pod를 정의

```shell
kubectl get daemonset # 축약시, ds
```

Job & CronJob

- Job

  - 한번 실행하고 완료되는 일괄처리 프로세스

    - `spec.template` Pod 리소스의 spec과 동일
    - `spec.backoffLimit` 재시도 횟수를 지정 (재시도가 끝나면 최종적으로 실패기록)
      - 만일 2로 설정되어 있다면, 첫시도 + 2번 재시도 = 3번 실행된다.

  - 명령

    ```shell
    kubectl get job
    ```

    - 완료된 이후에 `Running`이 아니라 `Completed`로 남아있는다.

- CronJob

  - 주기적으로 Job을 실행할 수 있도록 확장된 리소스

    - `spec.schedule` 실행할 주기 설정
    - `spec.jobTemplate` job 리소스에서 사용하던 스펙을 동일하게 사용

  - 명령

    ```shell
    kubectl get cronjob
    ```

    



