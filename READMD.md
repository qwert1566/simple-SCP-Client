# Simple Scp Server

- Termux로 열려있는 SSH 서버로 접속하여 휴대폰에 있는 파일을 빠르게 옮기는 용도로 사용하고 있습니다.
- 파일 보기/다운로드 외 다른 기능은 존재하지 않습니다.
- 파일 안에 있는 `NetworkAdpater`, `passwd`, `oriDirectory`, `downloadDirectory`를 수정하여 기본값을 바꿀 수 있습니다.
- Get IP for Network Adpther는 위에 적혀있는 어댑터의 IP를 가져옵니다.
- 어댑터 이름의 기준은 `ipconfig`입니다.
- 휴대폰과 컴퓨터를 선으로 연결 후 휴대폰 USB 모드를 USB 테더링으로 바꾸면 됩니다.
- 어댑터 이름을 모르거나 IP를 모르면 터미널에서 `ipconfig`를 입력하여 확인하세요.
