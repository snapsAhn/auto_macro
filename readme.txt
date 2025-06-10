터미널 창 >
python app.py

또 다른 터미널 창 > 
cd ticket-macro-frontend
npm start


GitHub Copilot
아래는 React(프론트엔드) 설치 및 버전 맞추기 방법을 정리한 최신 가이드입니다.

0. 새 프로젝트 생성
npm create ticket-macro-frontend@latest
1. 터미널에서 프로젝트 폴더로 이동
cd ticket-macro-frontend
2. 기존 node_modules와 lock 파일 삭제 (버전 충돌 방지)
rm -rf node_modules
del package-lock.json
npm cache clean --force
(Windows에서는 rd /s /q node_modules 명령도 사용 가능)

3. React 18.2.0 버전으로 설치
npm install react@18.2.0 react-dom@18.2.0 --save

4. 기타 의존성 설치
npm install

5. React 개발 서버 실행
npm start

6. 버전 확인
npm ls react

출력 결과에 react@18.2.0만 보이면 정상입니다.
정리
반드시 react@18.2.0, react-dom@18.2.0 버전만 사용해야 합니다.
package.json의 react, react-dom 버전도 "18.2.0"으로 맞춰주세요.
위 과정을 모두 거치면 버전 충돌 없이 React 개발 환경을 사용할 수 있습니다.