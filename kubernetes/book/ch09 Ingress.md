### :ship: Ingress

> Layer 7 (application)계층에서 외부의 트래픽을 처리하는 리소스.
> 클러스터로 들어오는 트래픽을 관장할 수 있는 매커니즘 제공한다.

Ingress란?

- 7계층(application)에 대한 설정을 담당하는 리소스이다.
- 기본역할은 외부 HTTP 호출에 대한 트래픽을 처리한다.
  - 부하 분산, TLS 종료, 도메인 기반 라우팅 등등...
  - 클러스터 내부로 접속 할 수 있도록 URL을 부여하여 쉽게 접속할 수 있도록 도와준다.
- Ingress Controller를 통해 Ingress에 정의된 트래픽 라우팅 규칙을 수행한다.

Ingress Controller란?

- 트래픽 처리에 대한 정보를 담고 있는 정의(규칙)에 가깝다.
- 규칙을 읽고 외부의 트래픽을 Service로 전달해 주는 역할을 하는 것이 Ingress Controller 이다.
- <u>특이하게도 해당 Controller는 따로 설치를 해야 사용 가능하다.</u>
- Ingress Controller란 종류
  - NGINX
  - HAProxy
  - AWS ALB
  - 그외 다수...

NGINX Ingress Controller

- 가장 많이 사용되는 제품 중 하나이다.

- 설치방법은 helm을 이용하여 쉽게 가능하다.

  ```shell
  # 네임스페이스 생성
  kubectl create ns ctrl
  
  # nginx-ingress 설치
  helm install nginx-ingress stable/nginx-ingress --version 1.40.3 -n ctrl
  
  # 생성된 리소스 확인
  kubectl get pod -n ctrl
  kubectl get svc -n ctrl
  ```

도메인 주소 테스트

- https://sslip.io 라는 서비스를 이용하면 테스트 할 수 있는 도메인 주소를 얻을 수 있다.
- sslip.io의 서브 도메인에 IP를 입력하면 해당하는 IP를 DNS lookup 결과로 반환한다.

```shell
# IP == IP.sslip.io
nslookup 10.0.1.1.sslip.io

# 2차 서브 도메인 주소 테스트
nslookup sub.10.0.1.1.sslip.io
```

- Layer 7 에서는 서로 다른 도메인 이름으로 라우팅 규칙을 정할 수 있다.

참고 - Ingress Controller IP 확인

```shell
INGRESS_IP=$(kubectl get svc -nctrl nginx-ingress-controller -ojsonpath-"{.status.loadBalancer.ingress[0].ip}")
echo $INGRESS_IP
```

- 외부 네트워크에서 접근 하려는 경우, 호스트 서버(마스터 또는 워크) 중에 하나의 공인 IP로 설정해야 한다.

Ingress 생성

```shell
# Ingress와 연결할 nginx 서비스 생성
kubectl run nginx --image nginx --expose --port 80
kubectl get pod,svc mynginx
```

- Ingress 리소스 정의

  ```yaml
  apiVersion: extensions/v1beta1
  kind: Ingress
  metadata:
    annotations:
      kubernetes.io/ingress.class: nginx
    name: mynginx
  spec:
    rules:
    - host: 10.0.1.1.sslip.io
      http:
      - path: /
        backend:
          serviceName: mynginx
          servicePort: 80
  ```

  - `annotations`은 메타정보를 저장하기 위한 property 이다.
    - Ingress Controller에게 메타정보를 전달할 목적으로 사용
    - 해당 Ingress가 NGINX Ingress Controller에 의해 처리될 것을 명시한 것
  - `rules` 외부 트래픽을 어떻게 처리할지 정의

도메인 기반 라우팅

- 서브 도메인 주소를 이용하여 라우팅 규칙을 설정

```shell
# apache server
kubectl run apache --image httpd --expose --port 80

# nginx server
kubectl run nginx --image nginx --expose --port 80
```

- YAML 파일 작성

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: apache-domain
spec:
  rules:
  # apache 서브도메인
  - host: apache.10.0.1.1.sslip.io
    http:
      paths:
      - backend:
        serviceName: apache
        servicePort: 80
       path: /
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
  name: nginx-domain
spec:
  rules:
  # nginx 서브 도메인
  - host: nginx.10.0.1.1.sslip.io
    http:
      paths:
      - backend:
        serviceName: nginx
        servicePort: 80
       path: /
```

Path 기반 라우팅

- URL path를 기반으로 라우팅할 수 있다.

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
  name: apache-path
spec:
  rules:
  - host: 10.0.1.1.sslip.io
    http:
      paths:
      - backend:
        serviceName: apache
        servicePort: 80
       path: /
---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /
  name: nginx-path
spec:
  rules:
  - host: 10.0.1.1.sslip.io
    http:
      paths:
      - backend:
        serviceName: nginx
        servicePort: 80
       path: /nginx
```

- `nginx.ingress.kubernetes.io/rewrite-target` path 재정의 지시자

  ```shell
  # URL path 테스트
  curl 10.0.1.1.sslip.io/apache
  curl 10.0.1.1.sslip.io/nginx
  ```

Basic Auth 설정

- HTTP Authentication 기능 추가 가능, NGINX 서버에서 제공하는 대부분의 기능들을 동일하게 사용
  - 외부 사용자 접근에 대한 최소한의 보안 절차 설정
- User ID, Password 정보를 HTTP 헤더로 전달하여 인증을 하는데 해당 정보는 base64로 인코딩하여 전달
  - Authentication 헤더 없이 접속 시도 시, 401 Unauthorized를 응답받는다.

```shell
# htpasswd 설치
sudo apt install -y apache2-utils

# id=foo, pw=bar 인 auth 파일 생성
htpasswd -cb auth foo bar

# 생성한 auth 파일 -> Secret으로 변환
kubectl create secret generic basic-auth --from-file=auth

# Secret 리소스 확인
kubectl get secret basic-auth -o yaml
```

basic-auth Secret 리소스를 Ingress에 설정

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/auth-type: basic
    nginx.ingress.kubernetes.io/auth-secret: basic-auth
    nginx.ingress.kubernetes.io/auth-realm: 'Authentication Required - foo'
  name: apache-auth
spec:
  rules:
  - host: apache-auth.10.0.1.1.sslip.io
    http:
      paths:
      - backend:
        serviceName: apache
        servicePort: 80
       path: /
```

- `nginx.ingress.kubernetes.io/auth-type` 인증방식 설정
- `nginx.ingress.kubernetes.io/auth-secret` 사용자 auth 파일이 저장된 secret 이름 저장
- `nginx.ingress.kubernetes.io/auth-realm` 보안 메시지 및 인증 영역 설정

```shell
# 실패
curl -I apache-auth.10.0.1.1.sslip.io
# 성공
curl -I -H "Authorization: Basic $(echo -n foo:bar | base64)" apache-auth.10.0.1.1.sslip.io
```

TLS 설정

- 대부분 웹 브라우저는 TLS가 적용된 HTTPS 서비스를 요구한다.
- Ingress 리소스에 Self-signed 인증서 또는 정식 CA를 통해 서명된 인증서에 대한 정보를 등록해야 한다.

Self-signed 인증서 설정

- 직접 서명한 인증서
- 웹 브라우저에서는 정식이 아니라서 경고가 뜬다.

Self-signed 인증성 생성

```shell
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=apache-tls.10.0.1.1.sslip.io"
```

```yaml
# Secret 리소스 생성
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Secret
metadata:
  name: my-tls-certs
  namespace: default
data:
  tls.crt: $(cat tls.crt | base64 | tr -d '\n')
  tls.crt: $(cat tls.key | base64 | tr -d '\n')
type: kubernetes.io/tls
EOF

# TLS가 적용된 HTTPS Ingress 생성
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: apache-tls
spec:
  tls:
  - hosts:
    - apache-tls.10.0.1.1.sslip.io
    secretName: my-tls-certs
  rules:
  - host: apache-tls.10.0.1.1.sslip.io
  http:
    paths:
    - path: /
      backend:
        serviceName: apache
        servicePort: 80
EOF
```

cert-manager를 이용한 인증서 발급 자동화

```shell
# cert-manager라는 네임스페이스 생성
kubectl create namespace cert-manager

# cert-manager 고나련 사용자 리소스 생성
kubectl apply --validate-false -f https://github.com/jetstack/cert-manager/release/download/v0.15.1/cert-manager.crds.yaml

# jetstack 리파지토리 추가
helm repo add jetstack https://charts.jetstack.io

# 리파지토리 index 업데이트
helm repo update

# cert-manager 설치
helm install \
  cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --version v0.15.1
```

Issuer 생성

```yaml
apiVersion: cert-manager.io/v1alpha2
kind: ClusterIssuer
metadata:
  name: http-issuer
spec:
  acme:
    email: user@test.com
    serverL: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: issuer-key
    solvers:
    - http01:
      ingress:
        class: nginx
```

cert-manager가 관리하는 Ingress 생성

```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: http-issuer
  name: apache-tls-issuer
spec:
  rules:
  - host: apache-tls-issuer.10.0.1.1.sslip.io
    http:
      paths:
      - backend:
        serviceName: apache
        servicePort: 80
      path: /
   tls:
   - host:
     - apache-tls-issuer.10.0.1.1.sslip.io
     secretName: apache-tls
```

```shell
# certificate 확인
kubectl get certificate
```

