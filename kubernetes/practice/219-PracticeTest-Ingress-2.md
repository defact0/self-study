Practice Test - Ingress - 2

- https://uklabs.kodekloud.com/topic/practice-test-cka-ingress-networking-2-2/

---

Q1. We have deployed two applications. Explore the setup.

- ok

---

Q2. Let us now deploy an Ingress Controller. First, create a namespace called `ingress-space`.

```shell
root@controlplane:~# kubectl create namespace ingress-space
namespace/ingress-space created
```

---

Q3. The NGINX Ingress Controller requires a ConfigMap object. Create a ConfigMap object in the `ingress-space`.

```shell
root@controlplane:~# kubectl create configmap nginx-configuration --namespace ingress-space
configmap/nginx-configuration created
```

---

Q4. The NGINX Ingress Controller requires a ServiceAccount. Create a ServiceAccount in the `ingress-space` namespace.

```shell
root@controlplane:~# kubectl create serviceaccount ingress-serviceaccount --namespace ingress-space
serviceaccount/ingress-serviceaccount created
```

---

Q5. We have created the Roles and RoleBindings for the ServiceAccount. Check it out!!

- ok

---

Q6. Let us now deploy the Ingress Controller. Create a deployment using the file given.

- Deployed in the correct namespace.
- Replicas: 1
- Use the right image
- Namespace: ingress-space

```shell
cat << EOF | kubectl apply -f -
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ingress-controller
  namespace: ingress-space
spec:
  replicas: 1
  selector:
    matchLabels:
      name: nginx-ingress
  template:
    metadata:
      labels:
        name: nginx-ingress
    spec:
      serviceAccountName: ingress-serviceaccount
      containers:
        - name: nginx-ingress-controller
          image: quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.21.0
          args:
            - /nginx-ingress-controller
            - --configmap=$(POD_NAMESPACE)/nginx-configuration
            - --default-backend-service=app-space/default-http-backend
          env:
            - name: POD_NAME
              valueFrom:
                fieldRef:
                  fieldPath: metadata.name
            - name: POD_NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
          ports:
            - name: http
              containerPort: 80
            - name: https
              containerPort: 443
EOF
```

---

Q7. Let us now create a service to make Ingress available to external users.

- Name: ingress
- Type: NodePort
- Port: 80
- TargetPort: 80
- NodePort: 30080
- Namespace: ingress-space
- Use the right selector

```shell
cat << EOF | kubectl apply -f -
apiVersion: v1
kind: Service
metadata:
  name: ingress
  namespace: ingress-space
spec:
  type: NodePort
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    nodePort: 30080
    name: http
  - port: 443
    targetPort: 443
    protocol: TCP
    name: https
  selector:
    name: nginx-ingress
EOF
```

---

Q8. Create the ingress resource to make the applications available at `/wear` and `/watch` on the Ingress service.

- Ingress Created
- Path: /wear
- Path: /watch
- Configure correct backend service for /wear
- Configure correct backend service for /watch
- Configure correct backend port for /wear service
- Configure correct backend port for /watch service

```shell
cat << EOF | kubectl apply -f -
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
  namespace: app-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - http:
      paths:
      - path: /wear
        pathType: Prefix
        backend:
          service:
           name: wear-service
           port: 
            number: 8080
      - path: /watch
        pathType: Prefix
        backend:
          service:
           name: video-service
           port:
            number: 8080
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: ingress-wear-watch
  namespace: app-space
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
  - http:
      paths:
      - path: /wear
        pathType: Prefix
        backend:
          service:
           name: wear-service
           port: 
            number: 8080
      - path: /watch
        pathType: Prefix
        backend:
          service:
           name: video-service
           port:
            number: 8080
EOF
```

---

Q9. Access the application using the `Ingress` tab on top of your terminal.

- ok