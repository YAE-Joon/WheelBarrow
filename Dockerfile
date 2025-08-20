#Python 공식 이미지 사용
FROM python:3.11-slim

#메인테이너 정보
LABEL maintainer='carregt@gmail.com'

#작업 디렉토리 설정
WORKDIR /app

#시스템의존성 설치 (POSTGRESQL 클라이언트 등)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

#파이썬 의존성 설치 \
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

#애플리케이션 코드 복사
COPY . .

#환경변수 설정
ENV PYTHONPATH=/app
ENV ENV_FILE=.env.production

#포트 노출(8000으로 변경)
EXPOSE 8000

# Health check 추가
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

#애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port","8000"]