from machine import Timer, PWM
import time
from Maix import I2S, GPIO
from fpioa_manager import fm

# タイマーとPWMの設定
tim0 = Timer(Timer.TIMER0, Timer.CHANNEL0, mode=Timer.MODE_PWM)
tim1 = Timer(Timer.TIMER1, Timer.CHANNEL1, mode=Timer.MODE_PWM)
ch0 = PWM(tim0, freq=50, duty=5, pin=34)
ch1 = PWM(tim1, freq=50, duty=10, pin=35)

# === 音声認識部分の追加開始 ===
from Maix import KPU
import audio

KPU.load("/sd/model.kmodel")  # 事前に訓練したモデルのパス
record = audio.record(6)  # 音声データを6秒間録音

def detect_voice_command():
    # 音声データの録音
    record.start()
    time.sleep(6)
    record.stop()
   
    # 音声データの分析
    result = KPU.forward(task, record.getdata())
   
    # ここでは「右に曲がって」と「左に曲がって」をそれぞれ0, 1として識別すると仮定
    if result[0] > 0.5:
        return "右に曲がって"
    elif result[1] > 0.5:
        return "左に曲がって"
    else:
        return None
# === 音声認識部分の追加終了 ===

while True:
    command = detect_voice_command()
   
    if command == "右に曲がって":
        ch0.duty(10)  # 左のモーターを前進させる
        ch1.duty(5)   # 右のモーターを後退させる
        time.sleep(1)
    elif command == "左に曲がって":
        ch0.duty(5)   # 左のモーターを後退させる
        ch1.duty(10)  # 右のモーターを前進させる
        time.sleep(1)
   
    # モーターをストップする
    ch0.duty(7.5)
    ch1.duty(7.5)
