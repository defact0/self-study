Practice Test - RBAC

- https://uklabs.kodekloud.com/topic/practice-test-role-based-access-controls-2/

---

Q1. Inspect the environment and identify the authorization modes configured on the cluster.

- Check the `kube-apiserver` settings.

```shell
root@controlplane:~# kubectl describe pod kube-apiserver-controlplane -n kube-system
Name:                 kube-apiserver-controlplane
Namespace:            kube-system
Priority:             2000001000
Priority Class Name:  system-node-critical
Node:                 controlplane/10.49.19.6
Start Time:           Tue, 24 Aug 2021 22:50:05 +0000
Labels:               component=kube-apiserver
                      tier=control-plane
Annotations:          kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 10.49.19.6:6443
                      kubernetes.io/config.hash: a2103cc43ac89170055321dd9c28128e
                      kubernetes.io/config.mirror: a2103cc43ac89170055321dd9c28128e
                      kubernetes.io/config.seen: 2021-08-24T22:50:03.866128817Z
                      kubernetes.io/config.source: file
Status:               Running
IP:                   10.49.19.6
IPs:
  IP:           10.49.19.6
Controlled By:  Node/controlplane
Containers:
  kube-apiserver:
    Container ID:  docker://45036b7d993e5a23723c7e140e559ee50c88e0360712aa2262c192abd0acd410
    Image:         k8s.gcr.io/kube-apiserver:v1.20.0
    Image ID:      docker-pullable://k8s.gcr.io/kube-apiserver@sha256:8b8125d7a6e4225b08f04f65ca947b27d0cc86380bf09fab890cc80408230114
    Port:          <none>
    Host Port:     <none>
    Command:
      kube-apiserver
      --advertise-address=10.49.19.6
      --allow-privileged=true
      --authorization-mode=Node,RBAC
```

- `--authorization-mode=Node,RBAC`

---

Q2. How many roles exist in the `default` namespace?

```shell
root@controlplane:~# kubectl get roles
No resources found in default namespace.
```

- 0

---

Q3. How many roles exist in all namespaces together?

```shell
root@controlplane:~# kubectl get roles --all-namespaces
NAMESPACE     NAME                                             CREATED AT
blue          developer                                        2021-08-24T23:01:59Z
kube-public   kubeadm:bootstrap-signer-clusterinfo             2021-08-24T22:50:01Z
kube-public   system:controller:bootstrap-signer               2021-08-24T22:49:59Z
kube-system   extension-apiserver-authentication-reader        2021-08-24T22:49:59Z
kube-system   kube-proxy                                       2021-08-24T22:50:02Z
kube-system   kubeadm:kubelet-config-1.20                      2021-08-24T22:50:00Z
kube-system   kubeadm:nodes-kubeadm-config                     2021-08-24T22:50:00Z
kube-system   system::leader-locking-kube-controller-manager   2021-08-24T22:49:59Z
kube-system   system::leader-locking-kube-scheduler            2021-08-24T22:49:59Z
kube-system   system:controller:bootstrap-signer               2021-08-24T22:49:59Z
kube-system   system:controller:cloud-provider                 2021-08-24T22:49:59Z
kube-system   system:controller:token-cleaner                  2021-08-24T22:49:59Z

root@controlplane:~# kubectl get roles --all-namespaces --no-headers | wc -l
12
```

- 12

---

Q4. What are the resources the `kube-proxy` role in the `kube-system` namespace is given access to?

```shell
root@controlplane:~# kubectl describe role kube-proxy -n kube-system
Name:         kube-proxy
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources   Non-Resource URLs  Resource Names  Verbs
  ---------   -----------------  --------------  -----
  configmaps  []                 [kube-proxy]    [get]
```

- `configmaps`

---

Q5. What actions can the `kube-proxy` role perform on `configmaps`?

```shell
root@controlplane:~# kubectl describe role -n kube-system kube-proxy
Name:         kube-proxy
Labels:       <none>
Annotations:  <none>
PolicyRule:
  Resources   Non-Resource URLs  Resource Names  Verbs
  ---------   -----------------  --------------  -----
  configmaps  []                 [kube-proxy]    [get]
```

- `get`

---

Q6. Which of the following statements are true?

- kube-proxy role can get details of configmap object by the name kube-proxy

---

Q7. Which account is the `kube-proxy` role assigned to it?

```shell
root@controlplane:~# kubectl describe rolebinding kube-proxy -n kube-system
Name:         kube-proxy
Labels:       <none>
Annotations:  <none>
Role:
  Kind:  Role
  Name:  kube-proxy
Subjects:
  Kind   Name                                             Namespace
  ----   ----                                             ---------
  Group  system:bootstrappers:kubeadm:default-node-token  
```

- `Group: system:bootstrappers:kubeadm:default-node-token`

---

Q8. A user `dev-user` is created. User's details have been added to the `kubeconfig` file. Inspect the permissions granted to the user. Check if the user can list pods in the `default` namespace.

- Use the `--as dev-user` option with `kubectl` to run commands as the `dev-user`.

```shell
root@controlplane:~# kubectl get pods --as dev-user
Error from server (Forbidden): pods is forbidden: User "dev-user" cannot list resource "pods" in API group "" in the namespace "default"
```

- dev-user does not have permissions to list pods

---

Q9. Create the necessary roles and role bindings required for the `dev-user` to create, list and delete pods in the `default` namespace.

- Role: developer
- Role Resources: pods
- Role Actions: list
- Role Actions: create
- RoleBinding: dev-user-binding
- RoleBinding: Bound to dev-user

```shell
#
# To create a Role
kubectl create role developer --namespace=default --verb=list,create --resource=pods

#
# To create a RoleBinding
kubectl create rolebinding dev-user-binding --namespace=default --role=developer --user=dev-user

#
# 아니면 role 리소스를 yaml 파일로 만드는 방법
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: default
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "create"]

---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: dev-user-binding
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

---

Q10. The `dev-user` is trying to get details about the `dark-blue-app` pod in the `blue` namespace. Investigate and fix the issue.

- We have created the required roles and rolebindings, but something seems to be wrong.

```shell
#
# resourceNames 부분을 수정
kubectl edit role developer -n blue
```

---

Q11. Grant the `dev-user` permissions to create deployments in the `blue` namespace.

- Remember to add both groups `"apps"` and `"extensions"`.

```shell
---
kind: Role
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  namespace: blue
  name: deploy-role
rules:
- apiGroups: ["apps", "extensions"]
  resources: ["deployments"]
  verbs: ["create"]

---
kind: RoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: dev-user-deploy-binding
  namespace: blue
subjects:
- kind: User
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: Role
  name: deploy-role
  apiGroup: rbac.authorization.k8s.io
```

