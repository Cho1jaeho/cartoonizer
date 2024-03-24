import cv2
import numpy as np

def cartoonize_frame(frame):
    # 에지 감지를 위한 그레이스케일 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 에지 검출
    edges = cv2.medianBlur(gray, 7)
    edges = cv2.adaptiveThreshold(edges, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    # 카툰화된 프레임 생성
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon = cv2.bitwise_and(color, color, mask=edges)
    
    return cartoon

# 비디오 파일 경로 설정
video_path = 'data/vtest.avi'

# 비디오 불러오기
cap = cv2.VideoCapture(video_path)

# 비디오 정보 가져오기
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# 카툰화된 비디오 저장 설정
output_path = 'data/cartoonized_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# 영상 프레임별로 처리 및 저장
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # 현재 프레임을 카툰화
    cartoon_frame = cartoonize_frame(frame)
    
    # 카툰화된 프레임 저장
    out.write(cartoon_frame)
    
    # 카툰화된 프레임 화면에 출력
    cv2.imshow('Cartoonized Video', cartoon_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 작업 완료 후 해제
cap.release()
out.release()
cv2.destroyAllWindows()