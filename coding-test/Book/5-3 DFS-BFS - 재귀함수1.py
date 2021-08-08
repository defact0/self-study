# 재귀함수1
# - DFS와 BFS를 이해하기 위해 필수
# - 자기 자신을 다시 호출한는 함수
# - 무한대로 실행 할 수는 없다(오류내며 종료)
# - 재귀함수가 언제 끝날지, 종료조건 명시 필요
# - 재귀함수의 수행을 스택자료구조를 이용
# - 점화식(재귀식) => '다이나믹 프로그래밍'으로 이어진다.

def recursive_function():
    print('재귀 함수를 호출합니다.')
    recursive_function()

recursive_function()


# 실행 결과
# 재귀 함수를 호출합니다.
# 재귀 함수를 호출합니다.
# ...
# RecursionError: maximum recursion depth exceeded while calling a Python object