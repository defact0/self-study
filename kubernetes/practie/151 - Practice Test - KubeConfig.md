Practice Test - KubeConfig

- https://uklabs.kodekloud.com/topic/practice-test-kubeconfig-2/

---

Q1. Where is the default kubeconfig file located in the current environment?

- Find the current home directory by looking at the HOME environment variable.
  - `/root/.kube/config`

---

Q2. How many clusters are defined in the default kubeconfig file?

```shell
root@controlplane:~# kubectl config view
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://controlplane:6443
  name: kubernetes
contexts:
- context:
    cluster: kubernetes
    user: kubernetes-admin
  name: kubernetes-admin@kubernetes
current-context: kubernetes-admin@kubernetes
kind: Config
preferences: {}
users:
- name: kubernetes-admin
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
```

- 1

---

Q3. How many Users are defined in the default kubeconfig file?

- Q2의 내용을 참고, 정답은 1 이다.

---

Q4. How many contexts are defined in the default kubeconfig file?

- Q2의 내용을 참고, 정답은 1 이다.

---

Q5. What is the user configured in the current context?

- Q2의 내용을 참고, 정답은 `kubernetes-admin` 이다.

---

Q6. What is the name of the cluster configured in the default kubeconfig file?

- Q2의 내용을 참고, 정답은 `kubernetes` 이다.

---

Q7. A new kubeconfig file named `my-kube-config` is created. It is placed in the `/root` directory. How many clusters are defined in that kubeconfig file?

```shell
root@controlplane:~# kubectl config view --kubeconfig my-kube-config
apiVersion: v1
clusters:
- cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
  name: development
- cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
  name: kubernetes-on-aws
- cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
  name: production
- cluster:
    certificate-authority: /etc/kubernetes/pki/ca.crt
    server: https://controlplane:6443
  name: test-cluster-1
contexts:
- context:
    cluster: kubernetes-on-aws
    user: aws-user
  name: aws-user@kubernetes-on-aws
- context:
    cluster: test-cluster-1
    user: dev-user
  name: research
- context:
    cluster: development
    user: test-user
  name: test-user@development
- context:
    cluster: production
    user: test-user
  name: test-user@production
current-context: test-user@development
kind: Config
preferences: {}
users:
- name: aws-user
  user:
    client-certificate: /etc/kubernetes/pki/users/aws-user/aws-user.crt
    client-key: /etc/kubernetes/pki/users/aws-user/aws-user.key
- name: dev-user
  user:
    client-certificate: /etc/kubernetes/pki/users/dev-user/developer-user.crt
    client-key: /etc/kubernetes/pki/users/dev-user/dev-user.key
- name: test-user
  user:
    client-certificate: /etc/kubernetes/pki/users/test-user/test-user.crt
    client-key: /etc/kubernetes/pki/users/test-user/test-user.key
```

- 4

---

Q8. How many contexts are configured in the `my-kube-config` file?

- Q7의 내용을 참고, 정답은 4 이다.

---

Q9. What user is configured in the `research` context?

- Q7의 내용을 참고, 정답은 `dev-user` 이다.

---

Q10. What is the name of the client-certificate file configured for the `aws-user`?

- Q7의 내용을 참고, 정답은 `/etc/kubernetes/pki/users/aws-user/aws-user.crt` 이다.

---

Q11. What is the current context set to in the `my-kube-config` file?

- Q7의 내용을 참고
  - `current-context: test-user@development`

---

Q12. I would like to use the `dev-user` to access `test-cluster-1`. Set the current context to the right one so I can do that.

- Once the right context is identified, use the `kubectl config use-context` command.

```shell
#
# current-context 변경
#
root@controlplane:~# kubectl config --kubeconfig=/root/my-kube-config use-context research
Switched to context "research".

#
# current-context 확인
#
root@controlplane:~# kubectl config --kubeconfig=/root/my-kube-config current-context
research
root@controlplane:~# 
```

---

Q13. We don't want to have to specify the kubeconfig file option on each command. Make the `my-kube-config` file the default kubeconfig.

```shell
root@controlplane:~# mv .kube/config .kube/config.bak 
root@controlplane:~# cp /root/my-kube-config .kube/config
```



---

Q14. With the current-context set to `research`, we are trying to access the cluster. However something seems to be wrong. Identify and fix the issue.

- Try running the `kubectl get pods` command and look for the error. All users certificates are stored at `/etc/kubernetes/pki/users`.

```shell
#
# 문제 확인
root@controlplane:~# kubectl get pods master 
error: unable to read client-cert /etc/kubernetes/pki/users/dev-user/developer-user.crt for dev-user due to open /etc/kubernetes/pki/users/dev-user/developer-user.crt: no such file or directory

# 
# /etc/kubernetes/pki/users/dev-user 디렉토리에는 아래와 같은 파일이 존재 한다.
# dev-user.crt  dev-user.csr  dev-user.key

vi /root/.kube/config
# developer-user.crt 부분을 찾아, dev-user.crt 으로 수정해 주어야 한다.

root@controlplane:~# kubectl get pods master 
Error from server (NotFound): pods "master" not found
# 이렇게 메세지가 나오면 정상
```

---

[참고](https://github.com/kodekloudhub/certified-kubernetes-administrator-course/blob/master/docs/07-Security/14-Practice-Test-KubeConfig.md)