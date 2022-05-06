# 주가 예측 모델에서의 분할 예측을 통한 성능향상 탐구 논문 (2022)
논문 링크: https://doi.org/10.6109/jkiice.2022.26.4.503

본 Repository는 논문에 사용된 AE-DNN 모델의 생성에 사용한 데이터의 다운로드 & 전처리 코드를 모아놓았습니다.  
유도희가 담당한 [데이터 다운로드 & 전처리 코드](https://github.com/doch2/AE-DNN-model-data), 여태건우가 담당한 [인공지능 코드](https://github.com/ytgw0/AE_dnn-and-DNN_experiment)로 나누어 각 GitHub 계정에 Repository를 생성하였습니다.<br>  
코드 작성시에 진행한 이전 Commit 내역은 별도의 Private Repository에 존재합니다.
<div align="center"><img style="width:90%;" alt="code FlowChart" src="https://user-images.githubusercontent.com/30923566/153738292-51912299-d78e-4b8e-aece-9cd3437fd3a8.png"></div>

## 초록
본 논문의 연구 취지는 예측하고자 하는 다음 날과 이전 날의 시가 사이 변동률을 예측값으로 두고 시가를 예측하는 기존 논문들과는 다르게 예측하고자 하는 다음날의 주가 순위를 일정한 간격으로 분할하여 생성된 각 구간마다의 시가 변동률을 예측값으로 하는 모델을 통하여 최종적인 다음날의 시가 변동률을 예측하는 새로운 시계열 데이터 예측 방식을 제안하고자 한다. 예측값의 세분화 정도와 입력 데이터의 종류에 따른 모델의 성능 변화를 분석했으며 연구 결과 예측값의 세분화 정도에 따른 모델의 예측값과 실제값의 차이가 예측값의 세분화 개수가 3일 때 큰 폭으로 감소한다는 사실도 도출해 낼 수 있었다.

## 저자
한국디지털미디어고등학교 IT LAB **XOR**에 소속되어 있는 한국디지털미디어고등학교 20기 웹프로그래밍과 [여태건우](https://github.com/ytgw0), [유도희](http://dohui-portfolio.kro.kr), 남정원 학생이 작성하였습니다.  
성균관대학교 글로벌융합학부 오하영 교수님께서 지도교수로 참여해주셨습니다.

## 출판된 논문에서 정확하지 않은 부분
논문 출판과정에서 편집이 잘못되어, 현재 출판된 논문에서 정확하지 않은 곳이 몇 군데 있습니다.
먼저 현재 논문에서 식(3)은 아래 왼쪽과 같이 표시되어 있는데, 이는 정확하지 않은 식이며 오른쪽 식이 정확한 식입니다.
<div align="center"><img style="width:70%;" alt="수식" src="https://user-images.githubusercontent.com/30923566/167133372-339aa397-817e-4a3c-955d-ea253a24b96e.png"></div>

다음으로 본문 상에서는 언급되어 있는 그림(8)이 논문안에는 포함되어있지 않은데, 그림(8)은 아래 사진이며 빠진 그림의 설명부분은 다음과 같습니다.


<div align="center"><img style="width:70%;" alt="**Fig. 8** Accuracy graph of output value format diversification experiment" src="https://user-images.githubusercontent.com/30923566/167132214-6e7bb89b-4769-4f26-b0fd-71340a9c8ce2.png"><p>Fig. 8 Accuracy graph of output value format diversification experiment</div>

위 그래프 그림 8를 해석하면 Output의 값이 점점 세분화 됨에 따라 전체적으로 정확도가 상승하는 것을 알 수 있었다.



## 코드 관련 영상
이미지 클릭 시 유튜브 동영상으로 연결됩니다.  
<div align="center">
<a href="https://www.youtube.com/watch?v=fBZ8UDx8VZY"><img src="https://img.youtube.com/vi/fBZ8UDx8VZY/maxresdefault.jpg" style="width:75%;"></a>  
<br><br>  
<a href="https://www.youtube.com/watch?v=y8CM_OsbpVg"><img src="https://img.youtube.com/vi/y8CM_OsbpVg/maxresdefault.jpg" style="width:75%;"></a>
</div>
