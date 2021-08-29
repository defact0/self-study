Practice Test - Application Failure

- https://uklabs.kodekloud.com/topic/practice-test-application-failure-2/

---

Q1. **Troubleshooting Test 1:** A simple 2 tier application is deployed in the `alpha` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

App 버튼을 클릭하면 웹 페이지가 나오는데 아래와 같은 오류 메세지가 출력된다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=root; DB_Password=paswrd; 2003: Can't connect to MySQL server on 'mysql-service:3306' (-2 Name does not resolve)
From webapp-mysql-75dfdf859f-gxs6w!
```

- Can't connect to MySQL server 인 것을 오류로그를 통해 확인 할 수 있다.

```shell
controlplane $ kubectl -n alpha get all
NAME                                READY   STATUS    RESTARTS   AGE
pod/mysql                           1/1     Running   0          4m
pod/webapp-mysql-75dfdf859f-gxs6w   1/1     Running   0          4m

NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/mysql         ClusterIP   10.100.9.67     <none>        3306/TCP         4m
service/web-service   NodePort    10.96.226.166   <none>        8080:30081/TCP   3m59s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webapp-mysql   1/1     1            1           4m

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/webapp-mysql-75dfdf859f   1         1         1       4m
```

- alpha 네임스페이스의 리소스를 전부 출력 하면 service 리소스에 `mysql`을 확인할 수 있다.
  - 오류 로그에서는 DB_Host=`mysql-service` 이름과 다름을 알 수 있다.

```shell
# service 리소스를 수정한다.
kubectl -n alpha get svc mysql -o yaml > mysql.yaml

# mysql.yaml 내용 중에 metadata.name에 있는 값을 수정한다.
# mysql -> mysql-service

# 기존에 동작중인 리소스를 지우고 수정된 리소스를 생성한다.
kubectl -n alpha delete svc mysql
kubectl apply -f mysql.yaml

# 상태를 확인한다.
controlplane $ kubectl -n alpha get svc
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
mysql-service   ClusterIP   10.100.9.67     <none>        3306/TCP         7s
web-service     NodePort    10.96.226.166   <none>        8080:30081/TCP   10m
```

- service 리소스 이름이 mysql에서 mysql-service로 변경된 것을 확인 할 수 있다.

App 버튼을 클릭하면 웹 페이지가 나오는데 정상적인 페이지가 출력됨을 확인 할 수 있다.

---

Q2. **Troubleshooting Test 2:** The same 2 tier application is deployed in the `beta` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

App 버튼을 클릭하면 웹 페이지가 나오는데 아래와 같은 오류 메세지가 출력된다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=root; DB_Password=paswrd; 2003: Can't connect to MySQL server on 'mysql-service:3306' (111 Connection refused)
From webapp-mysql-75dfdf859f-tngdr!
```

리소스를 확인해 본다.

```shell
controlplane $ kubectl -n beta get all
NAME                                READY   STATUS    RESTARTS   AGE
pod/mysql                           1/1     Running   0          3m14s
pod/webapp-mysql-75dfdf859f-tngdr   1/1     Running   0          3m13s

NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/mysql-service   ClusterIP   10.102.140.140   <none>        3306/TCP         3m14s
service/web-service     NodePort    10.100.73.178    <none>        8080:30081/TCP   3m13s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webapp-mysql   1/1     1            1           3m13s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/webapp-mysql-75dfdf859f   1         1         1       3m13s
```

- service 리소스의 mysql-service 상세정보를 확인해 본다.

```shell
controlplane $ kubectl -n beta describe svc mysql-service 
Name:              mysql-service
Namespace:         beta
Labels:            <none>
Annotations:       <none>
Selector:          name=mysql
Type:              ClusterIP
IP:                10.102.140.140
Port:              <unset>  3306/TCP
TargetPort:        8080/TCP
Endpoints:         10.244.1.6:8080
Session Affinity:  None
Events:            <none>
```

- TargetPort는 Pod로 전달되는 요청이 도달하는 포트를 가리킨다 8080이 아닌 3306으로 설정되어야 한다.
  - service 리소스는 endpoints를 통해 트래픽을 보내는 주소의 목록을 관리한다.

```shell
# 현재 svc 리소스를 yaml 파일로 저장한다
kubectl -n beta get svc mysql-service -o yaml > mysql.yaml

# 기존에 서비스 중이었던 svc를 삭제
kubectl -n beta delete svc mysql-service

# mysql.yaml 수정
vi mysql.yaml
# spec.ports.targetPort 부분을 8080 -> 3006 으로 수정한다.
kubectl apply -f mysql.yaml

# 생성된 서비스 리소스 확인
controlplane $ kubectl -n beta describe svc mysql-service
Name:              mysql-service
Namespace:         beta
Labels:            <none>
Annotations:       <none>
Selector:          name=mysql
Type:              ClusterIP
IP:                10.102.140.140
Port:              <unset>  3306/TCP
TargetPort:        3306/TCP
Endpoints:         10.244.1.6:3306
Session Affinity:  None
Events:            <none>
```

App 버튼을 클릭하면 웹 페이지가 나오는데 정상적인 페이지가 출력됨을 확인 할 수 있다.

----

Q3. **Troubleshooting Test 3:** The same 2 tier application is deployed in the `gamma` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

App 버튼을 클릭하면 웹 페이지가 나오는데 아래와 같은 오류 메세지가 출력된다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=root; DB_Password=paswrd; 2003: Can't connect to MySQL server on 'mysql-service:3306' (111 Connection refused)
From webapp-mysql-75dfdf859f-rmc2m!
```

아래와 같이 리소스 확인 부터 한다.

```shell
# gamma 네임스페이스의 전체 리소스 확인
controlplane $ kubectl -n gamma get all
NAME                                READY   STATUS    RESTARTS   AGE
pod/mysql                           1/1     Running   0          2m49s
pod/webapp-mysql-75dfdf859f-rmc2m   1/1     Running   0          2m49s

NAME                    TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
service/mysql-service   ClusterIP   10.96.81.88      <none>        3306/TCP         2m49s
service/web-service     NodePort    10.101.154.122   <none>        8080:30081/TCP   2m48s

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/webapp-mysql   1/1     1            1           2m49s

NAME                                      DESIRED   CURRENT   READY   AGE
replicaset.apps/webapp-mysql-75dfdf859f   1         1         1       2m49s

# gamma 네임스페이스에 endpoints를 검사하는데 mysql-service 주소가 none 이다.
controlplane $ kubectl -n gamma get ep
NAME            ENDPOINTS         AGE
mysql-service   <none>            3m11s
web-service     10.244.1.9:8080   3m10s
```

- gamma 네임스페이스에 endpoints를 검사하는데 mysql-service 주소가 none 이다.

```shell
# -----------------------
# svc mysql-service
controlplane $ kubectl -n gamma get svc mysql-service -o yaml
apiVersion: v1
kind: Service
...
spec:
  clusterIP: 10.96.81.88
...
  selector:
    name: sql00001    <------------- 여기 부분 확인(비교1)
    
# -----------------------
# pod mysql
controlplane $ kubectl -n gamma get pod mysql -o yaml
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: mysql    <------------- 여기 부분 확인(비교2)
```

- mysql-service와 mysql pod 내용을 살펴보면 labels selector가 매칭이 안되는 것을 확인 할 수 있다.
- 그렇기 때문에 mysql-service 리소스를 수정해야 한다.

```shell
# 기존에 서비스를 삭제한다.
kubectl -n gamma delete svc mysql-service

# expose 옵션과 라벨을 추가한다.
kubectl -n gamma expose pod mysql --name=mysql-service

# mysql-service의 endpoints 정보가 추가되었음을 확인 할 수 있다.
controlplane $ kubectl -n gamma get ep
NAME            ENDPOINTS         AGE
mysql-service   10.244.1.8:3306   0s
web-service     10.244.1.9:8080   12m

# mysql-service 서비스에 selector.name이 변경된 것을 확인 할 수 있다.
controlplane $ kubectl -n gamma get svc mysql-service -o yaml | grep -A3 selector
  selector:
    name: mysql
  sessionAffinity: None
  type: ClusterIP
```

---

Q4. **Troubleshooting Test 4:** The same 2 tier application is deployed in the `delta` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

App 버튼을 클릭하면 웹 페이지가 나오는데 아래와 같은 오류 메세지가 출력된다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=sql-user; DB_Password=paswrd; 1045 (28000): Access denied for user 'sql-user'@'10.244.1.11' (using password: YES)
From webapp-mysql-67cfc57cbc-q8gd8!
```

- 설계에는 DB USER가 root인데 현재 sql-user로 되어 있다.

```shell
# deployment 리소스 확인
controlplane $ kubectl -n delta get deployments.apps 
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
webapp-mysql   1/1     1            1           4m9s

# deployment 부분에서 Pod Template를 확인해야 한다.
kubectl -n delta describe deployment webapp-mysql

# describe deployment webapp-mysql
Name:                   webapp-mysql
Namespace:              delta
....
Pod Template:
  Labels:  name=webapp-mysql
  Containers:
   webapp-mysql:
    Image:      mmumshad/simple-webapp-mysql
    Port:       8080/TCP
    Host Port:  0/TCP
    Environment:
      DB_Host:      mysql-service
      DB_User:      sql-user          <----------- 여기 부분을 확인
      DB_Password:  paswrd

# yaml 파일로 저장
kubectl -n delta get deployment webapp-mysql -o yaml > web.yaml
kubectl -n delta delete deployment webapp-mysql
vi web.yaml
# Pod Template.Containers.webapp-mysql.Environment.DB_User 부분을 수정한다.
kubectl apply -f web.yaml
```

---

Q5.**Troubleshooting Test 5:** The same 2 tier application is deployed in the `epsilon` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

App 버튼을 클릭하면 웹 페이지가 나오는데 아래와 같은 오류 메세지가 출력된다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=sql-user; DB_Password=paswrd; 1045 (28000): Access denied for user 'sql-user'@'10.244.1.14' (using password: YES)
```

Q4에서 했던 것과 동일하게 deployment 리소스의 Pod Template.Containers.webapp-mysql.Environment.DB_User 부분을 수정한다.

```shell
kubectl -n epsilon get deployments.apps
kubectl -n epsilon get deployments.apps webapp-mysql -o yaml > deploy.yaml
vi deploy.yaml 
kubectl -n epsilon delete deployments.apps webapp-mysql 
kubectl apply -f deploy.yaml
```

여전히 오류 상태이다. 다른 오류의 원인을 찾아야 한다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=root; DB_Password=paswrd; 1045 (28000): Access denied for user 'root'@'10.244.1.16' (using password: YES)
```

mysql Pod 리소스의 내용을 확인하면 mysql 패스워드 부분이 잘못 입력된 것을 확인할 수 있으며 이것을 수정한다.

```shell
controlplane $ kubectl -n epsilon get pod mysql -o yaml
  spec:
    containers:
    - env:
      - name: MYSQL_ROOT_PASSWORD
        value: passwooooorrddd     <---------- 여기부분 확인
      image: mysql:5.6

# yaml 파일 생성
kubectl -n epsilon get pod mysql -o yaml > pod.yaml

# 기존에 생성된 Pod 삭제
kubectl -n epsilon delete pod mysql

# 수정된 Pod 생성
kubectl apply -f pod.yaml
```

----

Q6. **Troubleshooting Test 6:** The same 2 tier application is deployed in the `zeta` namespace. It must display a green web page on success. Click on the app tab at the top of your terminal to view your application. It is currently failed. Troubleshoot and fix the issue.

Stick to the given architecture. Use the same names and port numbers as given in the below architecture diagram. Feel free to edit, delete or recreate objects as necessary.

App 버튼을 클릭하면 웹 페이지가 나오는데 아래와 같은 오류 메세지가 출력된다.

```shell
Connecting to Port 30081
We're currently trying to connect to a HTTP service running on 30081. Services can sometimes take a few moments to start, even up to five minutes.
```

서비스 리소스 부터 점검한다.

```shell
controlplane $ kubectl -n zeta get svc
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
mysql-service   ClusterIP   10.105.80.82    <none>        3306/TCP         80s
web-service     NodePort    10.97.131.238   <none>        8080:30088/TCP   80s

# 수정 내용
controlplane $ kubectl -n zeta get svc web-service -o yaml > web.yaml
controlplane $ vi web.yaml 
controlplane $ kubectl -n zeta delete svc web-service 
service "web-service" deleted
controlplane $ kubectl apply -f web.yaml 
service/web-service created
controlplane $ kubectl -n zeta get svc
NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
mysql-service   ClusterIP   10.105.80.82    <none>        3306/TCP         5m12s
web-service     NodePort    10.97.131.238   <none>        8080:30081/TCP   5s
```

- web-service의 NodePort가 8080:30088 인데 8080:30081 으로 수정되어야 한다.
  - 구성도를 보면 8080:30081 으로 수정되어야 한다.

수정했음에도 여전히 웹 페이지는 오류가 발생한다.

```shell
Environment Variables: DB_Host=mysql-service; DB_Database=Not Set; DB_User=sql-user; DB_Password=paswrd; 1045 (28000): Access denied for user 'sql-user'@'10.244.1.15' (using password: YES)
```

delployment 리소스와 pod 리소스의 mysql 값 설정 오류로 인해 발생한 문제로 해당 부분을 수정하도록 한다.

```shell
# mysql pod 수정
controlplane $ kubectl -n zeta get pod
NAME                            READY   STATUS    RESTARTS   AGE
mysql                           1/1     Running   0          7m4s
webapp-mysql-67cfc57cbc-sk4h5   1/1     Running   0          7m4s
controlplane $ kubectl -n zeta get pod mysql -o yaml > mysql.yaml
controlplane $ vi mysql.yaml
controlplane $ kubectl -n zeta delete pod mysql                     
pod "mysql" deleted
controlplane $ kubectl apply -f mysql.yaml 
pod/mysql created

# deployment 수정
controlplane $ kubectl -n zeta get deployments.apps 
NAME           READY   UP-TO-DATE   AVAILABLE   AGE
webapp-mysql   1/1     1            1           8m46s
controlplane $ kubectl -n zeta get deployments.apps webapp-mysql -o yaml > deploy.yaml
controlplane $ vi deploy.yaml 
controlplane $ kubectl -n zeta delete deployments.apps webapp-mysql                      
deployment.apps "webapp-mysql" deleted         
controlplane $ kubectl apply -f deploy.yaml 
deployment.apps/webapp-mysql created
```

