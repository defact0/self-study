Practice Test - Commands and Arguments

- https://uklabs.kodekloud.com/topic/practice-test-commands-and-arguments-2/

---

Q1. How many PODs exist on the system?

- in the current(default) namespace

```shell
root@controlplane:~# kubectl get pods
NAME             READY   STATUS              RESTARTS   AGE
ubuntu-sleeper   0/1     ContainerCreating   0          7s
```

- 1

---

Q2. What is the command used to run the pod `ubuntu-sleeper`?

```shell
root@controlplane:~# kubectl describe pod ubuntu-sleeper 
Name:         ubuntu-sleeper
Namespace:    default
...
    Command:
      sleep
      4800
```

- `sleep 4800`

---

Q3. Create a pod with the ubuntu image to run a container to sleep for 5000 seconds. Modify the file `ubuntu-sleeper-2.yaml`.

- Note: Only make the necessary changes. Do not modify the name.
  - Pod Name: ubuntu-sleeper-2
  - Command: sleep 5000

```shell

root@controlplane:~# ls
sample.yaml  ubuntu-sleeper-2.yaml  ubuntu-sleeper-3.yaml  webapp-color  webapp-color-2  webapp-color-3
root@controlplane:~# vi ubuntu-sleeper-2.yaml 

# --------------------------------------
# ubuntu-sleeper-2.yaml 내용 수정
# --------------------------------------
---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "5000"

# --------------------------------------
# ubuntu-sleeper-2.yaml 적용
# --------------------------------------
root@controlplane:~# kubectl apply -f ubuntu-sleeper-2.yaml 
pod/ubuntu-sleeper-2 created
root@controlplane:~# kubectl get pod
NAME               READY   STATUS    RESTARTS   AGE
ubuntu-sleeper     1/1     Running   0          7m25s
ubuntu-sleeper-2   1/1     Running   0          4s
```

---

Q4. Create a pod using the file named `ubuntu-sleeper-3.yaml`. There is something wrong with it. Try to fix it!

- Note: Only make the necessary changes. Do not modify the name.
  - Pod Name: ubuntu-sleeper-3
  - Command: sleep 1200

```shell

root@controlplane:~# ls
sample.yaml  ubuntu-sleeper-2.yaml  ubuntu-sleeper-3.yaml  webapp-color  webapp-color-2  webapp-color-3
root@controlplane:~# vi ubuntu-sleeper-3.yaml 

# --------------------------------------
# ubuntu-sleeper-3.yaml 내용 수정
# --------------------------------------
---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-3 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "1200"

# --------------------------------------
# ubuntu-sleeper-3.yaml 적용
# --------------------------------------
root@controlplane:~# kubectl apply -f ubuntu-sleeper-3.yaml 
pod/ubuntu-sleeper-3 created
root@controlplane:~# kubectl get pod
NAME               READY   STATUS    RESTARTS   AGE
ubuntu-sleeper     1/1     Running   0          7m25s
ubuntu-sleeper-2   1/1     Running   0          4s
ubuntu-sleeper-3   1/1     Running   0          8s
```

---

Q5. Update pod `ubuntu-sleeper-3` to sleep for 2000 seconds.

- Note: Only make the necessary changes. Do not modify the name of the pod. Delete and recreate the pod if necessary.
  - Pod Name: ubuntu-sleeper-3
  - Command: sleep 2000

```shell
root@controlplane:~# ls
sample.yaml  ubuntu-sleeper-2.yaml  ubuntu-sleeper-3.yaml  webapp-color  webapp-color-2  webapp-color-3


root@controlplane:~# vi ubuntu-sleeper-3.yaml 
# --------------------------------------
# ubuntu-sleeper-3.yaml 내용 수정
# --------------------------------------
---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-3 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "2000"

root@controlplane:~# kubectl delete pod ubuntu-sleeper-3
pod "ubuntu-sleeper-3" deleted

root@controlplane:~# kubectl apply -f ubuntu-sleeper-3.yaml 
pod/ubuntu-sleeper-3 created

root@controlplane:~# kubectl get pod -w
NAME               READY   STATUS              RESTARTS   AGE
ubuntu-sleeper     1/1     Running             0          16m
ubuntu-sleeper-2   1/1     Running             0          8m39s
ubuntu-sleeper-3   1/1     Running             0          28s
```

---

Q6. Inspect the file `Dockerfile` given at /root/webapp-color. What command is run at container startup?

```shell
root@controlplane:~# ls
sample.yaml  ubuntu-sleeper-2.yaml  ubuntu-sleeper-3.yaml  webapp-color  webapp-color-2  webapp-color-3
root@controlplane:~# cd webapp-color
root@controlplane:~/webapp-color# ls
Dockerfile  Dockerfile2
root@controlplane:~/webapp-color# cat Dockerfile
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
```

- Dockerfile 내용을 보면 `ENTRYPOINT ["python", "app.py"]`인 것을 확인 할 수 있다.
  - 정답은 `python app.py` 이다.

---

Q7. Inspect the file `Dockerfile2` given at /root/webapp-color. What command is run at container startup?

```shell
root@controlplane:~# ls
sample.yaml  ubuntu-sleeper-2.yaml  ubuntu-sleeper-3.yaml  webapp-color  webapp-color-2  webapp-color-3
root@controlplane:~# cd webapp-color
root@controlplane:~/webapp-color# ls
Dockerfile  Dockerfile2
root@controlplane:~/webapp-color# cat Dockerfile2
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]
```

- `ENTRYPOINT ["python", "app.py"]` 와 `CMD ["--color", "red"]`을 보면
  - `python app.py --color red` 명령이 실행하는 것을 알 수 있다.

---

Q8. Inspect the two files under directory `webapp-color-2`. What command is run at container startup?

- Assume the image was created from the Dockerfile in this folder

```shell
root@controlplane:~# cd webapp-color-2/
root@controlplane:~/webapp-color-2# ls
Dockerfile2  webapp-color-pod.yaml
root@controlplane:~/webapp-color-2# cat webapp-color-pod.yaml 
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    command: ["--color","green"]
root@controlplane:~/webapp-color-2# 
```

- webapp-color-pod.yaml 파일의 command 항목을 보면 `--color green` 인 것을 확인 할 수 있다.

---

Q9. Inspect the two files under directory `webapp-color-3`. What command is run at container startup?

- Assume the image was created from the Dockerfile in this folder

```shell
root@controlplane:~# cd webapp-color-3
root@controlplane:~/webapp-color-3# ls
Dockerfile2  webapp-color-pod-2.yaml
root@controlplane:~/webapp-color-3# cat webapp-color-pod-2.yaml 
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    command: ["python", "app.py"]
    args: ["--color", "pink"]
```

- command와 args을 보면 아래와 같은 명령어를 실행하는 것을 알 수 있다.
  - `python app.y --color pink`

---

Q10. Create a pod with the given specifications. By default it displays a `blue` background. Set the given command line arguments to change it to `green`

- Pod Name: webapp-green
- Image: kodekloud/webapp-color
- Command line arguments: --color=green

```shell
# --------------------------------------
# pod.yaml 생성
# --------------------------------------
kubectl run webapp-green --image=kodekloud/webapp-color --dry-run=client -o yaml > pod.yaml

# --------------------------------------
# pod.yaml 내용 수정
# --------------------------------------
---
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    args: ["--color", "green"]
    
# --------------------------------------
# pod.yaml 내용 수정
# --------------------------------------
kubectl apply -f pod.yaml 
```







