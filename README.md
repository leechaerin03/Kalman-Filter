# 📡 Kalman Filter Sensor Fusion Simulation
> **로봇 데이터 융합/보정 알고리즘 개발(Kalman)**

<br>

## 📅 Project Overview
**"불확실한 센서 데이터 속에서, 최적의 위치를 찾아내다."**
자율주행 및 로보틱스 분야의 핵심인 **Sensor Fusion** 기술을 이해하고 구현하기 위해
Python기반, Kalman Filter를 활용한 IMU와 GPS 데이터 퓨전 및 보정 알고리즘 개발 프로젝트입니다.
특히 **Matplotlib의 Slider 기능**을 활용해 공분산(Covariance) 파라미터를 실시간으로 튜닝하며 성능 변화를 시각적으로 분석할 수 있는 환경을 구축했습니다.

<br>

## 🛠 Tech Stack

<div align="left">
  <h3>Environment</h3>
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Spyder-FF0000?style=flat&logo=spyder&logoColor=white"/>
  <br>
  <h3>Libraries</h3>
  <img src="https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white"/>
  <img src="https://img.shields.io/badge/Matplotlib-ffffff?style=flat&logo=matplotlib&logoColor=black"/>
  <br>
  <h3>Core Algorithm</h3>
  <img src="https://img.shields.io/badge/Kalman%20Filter-Linear%20Algebra-FF4785?style=flat"/>
  <img src="https://img.shields.io/badge/Sensor%20Fusion-GPS%20%2B%20IMU-FF4785?style=flat"/>
</div>

<br>
## 📐 Mathematical Model (Core Logic)
이 프로젝트는 선형 동적 시스템(Linear Dynamic System)을 전제로 한 칼만 필터를 적용했습니다.

### 1. State Vector (상태 벡터)
위치($p$)와 속도($v$)를 추정하기 위해 2차원 상태 벡터를 정의했습니다.

<div align="center">
  <img src="https://latex.codecogs.com/svg.latex?x%20=%20\begin{bmatrix}%20p%20\\%20v%20\end{bmatrix}" title="State Vector" />
</div>

### 2. State Prediction (상태 예측)
이전 상태와 IMU의 가속도 입력을 이용해 현재 상태를 예측하는 단계입니다. 구체적인 수식과 행렬 정의는 다음과 같습니다.

<div align="center">
  <img src="image01.png" title="State Prediction Formula and Matrices" width="800" />
</div>

### 3. Covariance Prediction (오차 공분산 예측)
센서의 불확실성을 예측하는 단계입니다. 시스템 노이즈를 반영하여 예측값의 신뢰도를 계산합니다. 구체적인 수식과 행렬 정의는 다음과 같습니다.

<div align="center">
  <img src="image02.png" title="Covariance Prediction Formula and Matrices" width="800" />
</div>

<br>

## 💡 Key Features

* **Real-time Visualization:** Python `matplotlib`를 활용하여 Raw GPS 데이터(점)와 칼만 필터 추정 경로(선)를 실시간으로 비교 시각화합니다.
* **Interactive Parameter Tuning:** `Slider` 위젯을 통해 측정 노이즈(Measurement Noise, R)와 프로세스 노이즈(Process Noise, Q) 값을 즉시 변경하며 필터의 민감도를 테스트할 수 있습니다.
* **Sensor Fusion Logic:**
    * **GPS:** 위치 정보를 제공하지만 노이즈가 심함 (Update 단계에서 보정)
    * **IMU:** 가속도를 적분하여 부드러운 움직임을 제공하지만 오차가 누적됨 (Prediction 단계에서 사용)
    * **Fusion:** 두 센서의 장점을 결합하여 정확도(GPS)와 연속성(IMU)을 동시에 확보

<br>

## 📸 Simulation Result
[![Kalman Filter Simulation](https://img.youtube.com/vi/XbY7f02Xpt8/hqdefault.jpg)](https://youtu.be/XbY7f02Xpt8)
> **Result:** 붉은 점(GPS 노이즈)이 튀는 상황에서도, 파란 선(Kalman Filter)은 물리 법칙에 기반하여 부드럽고 정확한 경로를 유지함을 확인했습니다.

<br>

## 🚀 Retrospective & Future Work

### 🎓 From Theory to Practice
학부 시절 **선형대수학**에서 배웠던 행렬 연산과 **다변량 통계**의 개념들이 실제 엔지니어링 문제(위치 추적)를 해결하는 데 어떻게 쓰이는지 몸소 체감할 수 있었습니다. 수식으로만 존재하던 $A x + B u$가 코드로 구현되어 실시간으로 움직이는 것을 보며 수학적 모델링의 강력함을 느꼈습니다.

### 🔭 Future Scope
1.  **Non-linear System:** 현재의 선형 모델을 넘어, 비선형 움직임을 추적할 수 있는 EKF(Extended Kalman Filter)나 Particle Filter를 구현하여 곡선 구간에서의 성능을 비교해보고 싶습니다.
2.  **AI-based Estimation:** IMU 센서 데이터는 시계열(Time-series) 특성을 가집니다. 이를 **RNN(LSTM/GRU)** 모델에 학습시켜, 센서 오차를 딥러닝으로 보정하는 AI 퓨전 모델로 발전시켜 볼 계획입니다.

---
