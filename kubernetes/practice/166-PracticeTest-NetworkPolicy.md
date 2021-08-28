Practice Test - Network Policy

- https://uklabs.kodekloud.com/topic/practice-test-network-policies-2/

---

Q1. How many network policies do you see in the environment?

![](https://e7988b28ad784e25.labs.kodekloud.com/images/kubernetes-ckad-network-policies-1.jpg)

- We have deployed few web applications, services and network policies. Inspect the environment.

```shell
root@controlplane:~# kubectl get networkpolicy
NAME             POD-SELECTOR   AGE
payroll-policy   name=payroll   29m
```

---

Q2. What is the name of the Network Policy?

- `payroll-policy`

---

Q3. Which pod is the Network Policy applied on?

```shell
root@controlplane:~# kubectl get networkpolicy
NAME             POD-SELECTOR   AGE
payroll-policy   name=payroll   29m

root@controlplane:~# kubectl get po --show-labels | grep name=payroll
payroll    1/1     Running   0          30m   name=payroll
```

- `payroll`

---

Q4. What type of traffic is this Network Policy configured to handle?

```shell
root@controlplane:~# kubectl describe networkpolicy
Name:         payroll-policy
Namespace:    default
Created on:   2021-08-28 19:30:13 +0000 UTC
Labels:       <none>
Annotations:  <none>
Spec:
  PodSelector:     name=payroll
  Allowing ingress traffic:
    To Port: 8080/TCP
    From:
      PodSelector: name=internal
  Not affecting egress traffic
  Policy Types: Ingress
```

- Policy Types: `Ingress`

---

Q5. What is the impact of the rule configured on this Network Policy?

![](https://e7988b28ad784e25.labs.kodekloud.com/images/kubernetes-ckad-network-policies-5.jpg)

```shell
root@controlplane:~# kubectl describe networkpolicy
Name:         payroll-policy
Namespace:    default
Created on:   2021-08-28 19:30:13 +0000 UTC
Labels:       <none>
Annotations:  <none>
Spec:
  PodSelector:     name=payroll
  Allowing ingress traffic:
    To Port: 8080/TCP
    From:
      PodSelector: name=internal
  Not affecting egress traffic
  Policy Types: Ingress
```



- Traffic From Internal to Payroll POD is allowed

---

Q6. What is the impact of the rule configured on this Network Policy?

```shell
root@controlplane:~# kubectl describe networkpolicy
Name:         payroll-policy
Namespace:    default
Created on:   2021-08-28 19:30:13 +0000 UTC
Labels:       <none>
Annotations:  <none>
Spec:
  PodSelector:     name=payroll
  Allowing ingress traffic:
    To Port: 8080/TCP
    From:
      PodSelector: name=internal
  Not affecting egress traffic
  Policy Types: Ingress
```

- Internal POD can access port 8080 on Payroll POD

---

Q7. Access the UI of these applications using the link given above the terminal.

- ok

---

Q8. Perform a connectivity test using the User Interface in these Applications to access the `payroll-service` at port `8080`.

![](https://e7988b28ad784e25.labs.kodekloud.com/images/kubernetes-ckad-network-policies-8.jpg)

- Only Internal application can access payroll service

---

Q9. Perform a connectivity test using the User Interface of the Internal Application to access the `external-service` at port `8080`.

- Successful

---

Q10. Create a network policy to allow traffic from the `Internal` application only to the `payroll-service` and `db-service`.

![](https://e7988b28ad784e25.labs.kodekloud.com/images/kubernetes-ckad-network-policies-9.jpg)

- Use the spec given on the below. You might want to enable ingress traffic to the pod to test your rules in the UI.
  - Policy Name: internal-policy
  - Policy Type: Egress
  - Egress Allow: payroll
  - Payroll Port: 8080
  - Egress Allow: mysql
  - MySQL Port: 3306

```shell
# ----------------------------------------------
# get networkpolicy
root@controlplane:~# kubectl get networkpolicy
NAME             POD-SELECTOR   AGE
payroll-policy   name=payroll   41m

# ----------------------------------------------
# get networkpolicy
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      name: internal
  policyTypes:
  - Egress
  - Ingress
  ingress:
    - {}
  egress:
  - to:
    - podSelector:
        matchLabels:
          name: mysql
    ports:
    - protocol: TCP
      port: 3306

  - to:
    - podSelector:
        matchLabels:
          name: payroll
    ports:
    - protocol: TCP
      port: 8080

  - ports:
    - port: 53
      protocol: UDP
    - port: 53
      protocol: TCP
EOF

# ----------------------------------------------
# get networkpolicy
root@controlplane:~# kubectl get networkpolicy
NAME              POD-SELECTOR    AGE
internal-policy   name=internal   4s
payroll-policy    name=payroll    41m

# ----------------------------------------------
# get svc -n kube-system
root@controlplane:~# kubectl get svc -n kube-system
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)                  AGE
kube-dns   ClusterIP   10.96.0.10   <none>        53/UDP,53/TCP,9153/TCP   76m
```