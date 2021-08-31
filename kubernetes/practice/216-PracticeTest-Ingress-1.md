Practice Test - Ingress - 1

- https://uklabs.kodekloud.com/topic/practice-test-cka-ingress-networking-1-2/

---

Q1. We have deployed Ingress Controller, resources and applications. Explore the setup.

- ok

---

Q2. Which namespace is the `Ingress Controller` deployed in?

```shell
root@controlplane:~# kubectl get all -A
NAMESPACE       NAME                                            READY   STATUS              RESTARTS   AGE
app-space       pod/default-backend-5cf9bfb9d-h72r7             1/1     Running             0          76s
app-space       pod/webapp-video-84f8655bd8-9ghqq               0/1     ContainerCreating   0          76s
app-space       pod/webapp-wear-6ff9445955-wr6j6                0/1     ContainerCreating   0          75s
ingress-space   pod/nginx-ingress-controller-697cfbd4d9-psfg5   1/1     Running             0          77s
...
```

- `ingress-space`

---

Q3. What is the name of the Ingress Controller Deployment?

```shell
root@controlplane:~# kubectl get deploy -A
NAMESPACE       NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
app-space       default-backend            1/1     1            1           2m38s
app-space       webapp-video               1/1     1            1           2m38s
app-space       webapp-wear                1/1     1            1           2m38s
ingress-space   nginx-ingress-controller   1/1     1            1           2m40s
kube-system     coredns                    2/2     2            2           8m7s
```

- `nginx-ingress-controller`

---

Q4. Which namespace are the applications deployed in?

```shell
root@controlplane:~# kubectl get po -A
NAMESPACE       NAME                                        READY   STATUS    RESTARTS   AGE
app-space       default-backend-5cf9bfb9d-h72r7             1/1     Running   0          3m21s
app-space       webapp-video-84f8655bd8-9ghqq               1/1     Running   0          3m21s
app-space       webapp-wear-6ff9445955-wr6j6                1/1     Running   0          3m20s
ingress-space   nginx-ingress-controller-697cfbd4d9-psfg5   1/1     Running   0          3m22s
...
```

- `app-space`

---

Q5. How many applications are deployed in the `app-space` namespace?

```shell
root@controlplane:~# kubectl get deploy --namespace app-space
NAME              READY   UP-TO-DATE   AVAILABLE   AGE
default-backend   1/1     1            1           5m9s
webapp-video      1/1     1            1           5m9s
webapp-wear       1/1     1            1           5m9s
```

- `3`

---

Q6. Which namespace is the Ingress Resource deployed in?

```shell
root@controlplane:~# kubectl get ingress --all-namespaces
NAMESPACE   NAME                 CLASS    HOSTS   ADDRESS   PORTS   AGE
app-space   ingress-wear-watch   <none>   *                 80      5m55s
```

- `app-space`

----

Q7. What is the name of the Ingress Resource?

- `ingress-wear-watch`

---

Q8. What is the `Host` configured on the `Ingress Resource`?

```shell
root@controlplane:~# kubectl describe ingress --namespace app-space
Name:             ingress-wear-watch
Namespace:        app-space
Address:          
Default backend:  default-http-backend:80 (<error: endpoints "default-http-backend" not found>)
Rules:
  Host        Path  Backends
  ----        ----  --------
  *           
              /wear    wear-service:8080 (10.244.0.7:8080)
              /watch   video-service:8080 (10.244.0.6:8080)
Annotations:  nginx.ingress.kubernetes.io/rewrite-target: /
              nginx.ingress.kubernetes.io/ssl-redirect: false
Events:       <none>
```

- `All Hosts (*)`

---

Q9. What backend is the `/wear` path on the Ingress configured with?

- `wear-service`

---

Q10. At what path is the video streaming application made available on the `Ingress`?

- `/watch`

---

Q11. If the requirement does not match any of the configured paths what service are the requests forwarded to?

- `default-http-backend`

---

Q12. Now view the Ingress Service using the tab at the top of the terminal. Which page do you see?

- `404 Error page`
  - Click on the tab named `Ingress`.

---

Q13. View the applications by appending `/wear` and `/watch` to the URL you opened in the previous step.

- ok

---

Q14. You are requested to change the URLs at which the applications are made available.

- Ingress: ingress-wear-watch
- Path: /stream
- Backend Service: video-service
- Backend Service Port: 8080

```shell
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  name: ingress-wear-watch
  namespace: app-space
spec:
  rules:
  - http:
      paths:
      - backend:
          service:
            name: wear-service
            port: 
              number: 8080
        path: /wear
        pathType: Prefix
      - backend:
          service:
            name: video-service
            port: 
              number: 8080
        path: /stream
        pathType: Prefix
EOF
```

---

Q15. View the Video application using the `/stream` URL in your browser.

- ok

---

Q16. A user is trying to view the `/eat` URL on the Ingress Service. Which page would he see?

- ` 404 ERROR PAGE`

---

Q17. Due to increased demand, your business decides to take on a new venture. You acquired a food delivery company. Their applications have been migrated over to your cluster.

- ok

---

Q18. You are requested to add a new path to your ingress to make the food delivery application available to your customers.

- Ingress: ingress-wear-watch
- Path: /eat
- Backend Service: food-service
- Backend Service Port: 8080

```shell
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  name: ingress-wear-watch
  namespace: app-space
spec:
  rules:
  - http:
      paths:
      - backend:
          service:
            name: wear-service
            port: 
              number: 8080
        path: /wear
        pathType: Prefix
      - backend:
          service:
            name: video-service
            port: 
              number: 8080
        path: /stream
        pathType: Prefix
      - backend:
          service:
            name: food-service
            port: 
              number: 8080
        path: /eat
        pathType: Prefix
EOF
```

---

Q19. View the Food delivery application using the `/eat` URL in your browser.

- ok

---

Q20. A new payment service has been introduced. Since it is critical, the new application is deployed in its own namespace.

- ` CRITICAL-SPACE`

---

Q21. What is the name of the deployment of the new application?

```shell
root@controlplane:~# kubectl get deploy --all-namespaces
NAMESPACE        NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
app-space        default-backend            1/1     1            1           13m
app-space        webapp-food                1/1     1            1           102s
app-space        webapp-video               1/1     1            1           13m
app-space        webapp-wear                1/1     1            1           13m
critical-space   webapp-pay                 1/1     1            1           46s
ingress-space    nginx-ingress-controller   1/1     1            1           13m
kube-system      coredns                    2/2     2            2           19m
```

- `webapp-pay`

---

Q22. You are requested to make the new application available at `/pay`.

- Ingress Created
- Path: /pay
- Configure correct backend service
- Configure correct backend port

```shell
cat << EOF | kubectl apply -f -
 apiVersion: extensions/v1beta1
 kind: Ingress
 metadata:
   name: test-ingress
   namespace: critical-space
   annotations:
     nginx.ingress.kubernetes.io/rewrite-target: /
 spec:
   rules:
   - http:
       paths:
       - path: /pay
         backend:
           serviceName: pay-service
           servicePort: 8282
EOF
```

---

Q23. View the Payment application using the `/pay` URL in your browser.

Click on the `Ingress` tab above your terminal, if its not open already, and append `/pay` to the URL in the browser.

- ok