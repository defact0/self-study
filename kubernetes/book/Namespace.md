**Namespace**

> Namespace, ResourceQuota, LimitRange

**Namespace**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nm-1
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
  namespace: nm-1
  labels:
    app: pod
spec:
  containers:
  - name: container
    image: kubetm/app
    ports:
    - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: svc-1
  namespace: nm-1
spec:
  selector:
    app: pod
  ports:
  - port: 9000
    targetPort: 8080
```

다른예제

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nm-2
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
  namespace: nm-2
  labels:
    app: pod
spec:
  containers:
  - name: container
    image: kubetm/init
    ports:
    - containerPort: 8080
```

리소스 접근

```shell
## pod ip
curl 10.16.36.115:8080/hostname

## service ip
curl 10.96.92.97:9000/hostname
```



**ResourceQuota**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nm-3
---
apiVersion: v1
kind: ResourceQuota
metadata:
  name: rq-1
  namespace: nm-3
spec:
  hard:
    requests.memory: 1Gi
    limits.memory: 1Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-2
spec:
  containers:
  - name: container
    image: kubetm/app
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-3
spec:
  containers:
  - name: container
    image: kubetm/app
    resources:
      requests:
        memory: 0.5Gi
      limits:
        memory: 0.5Gi
```

리소스 확인

```shell
kubectl describe resourcequotas --namespace=nm-3
```

**LimitRange**

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: nm-5
---
apiVersion: v1
kind: LimitRange
metadata:
  name: lr-1
spec:
  limits:
  - type: Container
    min:
      memory: 0.1Gi
    max:
      memory: 0.4Gi
    maxLimitRequestRatio:
      memory: 3
    defaultRequest:
      memory: 0.1Gi
    default:
      memory: 0.2Gi
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
spec:
  containers:
  - name: container
    image: kubetm/app
    resources:
      requests:
        memory: 0.1Gi
      limits:
        memory: 0.5Gi
```

- ResourceQuota는 Namespace 뿐만 아니라 Cluster 전체에 부여할 수 있는 권한이지만, LimitRange의 경우 Namespace내에서만 사용 가능

**kubectl command**

```shell
kubectl describe resourcequotas --namespace=nm-3
kubectl describe limitranges --namespace=nm-5
```



