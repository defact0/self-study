Account

- 사용자를 위한 유저
- 애플리케이션를 위한 `service account`

Static Token File

- apiServer 서비스 실행 시 `--token-auth-file=filename.csv`전달
  kube-apiserver 수정 필요함
-  API 서버를 다시 시작해야지 적용된다.
- 토큰 / 사용자이름 /사용자 uid / 선택적으로 그룹 이름 다음에 최소 3열의 csv 파일

kubectl에 등록하고 사용

```shell
kubectl config set-credentials user01 --token=password01
kubectl config set-contextg user01-context --cluster=kubernetes \
                               --namespace=frontend --user=user01
kubectl get pod --user user01
```

service account 만들기

- Pod에 별다른 정의가 없으면 `default`로 만들어진다.

  ```shell
  kubectl get sa default -o yaml
  
  # 기본 sa 내용
  apiVersion: v1
  kind: ServiceAccount
  metadata:
    name: default
    namespace: default
    resourceVersion: "279"
    selfLink: /api/v1/namespaces/default/serviceaccounts/default
    uid: 00000-0000-0000
  secrets:
  - name: default-token-ppzqk
  
  # 명령어로 sa 생성
  kubectl create serviceaccount sa01
  
  # Pod에 spec.serviceAccount: service-account-name과 같은 형식으로 지정
  ```

  연습

  ```shell
  # 스태틱 토큰 파일 만들기
  vi static-token.csv
  # password1,user1,uid001,"group1"
  # password2,user2,uid002
  # password3,user3,uid003
  
  vi /etc/kubernetes/manifests/kube-apiserver.yaml
  # spec.containers.command 에 옵션을 추가
  # --token-auth-file=<static-token.csv fullpath>
  
  # 아마 정상적으로 실행이 안될 수 있다.
  kubectl get pod
  docker ps -a | grep api
  docker logs <containerid>
  
  # api 서버가 container 이기 때문에 hostPath를 추가 설정해야 한다.
  # /etc/kubernetes/manifests/ 경로는 이미 hostPath로 등록되어 있기 때문에 오류가 없다.
  
  # user 등록
  kubectl config set-credentials user1 --token=password1
  
  # user1이 어느 클러스터로 접속할지 정하는 것
  kubectl config set-context user1-context --cluster=kubernetes --namespace=frontend --user=user1
  
  # user1-context를 사용한다.
  kubectl config use-context user1-context
  kubectl get pod
  # 현재 단계에서는 forbidden이 출력되어야 한다.(로그인은 했으나 get 권한이 없는 상태)
  
  # 원래 상태로 되돌리기
  kubectl config use-context kubernetes-admin@kubernetes
  ```
  



