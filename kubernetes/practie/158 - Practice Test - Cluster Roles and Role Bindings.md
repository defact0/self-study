Practice Test - Cluster Roles and Role Bindings

- https://uklabs.kodekloud.com/topic/practice-test-cluster-roles-2/

---

Q1. How many `ClusterRoles` do you see defined in the cluster?

```shell
root@controlplane:~# kubectl get clusterroles --no-headers | wc -l
63
```

---

Q2. How many `ClusterRoleBindings` exist on the cluster?

```shell
root@controlplane:~# kubectl get clusterrolebindings --no-headers | wc -l
48
```

---

Q3. What namespace is the `cluster-admin` clusterrole part of?

- `Cluster Roles are cluster wide and not part of any namespace`

---

Q4. What user/groups are the `cluster-admin` role bound to?

- The ClusterRoleBinding for the role is with the same name.

```shell
root@controlplane:~# kubectl describe clusterrolebinding cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
Role:
  Kind:  ClusterRole
  Name:  cluster-admin
Subjects:
  Kind   Name            Namespace
  ----   ----            ---------
  Group  system:masters  
```

- `system:masters`

---

Q5. What level of permission does the `cluster-admin` role grant?

- Inspect the `cluster-admin` role's privileges.

```shell
root@controlplane:~# kubectl describe clusterrole cluster-admin
Name:         cluster-admin
Labels:       kubernetes.io/bootstrapping=rbac-defaults
Annotations:  rbac.authorization.kubernetes.io/autoupdate: true
PolicyRule:
  Resources  Non-Resource URLs  Resource Names  Verbs
  ---------  -----------------  --------------  -----
  *.*        []                 []              [*]
             [*]                []              [*]
```

- `Perform any action on any resource in the cluster`

---

Q6. A new user `michelle` joined the team. She will be focusing on the `nodes` in the cluster. Create the required `ClusterRoles` and `ClusterRoleBindings` so she gets access to the `nodes`.

- Grant permission to list nodes

```shell
#
# cr.yaml
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: node-admin
rules:
- apiGroups: [""]
  resources: ["nodes"]
  verbs: ["get", "watch", "list", "create", "delete"]

---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: michelle-binding
subjects:
- kind: User
  name: michelle
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: node-admin
  apiGroup: rbac.authorization.k8s.io

#
# create cr.yaml
root@controlplane:~# vi cr.yaml
root@controlplane:~# kubectl create -f cr.yaml 
clusterrole.rbac.authorization.k8s.io/node-admin created
clusterrolebinding.rbac.authorization.k8s.io/michelle-binding created
```

---

Q7. `michelle`'s responsibilities are growing and now she will be responsible for storage as well. Create the required `ClusterRoles` and `ClusterRoleBindings` to allow her access to Storage.

Get the API groups and resource names from command `kubectl api-resources`. Use the given spec:

- ClusterRole: storage-admin
- Resource: persistentvolumes
- Resource: storageclasses
- ClusterRoleBinding: michelle-storage-admin
- ClusterRoleBinding Subject: michelle
- ClusterRoleBinding Role: storage-admin

```shell
#
# cr2.yaml
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: storage-admin
rules:
- apiGroups: [""]
  resources: ["persistentvolumes"]
  verbs: ["get", "watch", "list", "create", "delete"]
- apiGroups: ["storage.k8s.io"]
  resources: ["storageclasses"]
  verbs: ["get", "watch", "list", "create", "delete"]

---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: michelle-storage-admin
subjects:
- kind: User
  name: michelle
  apiGroup: rbac.authorization.k8s.io
roleRef:
  kind: ClusterRole
  name: storage-admin
  apiGroup: rbac.authorization.k8s.io

#
# create cr2.yaml
root@controlplane:~# vi cr2.yaml
root@controlplane:~# kubectl create -f cr2.yaml 
clusterrole.rbac.authorization.k8s.io/storage-admin created
clusterrolebinding.rbac.authorization.k8s.io/michelle-storage-admin created
```

