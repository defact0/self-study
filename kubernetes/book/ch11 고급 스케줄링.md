### :ship: 고급 스케줄링

> 기본적으로 쿠버네티스가 Pod의 스케줄링을 책임지지만 사용자가 좀 더 상세하게 프로세스를 스케줄링할 수 있는 방법을 제공
> 고가용성 확보를 위한 자동 확장, Pod 상세 스케줄링 방법에 대해 알아보자

고가용성 확보 (Pod 레벨)

- ReplicaSet, Deployment 리로스의 replica property를 사용하여 가용성을 높임
- <u>replica 개수가 정적으로 고정</u>되어 있기 때문에 처리량 범위를 넘어서는 트래픽의 한계를 가진다.
  - Pod 사용랑에 따라 자동 확장하는 `HPA (Horizontal Pod Autoscaler)` 리소스를 제공한다.

> - 수평적 확장
>   - scale-out
>   - 동일한 작업을 하는 프로세스를 늘려 많은 양의 요청 처리
> - 수직적 확장
>   - scale-up
>   - 프로세스의 성능을 높여 더 빠르게 요청 처리

- hpa는 `metrics-server (리소스 사용량 수집 서버)` 컴포넌트 사용 
  - 임계값을 넘으면 replica 개수를 동적으로 조절

metrics server 설치

- helm 을 사용하여 설치

- 기동 시간이 좀 걸리는 편

  - `top`명령을 이용하여 pod, node의 리소스를 확인할 수 있다.

  ```shell
  # pod 리소스 사용량 확인
  kubectl top pod
  
  # node 리소스 사용량 확인
  kubectl top node
  ```

  - 테스트 Pod 이미지는 `k8s.gcr.io/hpa-example`을 사용

  > [주의] hpa가 정상적으로 동작하기 위해서는 반드시 `requests property`가 정의되어야 한다. (HorizontalPodAutoscaler 리소스가 없는 경우)

  ```yaml
  template:
    spec:
      containers:
        resources:
          limits:
            cpu: 500m
          requests:
            cpu: 300m
  ```

hap 생성 - 선언형 명령

```yaml
apiVersion: autoscaling/v1
kind: HorizontalPodAutoscaler
metadata:
  name: heavy-cal
spec:
  minReplicas: 1
  maxReplicas: 50
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: heavy-cal
  targetCPUUtilizationPercentage: 50
```

- `minReplicas` replica 최소
- `maxReplicas` replica 최대
- `scaleTargetRef` 모니터링할 타깃
- `targetCPUUtilizationPercentage` 리소스 임계치
  - Pod가 해당 임계치를 넘기면 maxReplicas 개수까지 증가 시킨다.

hap 생성 - 명령형 명령

```shell
# hpa command
kubectl autoscale deployment heavy-cal --cpu-percent-50 --min=1 --max=50

# show hpa
kubectl get hpa
```

> hpa 를 사용하면 갑자기 증가하는 트래픽에 대해 능동적으로 대응할 수 있는 장점

---

고가용성 확보 (Node 레벨)

> 클러스터 레벨의 Node 또한 자동 수평확장 매커니즘 제공
> : AWS EKS와 GCP GKE 기준

AWS EKS Cluster AutoScaler 설정

- AWS 공식 문서 [참조](https://docs.aws.amazon.com/ko_kr/eks/latest/userguide/cluster-autoscaler.html)

GCP GKE Cluster AutoScaler 설정

- GCP 공식문서 [참조](https://cloud.google.com/kubernetes-engine/docs/concepts/cluster-autoscaler?hl=ko)

Cluster AutoScaler 활용

- Cluster AutoScaler가 판단하는 기준은 hpa와 달리 요청량(requests)이다.
  - `requests` 값에 따라 불필요한 작업이 있으므로 주의해야 한다.
    - Cluster AutoScaler = Pod 자원 요청량
    - Horizontal Pod Autoscaler  = Pod 실제 자원 사용량

  

종합적인 AutoScale 흐름

1. hpa가 CPU 사용량에 의해 Deployment의 replica 개수를 증가
2. 노드에 새로운 Pod 추가
3. 노드 자원 부족으로 일부 Pod가 스케줄링 되지 못하고 Pending 상태 발생
4. Cluster AutoScaler가 Pending된 Pod를 확인
5. 클라우드 플랫폼에 신규 노드를 요청
6. 새로운 노드 할당
7. Pending 되어 있던 Pod들이 신규 노드에 스케줄링

---

Taint

- Node 리소스에 적용하는 설정
- 오염시키다, 오점을 남기다
  - 신규 Pod들이 해당  Node에 스케줄링을 피하게 된다.

```shell
# taint 설정
kubectl taint nodes $NODE_NAME <KEY>=<VALUE>:<EFFECT>
```

- `key` taint의 key 값 (임의의 문자열)
- `value` taint의 value 값 (임의의 문자열)
- `effect` 아래 type 중에 하나를 선택
  - NoSchedule
    - 기존에 있던 Pod는 상관 없고 신규 Pod는 스케줄링 못함
  - PreferNoSchedule
    - 다른 노드에 우선 스케줄링 하고 더이상 리소스가 없는 경우 마지막에 스케줄링 시도 (약한 정책)
  - NoExecute
    - 신규 및 기존 Pod 모두 삭제 (강한 정책)

Toleration

- Pod에 적용하는 설정
- 견디다, 용인하다
  - Taint된 Node라 해도 Pod가 참을 수 있으면 스케줄링 한다.
    - `NoSchedule`가 적용된 Node에도 스케줄링을 한다.

```shell
# taint 설정
kubectl taint nodes worker project=A:NoSchedule

# taint 설정 확인
kubectl get node worker -o yaml | grep -A 4 taints

# no-tolerate.yaml
apiVersion: v1
kind: Pod
metadata:
  name: no-tolerate
spec:
  containers:
  - name: nginx
    image: nginx
    
# apply
kubectl apply -f no-tolerate.yaml
kubectl get pod -o wide
```

- 반복해서 Pod를 생성해도 master node에 할당 되는 것을 확인

```shell
# tolerate.yaml
apiVersion: v1
kind: Pod
metadata:
  name: tolerate
spec:
  containers:
  - name: nginx
    image: nginx
  tolerations:
  - key: "project"
    value: "A"
    operator: "Equal"
    effet: "NoSchedule"
```

- `operator` Equal, Exists 중 하나 선택
  - Equal 인 경우 key-value 가 동일
  - Exists 인 경우 key 값만 동일하면 tolerate 한다.
- 그러나 무조건 worker node에 할당 되는 것을 의미하지 않는다.

taint와 toleration 활용

- 특정 노드에 유지보수 작업
- 네트워크 이상 발생
- 알 수 없는 노드 이슈

---

Affinity & AntiAffinity

- taint & toleration 과 달리 특정 Node나 Pod와의 거리를 조절
  - Affinity = 특정 Pod끼리 가까이 스케줄링
    - NodeAffinity
    - PodAffinity
  - AntiAffinity = 특정 Pod와 멀리 스케줄링
    - PodAntiAffinity

NodeAffinity

- Pod가 특정 Node에 할당되길 원할 때 사용
  - nodeSelector 와 유사하지만 상세한 설정 가능

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: kubernetes.io/e2e-az-name
            operator: In
            values:
            - e2e-az1
            - e2e-az2
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
  containers:
  - name: with-node-affinity
    image: k8s.gcr.io/pause:2.0
```

- `requiredDuringSchedulingIgnoredDuringExecution` 특정 노드에 스케줄링 되길 강제(required)
- `preferredDuringSchedulingIgnoredDuringExecution` 특정 노드에 스케줄링 되길 희망(preferred)
- `operator` In, NotIn, Exists, DoesNotExist, Gt, Lt 과 같이 같이 다양한 매칭 정책을 선택

PodAffinity

- Pod 간의 스케줄링을 관장하기 때문에 Deployment 리소스를 이용하여 설정한다.
  - `topologyKey` Pod끼리 묶을 기준

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-server
spec:
  selector:
    matchLabels:
      app: web-store
  replicas: 3
  template:
    metadata:
      labels:
        app: web-store
    spec:
      affinity:
        podAntiAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - web-store
            topologyKey: "kubernetes.io/hostname"
        podAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
          - labelSelector:
              matchExpressions:
              - key: app
                operator: In
                values:
                - store
            topologyKey: "kubernetes.io/hostname"
      containers:
      - name: web-app
        image: nginx:1.16-alpine
```

PodAntiAffinity

- Pod끼리 서로 다른 노드에 스케줄링하고 싶을 때 사용
- `AntiAffinity`를 `PodAntiAffinity`으로 바꾸면 된다.

PodAffinity 와 PodAntiAffinity 활용

- 적절히 조합하면 높은 안정성을 갖는 서비스 가능

  - web 서버별 최대한 멀리 스케줄링
  - cache 서버별 최대한 멀리 스케줄링
  - web-cache 서버 최대한 가까이 스케줄링

- cach 서버 설정

  ```yaml
  affinity:
    # cache 서버끼리 멀리 스케줄링
    # app=store 라벨을 가진 Pod끼리 멀리 스케줄링
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - store
        topologyKey: "kubernetes.io/hostname"
  ```

- web 서버 설정

  ```yaml
  affinity:
    # web 서버끼리 멀리 스케줄링
    # app=web-store 라벨을 가진 Pod끼리 멀리 스케줄링
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - web-store
        topologyKey: "kubernetes.io/hostname"
    # web-cache 서버끼리 가까이 스케줄링
    # app=store 라벨을 가진 Pod끼리 가까이 스케줄링
      AntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
        matchExpressions:
        - key: app
          operator: In
          values:
          - store
        topologyKey: "kubernetes.io/hostname"
  ```

  
