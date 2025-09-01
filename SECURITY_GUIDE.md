# 🔒 개인정보 보호 가이드

## ⚠️ 중요: GitHub 공개 저장소 사용 시 주의사항

이 프로젝트는 GitHub에 공개되어 있으므로, **개인정보가 노출되지 않도록** 다음 사항을 반드시 준수해주세요:

## ❌ GitHub에 절대 올리면 안 되는 파일들

### 🔑 개인 설정 파일
- `config.json` (실제 이메일/비밀번호 포함)
- `user_config.json` (개인 설정)
- `settings.ini` (사용자 설정)
- `.env` (환경 변수)

### 📁 개인 데이터
- `Pictures/참석자/` (캡처된 스크린샷)
- `data/` 폴더 (개인 데이터)
- `backups/` 폴더 (백업 데이터)
- `*.log` (모든 로그 파일)

### 🔐 인증 정보
- `secrets.json` (비밀 정보)
- `credentials.json` (인증 정보)
- `kakao_tokens.json` (카카오톡 토큰)

## ✅ 안전한 사용 방법

### 1. 환경 변수 사용 (권장)
```bash
# Windows
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-app-password
set RECIPIENT_EMAIL=recipient@example.com

# Linux/Mac  
export SMTP_USERNAME=your-email@gmail.com
export SMTP_PASSWORD=your-app-password
```

### 2. 로컬 설정 파일 생성
1. `config_template.json`을 `config.json`으로 복사
2. 실제 값으로 변경 (`.gitignore`에 의해 자동 제외됨)

### 3. 보안 설정 관리자 사용
```python
from secure_config_manager import SecureConfigManager
config = SecureConfigManager()
config.set_smtp_config("smtp.gmail.com", 587, "email", "password", ["recipient"])
```

## 🚨 긴급 대처 방법

### 이미 개인정보가 GitHub에 올라간 경우:
1. **즉시 비밀번호 변경**
2. **Git에서 파일 제거**:
   ```bash
   git rm config.json
   git commit -m "Remove sensitive config"
   ```
3. **Git 히스토리에서 완전 제거**:
   ```bash
   git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch config.json' HEAD
   ```

## 📞 도움이 필요한 경우
- 보안 문제 발생 시 즉시 개인정보 변경
- 기술적 문제는 Issues에 문의 (개인정보 제외)
