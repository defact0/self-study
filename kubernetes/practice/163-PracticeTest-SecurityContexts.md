Practice Test - Security Contexts

- https://uklabs.kodekloud.com/topic/practice-test-security-contexts-2/

---

Q1. What is the user used to execute the sleep process within the `ubuntu-sleeper` pod?

- In the current(default) namespace.

```shell
root@controlplane:~# kubectl get pod
NAME             READY   STATUS    RESTARTS   AGE
ubuntu-sleeper   1/1     Running   0          92s

root@controlplane:~# kubectl exec ubuntu-sleeper -- whoami
root
```

- `root`

----

Q2. Edit the pod `ubuntu-sleeper` to run the sleep process with user ID `1010`.

- Note: Only make the necessary changes. Do not modify the name or image of the pod.
  - 
    Pod Name: ubuntu-sleeper
  - Image Name: ubuntu
  - SecurityContext: User 1010

```shell
# ----------------------------------------
# delete pod
root@controlplane:~# kubectl delete pod ubuntu-sleeper 
pod "ubuntu-sleeper" deleted

# ----------------------------------------
# get pod
root@controlplane:~# kubectl get pod
No resources found in default namespace.

# ----------------------------------------
# apply pod
cat << EOF | kubectl apply -f -
---
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper
  namespace: default
spec:
  securityContext:
    runAsUser: 1010
  containers:
  - command:
    - sleep
    - "4800"
    image: ubuntu
    name: ubuntu-sleeper
EOF


# ----------------------------------------
# get pod
oot@controlplane:~# kubectl get pod
NAME             READY   STATUS    RESTARTS   AGE
ubuntu-sleeper   1/1     Running   0          5s
```

---

Q3. A Pod definition file named `multi-pod.yaml` is given. With what user are the processes in the `web` container started?

- The pod is created with multiple containers and security contexts defined at the `Pod` and `Container` level.

```shell
# ----------------------------------------
# multi-pod.yaml 파일 확인
root@controlplane:~# ls
multi-pod.yaml  sample.yaml

# ----------------------------------------
# multi-pod.yaml 내용 확인
root@controlplane:~# cat multi-pod.yaml 
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  securityContext:
    runAsUser: 1001
  containers:
  -  image: ubuntu
     name: web
     command: ["sleep", "5000"]
     securityContext:
      runAsUser: 1002

  -  image: ubuntu
     name: sidecar
     command: ["sleep", "5000"]

```

- web 이라는  컨테이너는 runAsUser의 값이 1002 인 것을 확인 할 수 있다.

---

Q4. With what user are the processes in the `sidecar` container started?

- The pod is created with multiple containers and security contexts defined at the `Pod` and `Container` level.

```shell
# ----------------------------------------
# multi-pod.yaml 를 생성하지 않았다면 먼저 생성한다.
root@controlplane:~# kubectl apply -f multi-pod.yaml
pod/multi-pod created

# ------------------------------------------
# pod에 있는 컨테이너 whoami 사용하기
#  - 컨테이너가 여러개 존재할 경우 -c <컨테이너이름> 으로 사용한다.
root@controlplane:~# kubectl exec multi-pod -c sidecar -- whoami
whoami: cannot find name for user ID 1001
command terminated with exit code 1

#  - web 컨테이너는 securityContext설정을 따로 하여 1002 이다.
root@controlplane:~# kubectl exec multi-pod -c web -- whoami
whoami: cannot find name for user ID 1002
command terminated with exit code 1
```

- multi-pod POD에 있는 sidecar 컨테이너가 실행하고 있는 유저는 `1001` 이다.
  - Q3에 있는 yaml 파일 내용을 유심히 보면 알 수 있다.
    - web container = 1002 (지역변수? 같은 securityContext이 적용됨)
    - sidecar container = 1001 (전역변수? 같은 securityContext이 적용됨)

---

Q5. Update pod `ubuntu-sleeper` to run as Root user and with the `SYS_TIME` capability.

- Note: Only make the necessary changes. Do not modify the name of the pod.
  - 
    Pod Name: ubuntu-sleeper
  - Image Name: ubuntu
  - SecurityContext: Capability SYS_TIME

```shell
# ----------------------------------------
# delete pod
root@controlplane:~# kubectl delete pod ubuntu-sleeper
pod "ubuntu-sleeper" deleted

# ----------------------------------------
# get pod
root@controlplane:~# kubectl get pod
No resources found in default namespace.

# ----------------------------------------
# apply pod
cat << EOF | kubectl apply -f -
---
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper
  namespace: default
spec:
  containers:
  - command:
    - sleep
    - "4800"
    image: ubuntu
    name: ubuntu-sleeper
    securityContext:
      capabilities:
        add: ["SYS_TIME"]
EOF

# ----------------------------------------
# get pod
root@controlplane:~# kubectl get pod
NAME             READY   STATUS    RESTARTS   AGE
ubuntu-sleeper   1/1     Running   0          5s
```

---

Q6. Now update the pod to also make use of the `NET_ADMIN` capability.

- Note: Only make the necessary changes. Do not modify the name of the pod.
  - Pod Name: ubuntu-sleeper
  - Image Name: ubuntu
  - SecurityContext: Capability SYS_TIME
  - SecurityContext: Capability NET_ADMIN

```shell
# ----------------------------------------
# delete pod
root@controlplane:~# kubectl delete pod ubuntu-sleeper 
pod "ubuntu-sleeper" deleted

# ----------------------------------------
# apply pod
cat << EOF | kubectl apply -f -
---
apiVersion: v1
kind: Pod
metadata:
  name: ubuntu-sleeper
  namespace: default
spec:
  containers:
  - command:
    - sleep
    - "4800"
    image: ubuntu
    name: ubuntu-sleeper
    securityContext:
      capabilities:
        add: ["SYS_TIME", "NET_ADMIN"]
EOF
```

