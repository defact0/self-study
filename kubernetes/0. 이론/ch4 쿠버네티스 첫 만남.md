### :ship: 쿠버네티스 첫 만남

공식문서(kubectl 치트 시트)

- https://kubernetes.io/ko/docs/reference/kubectl/cheatsheet/

---

컨테이너 실행

```shell
# kubectl run <NAME> --image <IMAGE>
kubectl run mynginx --image nginx
```

- [nginx](https://opentutorials.org/module/384/3462)에 대해 알고 싶으면 클릭!

컨테이너 조회

```shell
kubectl get pod

# Pod의 상세정보
kubectl get pod mynginx -o yaml

# Pod의 IP정보
kubectl get pod -o wide
```

컨테이너 상세정보

```shell
# kubectl describe pod <NAME>
kubectl describe pod mynginx
```

- get과 다른 점은 Pod에 대한 Events 기록까지 확인

컨테이너 로깅

```shell
# kubectl logs <NAME>
kubectl logs -f mynginx
```

- -f 옵션은 종료되지 않고 계속 로그가 출력

컨테이너 명령 전달

```shell
# kubectl exec <NAME> -- <CMD>
kubectl exec mynginx -- apt-get update
kubectl exec -it mynginx -- bash
```

- 명령어 전달시 구분자(--)로 전달할 명령을 구분한다.
- -it 옵션을 사용하여 컨테이너 내부로 접속

컨테이너와 호스트간 파일복사

```shell
# kubectl cp <TARGET> <SOURCE>
kubectl cp /etc/passwd mynginx:/tmp/passwd

# 복사 확인
kubectl exec mynginx -- ls /tmp/passwd
kubectl exec mynginx -- cat /tmp/passwd
```

컨테이너 정보 수정

```shell
# kubectl edit pod <NAME>
kubectl edit pod myngix
```

- 수정 내용이 바로 컨테이너에 반영된다.

컨테이너 삭제

```shell
# kubectl delete pod <NAME>
kubectl delete pod mynginx

# Clean up
kubectl delete pod --all
```

선언형 명령 정의서(YAML) 기반의 컨테이너 생성

```shell
# kubectl apply -f <FILE_NAME>
kubectl apply -f mynginx.yaml
```

- <FILE_NAME>부분에 인터넷에 위치한 yaml 경로를 입력해도 적용된다.
- apply 명령은 멱등성 보장, 여러번 실행하더라도 yaml 정의서에 있는 내용과 동일한 결과

Service 리소스

```shell
kubectl get service
kubectl describe service kubernetes
```

Node 리소스

```shell
kubectl get node
kubectl describe node master
```

Namespace 리소스

```shell
kubectl get namespace
kubectl describe namespace kube-system
```

- namespace 종류
  - default
  - kube-system
  - kube-public
  - kube-node-lease

```shell
kubectl run mynginx-ns --image nginx --namespace kube-system

# [Tip] namespace 옵션은 n으로 줄여써도 된다.
# kube-system 네임스페이스에서 Pod 확인
kubectl get pod mynginx-ns -n kube-system

# kube-system 네임스페이스에 있는 mynginx-ns Pod 삭제
kubectl delete pod mynginx -n kube-system
```

- 네임스페이스 옵션을 안쓰면 default 네임스페이스로 동작한다.

자동완성

- kubectl 명령을 매번 입력이 불편하여 명령어를 자동완성시켜주는 스크립트를 제공해 준다.
- https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/#enable-kubectl-autocompletion

즉석 리소스 생성

- YAML 명령 정의서를 cat &  here document 명령 조합으로 즉석으로 리소스 생성

```shell
cat << EOF | kubectl apply -f -
# YAML 내용
EOF
```

리소스 특정 정보 추출

- --jsonpath 옵션 사용, 특정 정보만 골라서 출력

```shell
kubectl get node master -o jsonpath="{.status.addresses[0].address}"

# 모든 노드의 외부IP를 조회
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="ExternalIP")].address}'
```

모든 리소스 조회

```shell
kubectl api-resources
kubectl api-resources --namespaced=true
```

리소스 정의 설명

```shell
kubectl explain pods
```

클러스터 상태 확인

- health check, 트러블 슈팅 시 사용

```shell
# 쿠버네티스 API서버 작동 여부 확인
kubectl cluster-info

# 전체 노드 상태 확인
kubectl get node

# 쿠버네티스 핵심 컴포넌트의 Pod 상태 확인
kubectl get pod -n kube-system
```

클라이언트 설정 파일

- KUBECONFIG ($HOME/.kube/config) 설정 파일 참조

```shell
# kubectl config <SUBCOMMAND>
kubectl config view
```

- 크게 3가지 영역으로 구분된다.
  - clusters
  - users
  - contexts
