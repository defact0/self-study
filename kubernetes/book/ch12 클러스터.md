### :ship: 클러스터 관리

> **리소스 관리**
> 이번 챕터는 쿠버네티스 리소스가 아니라 노드의 CPU, 메모리 같은 리소스를 말한다.

리소스 관리

- 네임스페이스 (가상의 논리 클러스터)로 리소스를 관리
- 리소스 관리 담당
  - `LimitRage`
  - `ResourceQuota`
- 앞서, Pod의 `resource property`를 통해 리소스를 관리하는 방법에 대해 알아 보았다

---

LimitRage

- 기능
  - 일반 사용자가 리소스 사용량 정의를 생략하더라도 자동으로 Pod의 리소스 사용량을 설정
  - 관리자가 설정한 최대 요청량을 일반 사용자가 넘지 못하게 제한
- 일반 사용자의 Pod 리소스 설정을 통제하는 리소스

```yaml
# limit-range.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: limit-range
spec:
  limits:
  - default:
      cpu: "400m"
      memory: "512Mi"
    defaultRequest:
      cpu: "300m"
      memory: "256Mi"
    max:
      cpu: "600Mi"
    min:
      cpu: "200Mi"
    type: Container
```

- `default` 생략 시 기본 사용되는 설정
- `defaultRequest` 기본 `request` 설정
- `max`사용자가 요청하는 최대치
- `min`사용자가 요청하는 최소치

> 강제로 LimitRange에 벗어난 리소스를 설정하면 Pod 생성 에러가 발생한다.

---

ResourceQuota

- LimitRage는 개별 Pod 생성에 관여 했다면, `ResourceQuota`는 전체 네임스페이스에 대한 제약 설정을 한다.
  - 클러스터 관리자가 특정 네임스페이스의 전체 리소스 사용량 제한 설정

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: res-quota
spec:
  hard:
    limit.cpu: 700m
    limit.memory: 800Mi
    request.cpu: 500m
    request.memory: 700Mi
```

default 네임스페이스

- Pod 전체 총합이 CPU의 경우 700m 을 넘으면 안되고 메모리도 800Mi를 넘으면 안된다.

request

- CPU = 500m, 메모리 = 700m 넘지 않아야 한다.

---

노드 관리

- 온프레미스 환경에서 노드를 일시적으로 중단하고 관리해야하는 경우가 있다.
  - 물리적인 디스크의 손상
  - 내부 네트워크의 장애
  - 서버 타입 변경
  - 디스크 교체
- 특정 노드를 유지보수 상태로 전환하여 새로운 Pod가 스케줄링 되지 않게 해야 한다.
  - Cordon
    - 노드를 유지보수 모드로 전환
  - Uncordon
    - 노드를 원래 상태로 정상화
  - Drain
    - 노드를 유지보수 모드로 전환
    - 기존의 있던 Pod도 모두 퇴거(Evict) 시킨다.

Cordon

```shell
kubectl cordon <NODE>
```

유지보수를 위해 새로운 Pod 가 해당 노드로 스케줄링 하지 못하게 막는다.

- node에 cordon 적용시 `taint`가 설정 `unschedulable`이 `true`로 설정
- 그려면 해당 node 이외에 다른 node 또는 master에 Pod이 스케줄링 된다.

Uncordon

- cordon 한 것을 다시 되돌린다.
- Pod가 다시 스케줄링을 시작한다.

```shell
kubectl uncordon worker
```

- `taint` 설정이 사라져 있다.
- `pendding` 상태로 있던 Pod들이 `Running` 상태로 전환 된다.

Drain

- `cordon`은 이미 있던 Pod에 대해 관여하지 않지만 `Drain`은 node에 있는 모든 Pod 이 없도록 만드는 역할을 한다.
- 정상적인 상태로 되돌리려면 `uncordon` 명령을  사용하면 된다.

```shell
kubectl drain worker
# 모든 노드에 존재하는 DeamonSet은 무시
kubectl drain worker --igrore-deamonsets
```

Pod 개수 유지

- `drain` 명령 수행 시 고유의 동작 때문에 순간적으로 트래픽이 한쪽으로 쏠려 응답지연 같은 오류가 발생 할 수 있다.
- `PodDisruptionBudget (PDB)`은 이러한 문제를 해결하고자 만든 리소스
  - pdb는 운영 중인 Pod의 개수를 항상 일정 수준으로 유지하도록 퇴거(Evict)를 막아주는 역할을 한다.
- 관리자가 의도를 가지고 Pod를 중단 하는 것을 VoluntaryDisruptions(자진 중단) 이라고 한다.
  - 자진 중단 상황에서 Pod의 개수가 일정 수준 이하로 내려가지 않게 막아준다.

```shell
# replica를 10으로 올린다.
kubectl scale deploy nginx --replicas 10

# 최소 9개의 Pod가 유지되도록 설정한다.
# nginx-pdb.yaml
apiVersion: policy/v1beta1
kind: PodDisruptionBudget
metadata:
  name: nginx-pdb
spec:
  minAvailable: 9
  selector:
    matchLabels:
      app: nginx      
```

- `minAvailable` 으로 최소 유지되어야 Pod의 개수와 `selector` 으로 유지할 Pod를 선택
  - 1개의 Pod만이 Evicted 된다.
