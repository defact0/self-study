19강 BFS 알고리즘 ([링크](https://youtu.be/CJiF-muKz30))

---

- BFS (Breadth-First Search)
  - 너비 우선 탐색
  - 가까운 노드부터 우선적으로 탐색하는 알고리즘
  - 큐 자료구조를 이용
- 동작 과정
  1. 탐색 시작 노드를 큐에 삽입하고 방문 처리
  2. 큐에서 노드를 꺼낸 뒤에 해당 노드의 인접 노드 중에서 방문하지 않은 노드를 모두 큐에 삽입하고 방문 처리
  3. 더 이상 2번의 과정을 수행할 수 없을 때 까지 반복

```python
# BFS 소스코드 구현
def bfs(x, y):
    # 큐(Queue) 구현을 위해 deque 라이브러리 사용
    queue = deque()
    queue.append((x,y))

    # 큐가 빌 때까지 반복
    while queue:
        x, y = queue.popleft()

        # 현재 위치에서 네 방향으로의 위치 확인
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]

            # 미로 찾기 공간을 벗어난 경우 무시
            if nx < 0 or ny < 0 or nx >= n or ny >= m:
                continue
            # 벽인 경우 무시
            if graph[nx][ny] == 0:
                continue
            # 해당 노드를 처음 방문하는 경우에만 최단 거리 기록
            if graph[nx][ny] == 1:
                graph[nx][ny] = graph[x][y] + 1
                queue.append((nx,ny))
    # 가장 오른쪽 아래까지의 최단 거리 반환
    return graph[n-1][m-1]
```

