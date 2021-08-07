# 1이 될 때까지
# ---------------
# 입력 예시
# 25 5
# 출력 예시
# 2
# ---------------

n, k = map(int, input().split())
result = 0

while True:
    target = (n//k)*k    # target 이라는 변수에 N이 K로 나누어 떨어지는 가장 가까운 수를 저장
    result += (n-target) # 총 연산횟수 저장, -1을 수행한 횟수를 구할 수 있다.
    n = target           # -1 이후 K로 나누어 떨어지는 가장 가까운 수 이기 때문에

    # N이 K보다 작을 때(더 이상 나눌 수 없을 때) 반복문 탈출
    if n < k:
        break

    result += 1 # K로 나누는 연산을 하므로 +1 추가
    n //= k

# 마지막으로 남은 수에 대하여 1씩 빼기
result += (n-1)
print(result)