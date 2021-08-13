# 빠르게 입력받기
# ----------------------
# 입력 데이터가 많은 문제는 
# sys 라이브러리의 readline() 함수를 이용하면
# 시간초과를 피할 수 있다.

import sys

# 하나의 문자열 데이터 입력받기
#  rstrip()는 필수이다.
#  왜냐하면 입력후 enter가 줄 바꿈 기호로 입력 되는데
#  이것을 제거하려면 rstrip()를 써야 한다.
input_data = sys.stdin.readline().rstrip()

# 입력받은 문자열을 그대로 출력
print(input_data)