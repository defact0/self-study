# 스택
# - 박스쌓기
# - 선입후출(FILO) 또는 후입선출(LIFO)
# - 삽입은 append() 삭제는 pop() 사용
stack = []

stack.append(5)    # 삽입
stack.append(2)
stack.append(3)
stack.append(7)
stack.pop()        # 삭제
stack.append(1)
stack.append(4)
stack.pop()

print(stack)       # 최하단 원소부터 출력
print(stack[::-1]) # 최상단 원소부터 출력

# 실행 결과
# [5, 2, 3, 1]
# [1, 3, 2, 5]