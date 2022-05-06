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

## 코드 관련 영상
이미지 클릭 시 유튜브 동영상으로 연결됩니다.  
<div align="center">
<a href="https://www.youtube.com/watch?v=fBZ8UDx8VZY"><img src="https://img.youtube.com/vi/fBZ8UDx8VZY/maxresdefault.jpg" style="width:75%;"></a>  
<br><br>  
<a href="https://www.youtube.com/watch?v=y8CM_OsbpVg"><img src="https://img.youtube.com/vi/y8CM_OsbpVg/maxresdefault.jpg" style="width:75%;"></a>
</div>
