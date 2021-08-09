18강 DFS 알고리즘 ([링크](https://youtu.be/1vLqC1rItM8))

---

- DFS (Depth-First Search)

  - 깊이 우선 탐색
  - 깊은 부분을 우선적으로 탐색하는 알고리즘
  - 스택 자료구조(혹은 재귀 함수)를 이용
- 동작 과정 ([설명](https://youtu.be/1vLqC1rItM8?t=51))
  1. 탐색 시작 노드를 스택에 삽입 하고 방문 처리
  2. 스택의 최상단 노드에 방문하지 않은 인접한 노드가 하나라도 있으면 그 노드를 스택에 넣고 방문처리. 방문하지 않은 인접 노드가 없으면 스택에서 최상단 노드를 꺼낸다.
  3. 더 이상 2번 항목을 수행할 수 없을 때까지 반복

```python
# DFS 메서드 정의
def dfs(graph, v, visited):
    # 현재 노드를 방문 처리
    visited[v] = True
    print(v, end=' ')

    # 현재 노드와 연결된 다른 노드를 재귀적으로 방문
    for i in graph[v]:
        if not visited[i]:
            dfs(graph, i, visited)
```



