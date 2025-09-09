# -*- coding: utf-8 -*-

%matplotlib qt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 칼만필터 클래스
class KalmanFilter:
    def __init__(self, process_variance, measurement_variance):
        # 상태 벡터 초기화
        self.x = np.array([[0], [0], [0], [0]])
        # 오차 공분산 초기값 (불확실성)
        self.P = np.eye(4)
        
        # 상태 전이 행렬 (시간 dt에 따라 업데이트되는 부분임)
        self.F = np.array([[1, 0, 1, 0],
                           [0, 1, 0, 1],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        
        # 관측 행렬 (GPS는 x, y만 측정함)
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])
        
        # 프로세스 잡음 공분산 (IMU 신뢰도 부분)
        self.Q = np.eye(4) * process_variance
        
        # 측정 잡음 공분산 (GPS 신뢰도)
        self.R = np.eye(2) * measurement_variance

    #예측하는 함수
    def predict(self, dt, imu_acceleration):
        # 상태 전이 행렬에 dt를 반영
        self.F[0, 2] = dt
        self.F[1, 3] = dt
        
        # 가속도에 따른 위치& 속도 변화량 계산하는 부분
        acceleration = np.array([[0.5 * imu_acceleration[0] * dt**2], 
                             [0.5 * imu_acceleration[1] * dt**2],
                                  [imu_acceleration[0] * dt],
                                  [imu_acceleration[1] * dt]])
        
        #상태예측 (다음 위치와 속도)
        self.x = self.F @ self.x + acceleration
        #공분산 예측
        self.P = self.F @ self.P @ self.F.T + self.Q

    # 업데이트 함수
    def update(self, gps_measurement):
        #측정 오차
        y = gps_measurement - (self.H @ self.x)
        #오차 공부산
        S = self.H @ self.P @ self.H.T + self.R
        
        #칼만 계산
        K = self.P @ self.H.T @ np.linalg.inv(S)
        
        #상태 보정
        self.x = self.x + K @ y
        self.P = (np.eye(4) - K @ self.H) @ self.P

# 데이터 불러오기!
data = pd.read_csv(r'C:\test\IMU_GPS_sensor_data.csv')
time = data['time'].values
gps_x = data['gps_x'].values
gps_y = data['gps_y'].values
absolute_x = data['absolute_x'].values
absolute_y = data['absolute_y'].values
imu_acceleration_x = data['imu_acceleration_x'].values
imu_acceleration_y = data['imu_acceleration_y'].values

# 칼만필터 함수 실행
def run_kalman_filter(process_variance, measurement_variance):
    kf = KalmanFilter(process_variance, measurement_variance)
    estimates_x = []
    estimates_y = []
    # 예측과 업데이트 반복시키는 부분
    for i in range(1, len(time)):
        dt = time[i] - time[i - 1]
        imu_acceleration = [imu_acceleration_x[i], imu_acceleration_y[i]]
        gps_measurement = np.array([[gps_x[i]], [gps_y[i]]])

        kf.predict(dt, imu_acceleration)
        kf.update(gps_measurement)

        estimates_x.append(kf.x[0, 0])
        estimates_y.append(kf.x[1, 0])

    # 시각화 부분
    ax.clear()
    ax.scatter(gps_x, gps_y,  label='GPS measured',s=1.5, color='green')
    ax.scatter(absolute_x, absolute_y,label='absolute_path(GT)',s=1,color='r' )
    ax.scatter(estimates_x, estimates_y, label='Kalman Filter predicted(GPS+IMU)',s=1, color='b')
    ax.set_title('GPS-IMU data fusion Path Estimate')
    ax.set_xlabel('x [m]')
    ax.set_ylabel('y [m]')
    ax.legend()
    ax.grid()
    plt.draw()

# 초기 파라미터
initial_process_variance = 1e-3
initial_measurement_variance = 1.0


fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.25)

run_kalman_filter(initial_process_variance, initial_measurement_variance)

# 슬라이더 구현 부분
ax_process_variance = plt.axes([0.2, 0.1, 0.65, 0.03])
ax_measurement_variance = plt.axes([0.2, 0.15, 0.65, 0.03])
slider_process_variance = Slider(ax_process_variance, 'Process Variance', 1e-5, 1e-1, valinit=initial_process_variance, valstep=1e-5)
slider_measurement_variance = Slider(ax_measurement_variance, 'Measurement Variance', 0.1, 5.0, valinit=initial_measurement_variance, valstep=0.1)

# 슬라이더 상태 업데이트
def update(val):
    process_variance = slider_process_variance.val
    measurement_variance = slider_measurement_variance.val
    run_kalman_filter(process_variance, measurement_variance)

slider_process_variance.on_changed(update)
slider_measurement_variance.on_changed(update)

plt.show()
