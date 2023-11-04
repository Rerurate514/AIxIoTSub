import audio
import KPU as kpu

# マイクからの入力を取得
audio.init(22050, 20000, 512)
audio.record()

while True:
    # 音声データを取得
    audio_data = audio.recorded_data()
    if audio_data:
        # 音声認識エンジンにデータを送信
        result = kpu.run_yolo2(audio_data)
        if result:
            for i in result:
                print(i)