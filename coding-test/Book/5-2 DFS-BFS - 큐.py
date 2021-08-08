# 큐
# - 대기줄
# - 선입선출(FIFO)
# - collections 모듈의 deque 자료구조 이용
# - 삽입 append(), 삭제 popleft()

from collections import deque

# 큐(Queue) 구현을 위해 deque 라이브러리 사용
queue = deque()

queue.append(5) # 삽입
queue.append(2)
queue.append(3)
queue.append(7)
queue.popleft() # 삭제
queue.append(1)
queue.append(4)
queue.popleft()

print(queue)    # 먼저 들어온 순서대로 출력
queue.reverse() # 다음 출력을 위해 역순으로 바꾸기
print(queue)    # 나중에 들어온 원소부터 출력

# 실행 결과
# deque([3, 7, 1, 4])
# deque([4, 1, 7, 3])