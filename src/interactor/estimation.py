from dataclasses import dataclass

import numpy as np
import pandas as pd
from ahrs.filters import Madgwick
from scipy.signal import butter, filtfilt
from scipy.spatial.transform import Rotation as R

import model
import repository
import usecase


#クォータニオン
@dataclass
class QuaternionEstimator:
    def EstimationQuaternion(self, input: usecase.EstimationQuaternionInput) -> usecase.EstimationQuaternionOutput:
            """
            センサデータから\n
            クォータニオンを算出
            """
            accData=input.data.acc
            gyroData=input.data.gyro
            # サンプリングレートの計算
            timeDiffs = np.diff(gyroData["time"]) / 1000.0  # タイムスタンプの差を秒単位に変換
            meanDt = np.mean(timeDiffs)
            samplingRate = 1.0 / meanDt
            # Madgwickフィルタの初期化
            q = [1.0, 0.0, 0.0, 0.0]  # 初期の四元数
            madgwick = Madgwick(frequency=samplingRate,gain_imu=0.33)
            # クォータニオンのリストを初期化
            quaternions:list[model.Quaternion] = []
            for i in range(len(gyroData)):
                gyr = [gyroData['x'][i], gyroData['y'][i], gyroData['z'][i]]
                acc = [accData['x'][i], accData['y'][i], accData['z'][i]]
                # フィルタの更新
                filter=madgwick.updateIMU(q=q,gyr=gyr, acc=acc)
                quaternion=model.Quaternion(time=gyroData['time'][i],w=float(filter[0]),x=float(filter[1]),y=float(filter[2]),z=float(filter[3]))
                quaternions.append(quaternion)
            return usecase.EstimationQuaternionOutput(quaternions=quaternions)


def NewQuaternionEstimator()-> QuaternionEstimator:
    return QuaternionEstimator()

def assert_protocol(impl: usecase.QuaternionEstimator):
    pass

assert_protocol(QuaternionEstimator())  # 型チェックを通過すれば OK

#移動距離
@dataclass
class DistanceEstimator:
    def EstimationDistance(self,input: usecase.EstimationDistanceInput)->usecase.EstimationDistanceOutput:
            """
            センサデータから\n
            移動距離を算出
            """
            def butter_lowpass_filter(data, cutoff, fs, order=5):
                nyquist = 0.5 * fs
                normal_cutoff = cutoff / nyquist
                b, a = butter(order, normal_cutoff, btype='low', analog=False)
                y = filtfilt(b, a, data)
                return y

            def butter_highpass_filter(data, cutoff, fs, order=5):
                nyquist = 0.5 * fs
                normal_cutoff = cutoff / nyquist
                b, a = butter(order, normal_cutoff, btype='high', analog=False)
                y = filtfilt(b, a, data)
                return y
            accData=input.data.acc
            quaternions=input.quaternions
            #重力加速度
            g=9.81
            linearAccData = pd.DataFrame(columns=["time", "x", "y", "z"])
            for i in range(len(quaternions)):
                rawAcc = np.array([accData['x'][i], accData['y'][i], accData['z'][i]])
                # フィルタの更新
                quaternion=quaternions[i]
                gravity = np.array([
                    2 * (quaternion.x * quaternion.z - quaternion.w * quaternion.y),
                    2 * (quaternion.w * quaternion.x + quaternion.y * quaternion.z),
                    quaternion.w**2 - quaternion.x**2 - quaternion.y**2 + quaternion.z**2
                ])
                # 重力ベクトルの大きさを考慮
                gravity *= g
                linearAcc=rawAcc-gravity

                # クォータニオンを回転行列に変換
                rotationMatrix = R.from_quat([
                        quaternion.w,
                        quaternion.x,
                        quaternion.y,
                        quaternion.z
                ]).as_matrix()

                # 地球座標系での加速度
                earthAcc = rotationMatrix @ linearAcc
                # 新しい行を作成
                new_row = pd.DataFrame({"time": [quaternion.time], "x": [earthAcc[0]], "y": [earthAcc[1]], "z": [earthAcc[2]]})
                linearAccData = pd.concat([linearAccData, new_row], ignore_index=True)

                # # 閾値の設定(ここを入れると加速度が閾値以下のところからの積分を行う,
                #   精度が上がるがおそらくキャリブレーションができたら不要)
                # threshold = 0.1  # 必要に応じて調整
                # # 各軸で閾値以下となる最初のインデックスを取得
                # condition = (
                #     (linearAccData["x"].abs() <= threshold) &
                #     (linearAccData["y"].abs() <= threshold) &
                #     (linearAccData["z"].abs() <= threshold)
                # )
                # # 条件を満たす最初のインデックスを取得
                # start_index = linearAccData[condition].index.min()
                # linearAccData = linearAccData.loc[start_index:].reset_index(drop=True)
                # 
                time = (linearAccData["time"] - linearAccData["time"][0]) / 1000

            def butter_lowpass_filter(data, cutoff, fs, order=5):
                nyquist = 0.5 * fs
                normal_cutoff = cutoff / nyquist
                b, a = butter(order, normal_cutoff, btype='low', analog=False)
                y = filtfilt(b, a, data)
                return y

            # サンプリングレートとカットオフ周波数の設定
            fs = 1 / (time[1] - time[0])
            cutoff = 1.0  # 低周波成分を残すためのカットオフ周波数

            # # フィルタリング
            linearAccData["x"] = butter_lowpass_filter(linearAccData["x"], cutoff, fs)
            linearAccData["y"] = butter_lowpass_filter(linearAccData["y"], cutoff, fs)
            linearAccData["z"] = butter_lowpass_filter(linearAccData["z"], cutoff, fs)
            # 速度データの初期化
            speedData = pd.DataFrame(columns=["time", "vx", "vy", "vz"])

            # 速度を計算するためのループ
            vx = 0
            vy = 0
            vz = 0
            for i in range(len(linearAccData)):
                if i == 0:
                    dt = 0
                else:
                    dt = (linearAccData["time"][i] - linearAccData["time"][i - 1])/1000

                # 台形積分を使用して速度を更新
                if i > 0:
                    avg_acc_x = (linearAccData["x"][i] + linearAccData["x"][i - 1]) / 2
                    avg_acc_y = (linearAccData["y"][i] + linearAccData["y"][i - 1]) / 2
                    avg_acc_z = (linearAccData["z"][i] + linearAccData["z"][i - 1]) / 2
                    
                    vx += avg_acc_x * dt
                    vy += avg_acc_y * dt
                    vz += avg_acc_z * dt

                # 新しい行を作成
                new_row = pd.DataFrame({"time": [linearAccData["time"][i]], "vx": [vx], "vy": [vy], "vz": [vz]})
                speedData = pd.concat([speedData, new_row], ignore_index=True)
                
            # カットオフ周波数の設定（ここでは0.1 Hzを例にしていますが、必要に応じて変更してください）
            cutoff_high = 0.1

            # 速度データのフィルタリング
            speedData["vx"] = butter_highpass_filter(speedData["vx"], cutoff_high, fs)
            speedData["vy"] = butter_highpass_filter(speedData["vy"], cutoff_high, fs)
            speedData["vz"] = butter_highpass_filter(speedData["vz"], cutoff_high, fs)

            speedData["vx"] = butter_lowpass_filter(speedData["vx"], cutoff, fs)
            speedData["vy"] = butter_lowpass_filter(speedData["vy"], cutoff, fs)
            speedData["vz"] = butter_lowpass_filter(speedData["vz"], cutoff, fs)

            # 距離を計算するためのループ
            distanceData = pd.DataFrame(columns=["time", "dx", "dy", "dz"])
            dx = 0
            dy = 0
            dz = 0
            for i in range(len(speedData)):
                if i == 0:
                    dt = 0
                else:
                    dt = (speedData["time"][i] - speedData["time"][i - 1])/1000
                
                dx += speedData["vx"][i] * dt
                dy += speedData["vy"][i] * dt
                dz += speedData["vz"][i] * dt

                # 新しい行を作成
                new_row = pd.DataFrame({"time": [speedData["time"][i]], "dx": [dx], "dy": [dy], "dz": [dz]})
                distanceData = pd.concat([distanceData, new_row], ignore_index=True)

            def butter_highpass_filter(data, cutoff, fs, order=5):
                nyquist = 0.5 * fs
                normal_cutoff = cutoff / nyquist
                b, a = butter(order, normal_cutoff, btype='high', analog=False)
                y = filtfilt(b, a, data)
                return y

            # カットオフ周波数の設定（ここでは0.1 Hzを例にしていますが、必要に応じて変更してください）
            cutoff_high = 0.1

            # 距離データのフィルタリング
            distanceData["dx"] = butter_highpass_filter(distanceData["dx"], cutoff_high, fs)
            distanceData["dy"] = butter_highpass_filter(distanceData["dy"], cutoff_high, fs)
            distanceData["dz"] = butter_highpass_filter(distanceData["dz"], cutoff_high, fs)

            distanceData["dx"] = butter_lowpass_filter(distanceData["dx"], cutoff, fs)
            distanceData["dy"] = butter_lowpass_filter(distanceData["dy"], cutoff, fs)
            distanceData["dz"] = butter_lowpass_filter(distanceData["dz"], cutoff, fs)

            #距離データのリストを初期化
            distances:list[model.Distance] = []
            for i in range(len(distanceData)):
                distance=model.Distance(
                    time=distanceData["time"][i],
                    x=distanceData["dx"][i],
                    y=distanceData["dy"][i],
                    z=distanceData["dz"][i]
                )
                distances.append(distance)
            return usecase.EstimationDistanceOutput(distances=distances)

def NewDistanceEstimator()-> DistanceEstimator:
    return DistanceEstimator()


