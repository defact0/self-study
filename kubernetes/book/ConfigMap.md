**ConfigMap, Secret**

> Env(Literal, File), Mount(File)

**Env(Literal)**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cm-dev
data:
  SSH: 'false'
  User: dev
---
apiVersion: v1
kind: Secret
metadata:
  name: sec-dev
data:
  Key: MTIzNA==
---
apiVersion: v1
kind: Pod
metadata:
  name: pod-1
spec:
  containers:
  - name: container
    image: kubetm/init
    envFrom:
    - configMapRef:
        name: cm-dev
    - secretRef:
        name: sec-dev
```

**Env (File)**

```yaml
## shell 에서 txt 파일을 생성하여 configmap과 secret 설정
echo "Content" >> file-c.txt
kubectl create configmap cm-file --from-file=./file-c.txt

echo "Content" >> file-s.txt
kubectl create secret generic sec-file --from-file=./file-s.txt

## yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-file
spec:
  containers:
  - name: container
    image: kubetm/init
    env:
    - name: file-c
      valueFrom:
        configMapKeyRef:
          name: cm-file
          key: file-c.txt
    - name: file-s
      valueFrom:
        secretKeyRef:
          name: sec-file
          key: file-s.txt
```

**Volume Mount (File)**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-mount
spec:
  containers:
  - name: container
    image: kubetm/init
    volumeMounts:
    - name: file-volume
      mountPath: /mount
  volumes:
  - name: file-volume
    configMap:
      name: cm-file
```

**kubectl command**

```shell
## configmap
kubectl create configmap cm-file --from-file=./file-c.txt
kubectl create configmap cm-file --from-literal=key1=value1
kubectl create configmap cm-file --from-literal=key1=value1 --from-literal=key2=value2

## secret
kubectl create secret generic sec-file --from-file=./file-s.txt
kubectl create secret generic sec-file --from-literal=key1=value1
```

**Secret**

- 데이터가 메모리에 저장되기 때문에 보안에 유리
- 한 Secret당 최대 1M까지만 저장됨