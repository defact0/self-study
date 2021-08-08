# 숫자 카드 게임
# ----------------
# 입력 예시
# 3 3
# 3 1 2
# 4 1 4
# 2 2 2
# ---------------
# 출력 예시
# 2
# ------------
# 각 행마다 가장 작은 수를 찾은 뒤에 그 수 중에서 가장 큰 수를 찾는 것

n, m = map(int, input().split())
result = 0

for i in range(n):
    data = list(map(int, input().split()))
    min_value = min(data)            # 현재 줄에서 가장 작은 수 찾기
    result = max(result, min_value)  # 가장 작은 수들 중에서 가장 큰 수 찾기

print(result)