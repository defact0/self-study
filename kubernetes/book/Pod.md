### :ship: Pod 살펴보기

> Pod는 쿠버네티스의 최소 실행 단위이다.



가상환경 플랫폼 실행 단위

- 가상머신 : Instance
- 도커 : Container
- 쿠버네티스 : Pod



Pod 특징

- 1개 이상의 컨테이너 실행

- 동일 노드에 할당

- 고유의 Pod IP

- IP 공유

- volume 공유

  > NAT (Network Address Translation)
  > 여러 개의 내부 IP를 1개의 외부 IP와 연결하는 기술로, 대표적으로 `port-forwarding`이 있다.



mynginx.yaml 이라는 YAML 정의서 생성

```shell
kubectl run mynginx --image nginx --dry-run=client -o yaml > mynginx.yaml
```

- `--dry-run`과 `-o yaml` 옵션 사용시 템플릿 파일 생성 가능 (Pod 생성하지 않음)



YAML 파일을 이용하여 Pod 생성

```shell
kubectl apply -f mynginx.yaml
```



라벨 정보 부여

- `label` 명령을 사용

  ```shell
  # kubectl label pod <NAME> <KEY>=<VALUE>
  kubectl label pod mynginx hello=world
  
  # 설정 확인
  kubectl get pod mynginx -o yaml
  ```

- 선언형 명령을 사용

  ```shell
  cat << EOF | kubectl apply -f -
  # 생략
  metadata:
    labels:
      hello: world
      run: mynginx
    name:mynginx
  # 생략
  EOF
  ```

  - `kubectl run <NAME>` 명령 수행시 자동으로 `run=<NAME>`이라는 라벨이 추가된다.



라벨 정보 확인

```shell
kubectl get pod mynginx -L run

# 모든 라벨 정보 표시
kubectl get pod mynginx --show-labels
```



라벨을 이용한 조건 필터링

```shell
# key가 run이고, value가 yournginx Pod 생성
kubectl run yournginx --image nginx

# key가 run인 Pod들 출력
kubectl get pod -l run

# key가 run이고, value가 mynginx Pod 출력
kubectl get pod -l run=mynginx

# key가 run이고, value가 yournginx Pod 출력
kubectl get pod -l run=yournginx
```



nodeSelector를 이용한 노드 선택

- ssd 환경이 필요한 Pod생성할 때, ssd 환경이 구성되어 있는 노드로 Pod 를 생성하기 위한 기능

```shell
kubectl get node --show-labels

# master 노드에 disk type을 ssd로 라벨 부여
kubectl label node master disktype=ssd

# worker 노드에 disk type을 hdd로 라벨 부여
kubectl label node worker disktype=hdd

# 노드의 라벨 확인
kubectl get node --show-labels | grep disktype
```

Pod를 생성하는 YAML 정의서에 `nodeSelector` property 추가

```yaml
# 생략
spec:
  nodeSelector:
    disktype: ssd
```

nodeSelector가 설정된 YAML 파일 적용

```shell
kubectl apply -f node-selector.yaml

# -o wide 옵션, 어느 노드에서 실행하고 있는지 확인
kubectl get pod node-selector -o wide
```

- `node-selector.yaml`안에 `disktype=ssd`으로 설정되어 있어 master 노드에 pod이 생성되었다.
- `node-selector.yaml`안에 `disktype=hdd`으로 변경하고 Pod를 재생성 하면 worker 노드에 pod이 생성되는 것을 확인 할 수 있다.



실행 명령 및 파라미터 지정

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    command: ["/bin/echo"]
    args: ["hello"]
```

- `command` = 컨테이너의 시작 실행 명령 (=도커의 `ENTRYPOINT`에 대응)
- `args` = 실행 명령에 넘겨줄 파라미터 지정 (= 도커의 `CMD`에 대응)

```shell
kubectl apply -f cmd.yaml
kubectl logs -f cmd
# hello
```



환경변수 설정

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    env:
    - name: hello
      value: "world!"
```

- `env`는 환경변수를 설정하는 property 선언
  - `name` 는 환경변수의 key 지정
  - `value` 는 환경변수의 value 지정

```shell
kubectl apply -f env.yaml
kubectl exec env -- printenv | grep hello
# hello=world!
```



볼륨 연결

- Pod가 삭제되면 저장된 데이터가 같이 사라지기 때문에 Pod의 생명주기와 상관없이 데이터를 유지하고 싶다면 볼륨을 따로 연결해야 한다.

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    # 컨테이너 내부의 연결 위치 지정
    volumeMounts:
    - mountPath: /container-volume
      name: my-volume
  # host 서버의 연결 위치 지정
  volumes:
  - name: my-volume
    hostPath:
      path: /home
```

- emptyDir volume
  - volumes 부분에 `emptyDir: {}` 을 추가하면 Pod 내에서 임시로 생성하는 스토리지가 설정된다.
  - Pod가 삭제되면 emptyDir volume도 같이 삭제된다.

```shell
kubectl apply -f volume.yaml
kubectl exec volume -- ls /container-volume
# ubuntu

ls /home
# ubuntu
```



requests

- Pod가 보장받을 수 있는 최소 리소스 사용량 정의

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      requests:
        cpu: "250m"
        memory: "500Mi"
```

- cpu 1 core = 1000m
- memory Mi = 1MiB(2^20 bytes)



limits

- Pod가 최대로 사용할 수 있는 최대 리소스 사용량 정의

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    resources:
      limits:
        cpu: "500m"
        memory: "1Gi"
```

- 최대 메모리 리소스 사용량을 넘으면 강제로 프로세스가 중단된다.
- requests와 limits 옵션을 같이 사용하면 안정적으로 운영 할 수 있다.



livenessProbe

- Pod가 정상적으로 동작하고 있는지 확인하는 property
- 자가치유를 위한 판단 기준

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    livenessProbe:
      httpGet:
        path: /live
        port: 80
```

- `httpGet`은 HTTP GET method를 이용하여 상태 확인을 수행

```shell
kubectl apply -f liveness.yaml

# <ctrl> + <c>로 watch를 종료
watch kubectl get pod liveness

# nginx에는 /live 라는 API가 없다
kubectl logs -f liveness

# 컨테이너 정상 상태 확인
kubectl exec liveness -- touch /usr/share/nginx/html/live
kubectl logs liveness
kubectl get pod liveness
# /live 호출에 200으로 응답, 더 이상 RESTART 개수가 증가하지 않음
```



readinessProbe

- Pod의 준비 완료를 확인하는 property
- Jenkins 같은 구동이 오래 걸리는 웹 서비스 확인 용도

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
    readinessProbe:
      httpGet:
        path: /ready
        port: 80
```

- readinessProbe의 상태를 `Ready 0/1` 표시를 통해 확인



2개 컨테이너 실행

- Pod 내에 2개의 서로 다른 컨테이너 실행

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
  - name: curl
    image: curlimages/curl
    command: ["/bin/sh"]
    args: ["-c", "while true; do sleep 5; curl localhost; done"]
```

- 컨테이너의 실행 순서를 보장하지 않는다.

컨테이너가 1개 이상이기 때문에 로그 확인 시 `-c` 옵션을 사용하여 특정 컨테이너를 지정해야 한다.

```shell
kubectl logs second -c nginx
kubectl logs second -c curl
```



사이드카 패턴(Sidecar Pattern)

- 1개의 Pod 내에 2개 이상의 컨테이너를 실행하는 이유는?
  - 메인 컨테이너
    - 웹 서버
  - 보조 컨테이너
    - 웹 서버의 로그를 중앙 로그 시스템으로 전송
    - 메인 컨테이너를 보조하는 역할
    - 오토바이의 사이드카를 닮았다고 하여 붙여진 이름



초기화 컨테이너

- `initContainers` 메인 컨테이너 실행에 앞서 초기화를 위해 먼저 실행되는 컨테이너를 정의 할 수 있다.

```yaml
spec:
  containers:
  - name: nginx
    image: nginx
  initContainers:
  - name: git
    image: alpine/git
```



Config 설정

- 설정 값들을 따로 모아두고 필요할 때 꺼내 사용할 수 있는 메커니즘이 존재
- ConfigMap에 모든 설정 값들을 저장하고 Pod에서 필요한 정보를 불러올 수 있다.

```shell
# [Case 1]
# kubectl create configmap <key> <data-source>
kubectl create configmap game-config --from-file=game.properties

# game.properties
weapon=gun
health=3
potion=4

# ConfigMap 상세 조회 (ConfigMap을 cm으로 축약)
kubectl get cm game-config -o yaml

# [Case 2]
# 추가 등록
kubectl create configmap special-config \
             --from-literal=special.power=10 \
             --form-literal=special.strength=20
             
# 추가 등록 확인
kubectl get cm special-config -o yaml

# [Case 3]
# yaml 파일 생성
apiVersion: v1
kind: ConfigMap
metadata:
  name: monster-config
  namespace: default
data:
  monsterType: fire
  monsterNum: "5"
  monsterLife: "3"
```



ConfigMap 활용

- 볼륨 연결

  ```yaml
  # Pod 생성시 volumes 부분
  volumes:
  - name: game-volume
    configMap:
      name: game-config
  ```

- 환경변수 - valueFrom
  - ConfigMap을 Pod의 환경변수로도 사용 할 수 있다.
  
  ```yaml
  spec:
    containers:
      env:
      - name: special-env
        valueFrom:
        - configMapKeyRef:
            name: special-config
            key: special.power
  ```
  
  - special-config라는 ConfigMap 중 special.power라는 설정값을 환경 변수 special-env로 활용하라는 것을 의미
  
- 환경변수 - envFrom

  - ConfigMap 에 포함된 모든 설정값을 환경변수로 사용 (1개만 사용하는 valueFrom과는 반대)

  ```yaml
  spec:
    containers:
      env:
      - name: special-env
        envFrom:
        - configMapKeyRef:
           name: special-config
  ```

  - special-config라는 ConfigMap 중 special.power라는 설정값을 환경 변수 special-env로 활용하라는 것을 의미



민감 데이터 관리

- Secret 리소스 생성

  - 관련 정보를 base64로 인코딩

  ```shell
  echo -ne admin | base64
  # YWRtaW4=
  
  echo -ne password123 | base64
  # cGFzc3dvcmQxMjM=
  ```

  - 해당 값을 이용하여 Secret 리소스 만들기

  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: user-info
  type: Opaque
  data:
    username: YWRtaW4=
    password: cGFzc3dvcmQxMjM=
  ```

  - yaml파일로 저장 후 리소스 생성

  ```shell
  kubectl apply -f user-info.yaml
  kubectl get secret user-info -o yaml
  ```

- base64를 쿠버네티스가 대신 처리하게 하려면 stringData 설정을 사용해라

  ```yaml
  apiVersion: v1
  kind: Secret
  metadata:
    name: user-info
  type: Opaque
  stringData :
    username: admin
    password: password123
  ```

- 명령형 커맨드로 Secret 리소스 생성하기

  - user-info.properties 준비

    ```properties
    username=admin
    password=password123
    ```

  - `--from-env-file`옵션을 이용하여 생성

    ```shell
    kubectl create secret generic user-info-from-file \
                       --from-env-file=user-info.properties
    
    kubectl get secret user-info-from-file -o yaml
    ```

    - `--from-file`, `--from-literal` 옵션을 지원



Secret 활용

- 볼륨 연결
  - `volumes property`에 `secret`이라는 이름으로 볼륨 연결
  
    ```yaml
    volumes:
    - name: secret
      secret:
        secretName: user-info
    ```
  
- 환경변수 - env

  - 개별적인 환경변수 지정, `valueFrom.secretKeyRef` property를 사용

    ```yaml
    valueFrom:
      secretKeyRef:
        name: user-info
        key: password
    ```

- 환경변수 - envFrom

  - 전체 환경변수를 불러오고자 할 때, `envFrom.secretRef` property를 사용

    ```yaml
    envFrom:
    - secretKeyRef:
        name: user-info
    ```

    

메타데이터 전달

> Pod의 메타데이터를 컨테이너에게 전달하는 방법제공 = Downward API
> 실행되는 Pod의 정보를 컨테이너에 노출하고 싶을 때 사용

- 볼륨 연결

  ```yaml
  metadata:
    name: downward-volume
  spec:
    containers:
      volumes:
        downwardAPI:
          items:
          - path: "labels"
            fieldRef:
              fieldPath: metadata.labels
  ```

- 환경변수 - env

  ```yaml
  spec:
    containers:
      env:
      - name: NODE_NAME
        valueFrom:
          fieldRef:
            fieldPath: spec.nodeName
      - name: POD_NAME
        valueFrom:
          fieldRef:
            fieldPath: metadata.name
  ```

  - `fieldPath`는 Pod의 메타데이터 필드를 지정

---

**Pod**

> Container, Label, NodeSchedule

Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
spec:
  containers:
  - name: container1
    image: kubetm/p8000
    ports:
    - containerPort: 8000
  - name: container2
    image: kubetm/p8080
    ports:
    - containerPort: 8080
```

ReplicationController

```shell
apiVersion: v1
kind: ReplicationController
metadata:
  name: replication-1
spec:
  replicas: 1
  selector:
    app: rc
  template:
    metadata:
      name: pod-1
      labels:
        app: rc
    spec:
      containers:
      - name: container
        image: kubetm/init
```

[Label] Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-2
  labels:
    type: web
    lo: dev
spec:
  containers:
  - name: container
    image: kubetm/init
```

[Label] Serivce

```yaml
apiVersion: v1
kind: Service
metadata:
  name: svc-1
spec:
  selector:
    type: web
  ports:
  - port: 8080
```

[Node Schedule] Pod - nodeSelector

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-3
spec:
  nodeSelector:
    kubernetes.io/hostname: k8s-node1
  containers:
  - name: container
    image: kubetm/init
```

- 원하는 노드에 스케쥴링을 하기위해서 `nodeSelector`를 설정한다. 

[Node Schedule] Pod - requests & limits

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-4
spec:
  containers:
  - name: container
    image: kubetm/init
    resources:
      requests:
        memory: 2Gi
      limits:
        memory: 3Gi
```

- 최소, 최대 container 리소스를 설정한다.

---

kubectl apply vs create 차이

- apply, create 둘다 리소스를 생성 가능
- create는 이미 이름이 존재하는 Pod를 생성할 수 없다.
- apply는 이미 이름이 존재하는 Pod를 update 처리 한다.

