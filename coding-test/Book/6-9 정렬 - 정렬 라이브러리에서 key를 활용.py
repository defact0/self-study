# 정렬 라이브러리에서 key를 활용

array = [('바나나',2), ('사과',5), ('당근',3)]

def setting(data):
    return data[1]

result = sorted(array, key=setting)
print(result)

# 실행결과
# [('바나나', 2), ('당근', 3), ('사과', 5)]