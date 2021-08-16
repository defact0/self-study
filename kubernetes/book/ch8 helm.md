### :ship: helm 패키지 매니저

> application 배포시 하나의 패키지로 묶어서 배포하면 관리(추가, 업그레이드)가 편리해 진다.
> 이러한 일을 할 수 있는 것이 쿠버네티스의 패키지 매니저인 helm 이다.

helm 이란?

- apt, yum, pip 툴과 같이 플랫폼의 패키지를 관리하는 매니저이다.
- YAML 형식으로 구성되어 있고 이것을 chart라고 한다.
  - values.yaml
    - 사용자가 설정하는 파일
    - 자주 바뀌는 설정을 기록
  - templates 디렉터리
    - 설치할 리소스 파일들이 존재하는 디렉터리
    - 패키지의 뼈대를 이룸

helm 설치

- https://helm.sh/ko/docs/intro/install/

chart 생성

```shell
# helm create <CHART_NAME>
helm create mychart
```

- Chart.yaml
  - chart 이름, 버전 등의 전반적인 정보 포함
- /charts
  - chart 속에 다른 여러 chart를 넣을 수 있다 (기본-비어있음)
- /templates
  - 쿠버네티스 리소스가 들어잇는 폴더
- values.yaml
  - 사용ㅈ자가 정의하는 설정파일

chart 설치

```shell
# helm install <CHART_NAME> <CHART_PATH>
helm install foo ./mychart
```

chart 리스트 조회

```shell
helm list

# 네임스페이스 조회
helm list -n kube-system
```

chart 랜더링

```shell
# helm template <CHART_PATH>
helm template foo ./mychart > foo-ouput.yaml
```

- template 명령은 해당 chart를 종합하여 하나의 yaml 파일로 만든다.
- kubectl 의 `--dry-run` 옵션과 유사하다

chart 업그레이드

```shell
# helm upgrade <CHART_NAME> <CHART_PATH>
helm upgrade foo ./mychart
```

- 이미 설치된 chart에서 values.yaml 값을 수정하고 업데이트 가능

chart 배포상태 확인

```shell
# helm status <CHART_NNAME>
helm status foo
```

chart 삭제

```shell
# helm delete <CHART_NAME>
helm delete foo
```

원격 리파지토리(repository)

- helm에는 chart 원격 저장소인 리파지토리가 있다.
- 여러 chart를 한 곳에 묶에서 보관해놓은 저장소이다.
- 사용자는 온라인상에 제공되는 리파지토리를 추가하여 원격 저장소로 부터 chart를 로컬 클러스터에 설치할 수 있다.

```shell
# 리파지토리 추가
helm repo add stable https://kubernetes-charts.storage.googleapis.com
# 리파지토리 업데이트
helm repo update
# 리파지토리 조회
helm repo list
# 리파지토리내 chart 조회
#  - helm 허브 https://hub.helm.sh/charts
helm search repo stable
helm search repo stable/airflow
```

chart fetch

- 원격 설치 말고 로컬 디렉토리로 다운로드해서 설치하는 방법
- tar로 묶인 상태로 저장

```shell
helm fetch --untar stable/wordpress --version 9.0.3
helm install wp-fetch ./wordpress
```

