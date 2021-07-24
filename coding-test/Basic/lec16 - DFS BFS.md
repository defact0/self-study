16강 스택과 큐 자료구조 ([링크](https://youtu.be/7iLoLcna7Hw))

---

그래프 탐색 알고리즘 : DFS/BFS

- 탐색(Search)이란 많은 양의 데이터 중에서 **원하는 데이터를 찾는 과정**을 말한다.
- 대표적인 그래프 탐색 알고리즘으로는 DFS 와 BFS가 있다.
- <u>DFS/BFS는 코딩 테스트에서 매우 자주 등장하는 유형</u>이므로 반드시 숙지해야 한다.



스택 자료구조

![lec16-01](./img/lec16-01.png)

- 먼저 들어 온 데이터가 나중에 나가는 형식(선입후출)의 자료구조
- <u>입구와 출구가 동일한 형태</u>로 스택을 시각화할 수 있다.



스택 구현 예제

```python
stack = []

stack.append(5) # 삽입
stack.append(2)
stack.append(3)
stack.append(7)
stack.pop()     # 삭제
stack.append(1)
stack.append(4)
stack.pop()

print(stack[::-1]) # 최상단 원소부터 출력
print(stack) # 최하단 원소부터 출력


# [1, 3, 2, 5]
# [5, 2, 3, 1]
```

https://youtu.be/7iLoLcna7Hw?t=267
