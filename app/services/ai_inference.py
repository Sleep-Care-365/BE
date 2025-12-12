import numpy as np
import random

# 실제로는 tensorflow 로드
# import tensorflow as tf
# import mne

class SleepModelService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        """
        서버 시작 시 모델(.h5)을 메모리에 로드합니다.
        """
        print("🧠 AI 모델 로딩 중...")
        try:
            # self.model = tf.keras.models.load_model("model_files/cnn_lstm_v1.h5")
            print("✅ AI 모델 로드 완료!")
        except Exception as e:
            print(f"❌ 모델 로드 실패: {e}")
            # 테스트를 위해 실패해도 넘어감

    def preprocess(self, file_path: str):
        """
        업로드된 EDF 파일을 읽어서 모델 입력 형태(Numpy)로 변환합니다.
        (PDF의 MNE 전처리 로직이 들어갈 곳)
        """
        print(f"📂 파일 전처리 시작: {file_path}")
        
        # --- [가짜 전처리 로직] ---
        # 실제로는 MNE로 파일 읽고 Epoching 해야 함
        # epochs = ...
        # return epochs.get_data()
        
        # 임시: 30초 단위로 8시간(960개) 정도 잤다고 가정
        dummy_epochs = 960 
        return dummy_epochs

    def predict(self, file_path: str):
        """
        파일 경로를 받아서 수면 단계를 예측하고 결과를 반환합니다.
        """
        # 1. 전처리
        total_epochs = self.preprocess(file_path)

        # 2. 모델 예측 (Inference)
        print("🔮 수면 단계 예측 중...")
        
        # --- [가짜 예측 로직] ---
        # 실제로는: predictions = self.model.predict(input_data)
        #           stages = np.argmax(predictions, axis=1)
        
        # 임시: 랜덤으로 수면 단계 생성 (0:W, 1:N1, 2:N2, 3:N3, 4:N4, 5:R)
        # N2(2)가 가장 많게 확률 조작
        stages = np.random.choice(
            [0, 1, 2, 3, 4, 5], 
            size=total_epochs, 
            p=[0.1, 0.1, 0.4, 0.1, 0.1, 0.2]
        )
        
        return stages.tolist()

# 전역 객체 생성 (싱글톤처럼 사용)
ai_service = SleepModelService()