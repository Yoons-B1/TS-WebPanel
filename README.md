[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://github.com/Yoons-B1/TS-WebPanel/releases) [![Release](https://img.shields.io/badge/Release-V1.8-fc1ba6)](https://github.com/Yoons-B1/TS-WebPanel/releases) ![License](https://img.shields.io/github/license/Yoons-B1/TS-WebPanel)
# TS-WebPanel (Fullscreen Signage Browser for Windows)

---

### 1. Secure Internal Access Browser (No Warning)
- Standard browsers like Chrome or Edge can access internal web servers  
  but Windows shows security warnings when using internal IP addresses  
- This happens because the connection uses HTTP instead of HTTPS  
- This app is a fullscreen browser designed to avoid security warnings in local networks  
- In windowed mode, the browser stays at the position defined in the settings  

---

### 2. Signage Mode
- Runs without address bar or browser UI  
- Custom window size and position  
- Supports fullscreen and rotation (90° / -90°)  
- Ideal for displaying HTML content in fullscreen signage environments  

---

### 3. First Run & Settings
- A settings window appears on first launch  
- Press **F2** anytime to open settings  
- Supports Korean / English toggle  

Configurable options:
- App title  
- URL  
- Window size & position  
- Zoom level  
- Fullscreen mode  
- Rotation  

Settings file:
```
internal_web_panel_config.json
```
<img width="472" height="383" alt="cap" src="https://github.com/user-attachments/assets/968a31b7-6923-46ea-974f-77be8d985822" />

---

### 4. Playback Behavior
- If the **URL field is empty**, `standby.mp4` will automatically loop  
- `standby.mp4` file must be located in the **same folder as the executable**  
- Supported codec: **H.264 (video) + AAC (audio)**
- **After changing or clearing the URL, please restart the application to apply the changes properly**  

---

### 5. Controls & Shortcuts
- Open settings: **F2**  
- Manual refresh: **F5**  
- Toggle fullscreen: **F11**  

---

### 6. YouTube / Streaming Notice
- **Live streaming (e.g. YouTube Live) is not officially supported**  
- To enter fullscreen in YouTube:
  - Press **F key** after the app starts  

---

### 7. Exit App
- Press and hold the **top-left corner for 5 seconds** to exit  
- Active area: **80x80 px square**
- Or press **Ctrl + Q** to exit  

---

## 🇰🇷 한국어

### 1. 보안 경고 없는 내부 접속용 브라우저
- 크롬, 엣지 등의 웹브라우저로 내부 웹서버에 접속할 수 있지만  
  Windows에서는 내부 IP 접속 시 보안 경고가 표시됩니다  
- 이는 HTTPS가 아닌 HTTP로 접속하기 때문에 발생하는 문제입니다  
- 본 앱은 전체화면 전용 브라우저로, 내부 네트워크에서도 보안 경고 없이 사용할 수 있습니다  
- 전체화면이 아닌 경우에는 설정에서 저장한 위치에 브라우저가 고정됩니다  

---

### 2. 사이니지 모드
- 주소창 등 상단 UI 없이 실행됩니다  
- 원하는 위치와 크기로 실행 가능  
- 전체화면 및 90° / -90° 회전 지원  
- HTML 콘텐츠를 사이니지용 풀스크린으로 출력 가능  

---

### 3. 첫 실행 및 설정
- 처음 실행 시 설정창이 자동으로 표시됩니다  
- 이후 **F2 키**로 설정창 진입 가능  
- 한국어 / 영어 언어 전환 가능  

설정 가능 항목:
- 앱 제목  
- 접속 주소(URL)  
- 창 크기 및 위치  
- 줌 비율  
- 전체화면 여부  
- 회전 방향  

설정 파일:
```
internal_web_panel_config.json
```

---

### 4. 재생 동작
- **URL이 빈칸일 경우 `standby.mp4` 영상이 자동으로 루프 재생됩니다**  
- `standby.mp4` 파일은 **실행파일과 같은 폴더에 위치해야 합니다**  
- 사용 코덱: **H.264 (영상), AAC (오디오)**
- **URL 주소를 변경하거나 삭제한 경우, 정상 적용을 위해 앱을 재실행 해주세요.**  

---

### 5. 단축키
- 설정 화면 진입: **F2**  
- 수동 새로고침: **F5**  
- 전체화면 전환: **F11**  

---

### 6. 유튜브 / 스트리밍 안내
- **유튜브 등 라이브 스트리밍은 공식적으로 지원하지 않습니다**  
- 유튜브 전체화면 방법:
  - 앱 실행 후 **F 키** 입력  

---

### 7. 종료 방법
- 화면 좌측 상단 모서리를 **5초간 길게 누르면 종료됩니다**  
- 활성 영역: **80x80px**
- 또는 **Ctrl + Q**를 눌러 종료할 수 있습니다 
