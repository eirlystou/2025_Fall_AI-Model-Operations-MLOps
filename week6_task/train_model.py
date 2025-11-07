# train_model.py
from sklearn.datasets import load_iris               #  Iris(붓꽃) 데이터셋 불러오기
from sklearn.model_selection import train_test_split #  학습용/테스트용 데이터 분리
from sklearn.pipeline import Pipeline                #  여러 단계를 하나의 파이프라인으로 묶기
from sklearn.preprocessing import StandardScaler     #  데이터 표준화(정규화) 도구
from sklearn.linear_model import LogisticRegression  #  로지스틱 회귀 모델 (분류용)
import pickle                                        #  학습된 모델을 파일로 저장하기 위한 모듈

# 모델 학습 및 저장 함수 정의
def train_and_save(model_path="iris_model.pkl"):
    # Iris 데이터셋 불러오기 (X: 특징값, y: 클래스 레이블)
    X, y = load_iris(return_X_y=True)

    # 전처리 + 모델을 하나의 파이프라인으로 구성
    pipe = Pipeline([
        ("scaler", StandardScaler()),                #  입력 데이터를 표준화, trung bình 0, độ lệch chuẩn 1
        ("clf", LogisticRegression(max_iter=1000))   #  로지스틱 회귀 모델 (최대 반복 1000번)-lặp tối đa 1000 lần để học
    ])

    # 데이터 분할 (학습 80%, 테스트 20%)
    # stratify=y → 각 클래스가 비슷한 비율로 나누어지도록 설정
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 모델 학습 수행
    pipe.fit(X_tr, y_tr)

    # 테스트 데이터로 정확도(accuracy) 평가
    acc = pipe.score(X_te, y_te)

    # 학습된 파이프라인(스케일러 + 모델) 저장
    with open(model_path, "wb") as f:
        pickle.dump(pipe, f)                        # 모델 객체를 .pkl 파일로 직렬화하여 저장, wb-ghi ở chế độ nhị phân binary

    # 학습 결과 출력
    print(f"Saved model to {model_path}. Test accuracy={acc:.3f}")

# 직접 실행할 때만 함수 호출 (import 시에는 실행되지 않음)
if __name__ == "__main__":
    train_and_save()
