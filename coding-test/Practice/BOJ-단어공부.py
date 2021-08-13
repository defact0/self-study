# https://www.acmicpc.net/problem/1157
#
# [결과]
#  - 정답은 맞췄으나 시간(2292ms)과 코드길이(631B)가 너무 길다.
#  - 다른 사람풀이를 참고해 보자

data = input().lower()
joindata = ''.join(set(data)) # 문자 중복 제거
array = []

for i in joindata:
    cnt = 0
    for j in data:
        if i == j:
            cnt +=1
    array.append((i, int(cnt)))

array = sorted(array, key=lambda arr: arr[1])
length = len(array)
if length > 1:
    f = array[length-2][1]
    s = array[length-1][1]
    if f != s:
        # 가장 많이 사용된 알파벳을 대문자로 출력
        print(array[length-1][0].upper())
    else:
        # 가장 많이 사용된 알파벳이 여러 개 존재하는 경우에는 ?를 출력
        print("?")
else:
    print(array[0][0].upper())


# [다른풀이]
#  - 시간(116ms)과 코드길이(197B)
#
# s = input().upper()
# lis = list(set(s))
# cnt = []
# 
# for c in lis:
#     cnt1 = s.count(c)
#     cnt.append(cnt1)
# 
# if cnt.count(max(cnt)) >= 2:
#     print('?')
# else:
#     print(lis[cnt.index(max(cnt))])