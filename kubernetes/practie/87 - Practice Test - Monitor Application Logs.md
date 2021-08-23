Practice Test - Monitor Application Logs

- https://uklabs.kodekloud.com/topic/practice-test-managing-application-logs-2/

---

Q1. We have deployed a POD hosting an application. Inspect it. Wait for it to start.

```shell
root@controlplane:~# kubectl get pods
NAME       READY   STATUS    RESTARTS   AGE
webapp-1   1/1     Running   0          36s
```

---

Q2. A user - `USER5` - has expressed concerns accessing the application. Identify the cause of the issue.

- Inspect the logs of the POD

```shell
root@controlplane:~# kubectl logs webapp-1 | grep USER5
[2021-08-23 02:01:08,553] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:13,559] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:18,566] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:23,573] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:28,580] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:33,587] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:38,593] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:43,599] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:48,606] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:53,613] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:01:58,619] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:02:03,628] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:02:08,633] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:02:13,673] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:02:18,680] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:02:23,690] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
```

- `Account Locked due to Many Failed Attempts`

---

Q3. We have deployed a new POD - `webapp-2` - hosting an application. Inspect it. Wait for it to start.

```shell
root@controlplane:~# kubectl get pod
NAME       READY   STATUS    RESTARTS   AGE
webapp-1   1/1     Running   0          2m31s
webapp-2   2/2     Running   0          14s
```

---

Q4. A user is reporting issues while trying to purchase an item. Identify the user and the cause of the issue.

- Inspect the logs of the webapp in the POD

```shell
root@controlplane:~# kubectl logs webapp-2
error: a container name must be specified for pod webapp-2, choose one of: [simple-webapp db]

root@controlplane:~# kubectl logs webapp-2 -c simple-webapp | grep WARNING
[2021-08-23 02:03:15,195] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:03:18,200] WARNING in event-simulator: USER30 Order failed as the item is OUT OF STOCK.
[2021-08-23 02:03:20,203] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:03:25,210] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:03:26,211] WARNING in event-simulator: USER30 Order failed as the item is OUT OF STOCK.
[2021-08-23 02:03:30,215] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2021-08-23 02:03:34,292] WARNING in event-simulator: USER30 Order failed as the item is OUT OF STOCK.
```

- `USER30 - Item Out of Stock`

