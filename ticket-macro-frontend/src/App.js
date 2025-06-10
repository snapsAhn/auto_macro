import React, { useState, useEffect, useRef } from 'react';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DatePicker, TimePicker } from '@mui/x-date-pickers';
import { TextField, Button, Box } from '@mui/material';
import { ko } from 'date-fns/locale';

function App() {
  const [openDate, setOpenDate] = useState(null); // 예매 오픈 날짜
  const [openTime, setOpenTime] = useState(null); // 예매 오픈 시간
  const [gameDateText, setGameDateText] = useState(''); // 경기 날짜(예: "06.15")
  const [step, setStep] = useState(0); // 0: 입력, 1: 브라우저 오픈, 2: 대기, 3: 예매 시도 등
  const [message, setMessage] = useState('');
  const [remainSeconds, setRemainSeconds] = useState(null);
  const timerRef = useRef(null);

  // step이 2(대기)로 바뀌면 타이머 시작
  useEffect(() => {
    if (step === 2 && openDate && openTime) {
      const target = new Date(
        openDate.getFullYear(),
        openDate.getMonth(),
        openDate.getDate(),
        openTime.getHours(),
        openTime.getMinutes(),
        0
      );
      const updateRemain = () => {
        const now = new Date();
        const diff = Math.floor((target - now) / 1000);
        setRemainSeconds(diff > 0 ? diff : 0);
        if (diff <= 0 && timerRef.current) {
          clearInterval(timerRef.current);
        }
      };
      updateRemain();
      timerRef.current = setInterval(updateRemain, 1000);
      return () => clearInterval(timerRef.current);
    } else {
      setRemainSeconds(null);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  }, [step, openDate, openTime]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStep(1); // 브라우저 오픈 안내를 즉시 띄움
    const pad = (n) => n.toString().padStart(2, '0');
    const openDateStr = openDate
      ? `${openDate.getFullYear()}-${pad(openDate.getMonth() + 1)}-${pad(openDate.getDate())}`
      : '';
    const openTimeStr = openTime
      ? `${pad(openTime.getHours())}:${pad(openTime.getMinutes())}`
      : '';
    const payload = {
      openDate: openDateStr,
      openTime: openTimeStr,
      gameDateText: gameDateText
    };
    // Flask API 호출
    try {
      const response = await fetch('http://localhost:5000/api/reserve', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const result = await response.json();
      if (!result.success) {
        alert(result.message); // 예매 오픈 날짜가 지났을 때 경고창
        setStep(0); // 입력 폼으로 복귀
        return;
      }
      setStep(1);
    } catch (err) {
      alert("서버 오류: " + err.message);
      setStep(0); // 입력 폼으로 복귀
    }
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
      <Box sx={{ maxWidth: 400, mx: 'auto', mt: 5, p: 3, border: '1px solid #eee', borderRadius: 2 }}>
        <h1>예매 매크로</h1>
        {step === 0 && (
          <form onSubmit={handleSubmit}>
            <DatePicker
              label="예매 오픈 날짜"
              value={openDate}
              onChange={setOpenDate}
              renderInput={(params) => <TextField {...params} fullWidth margin="normal" required />}
            />
            <TimePicker
              label="예매 오픈 시간"
              value={openTime}
              onChange={setOpenTime}
              renderInput={(params) => <TextField {...params} fullWidth margin="normal" required />}
            />
            <TextField
              label="경기 날짜 (예: 06.15)"
              value={gameDateText}
              onChange={e => setGameDateText(e.target.value)}
              fullWidth
              margin="normal"
              required
            />
            <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
              매크로 시작
            </Button>
          </form>
        )}
        {step === 1 && (
          <div>
            <p>브라우저가 열렸습니다.<br />
              1. <b>수동으로 로그인</b> 해주세요.<br />
              2. 모든 준비가 완료되면 아래 버튼을 눌러주세요.
            </p>
            <Button onClick={() => setStep(2)}>다음 단계로</Button>
            <Button onClick={() => setStep(0)} color="secondary" sx={{ mt: 1 }}>날짜 입력력으로 돌아가기</Button>
          </div>
        )}
        {step === 2 && (
          <div>
            <p>
              예매 오픈 시간까지 대기 중입니다...<br />
              {remainSeconds !== null && remainSeconds > 0 && (
                <span>⏳ 남은 시간: {remainSeconds}초</span>
              )}
              {remainSeconds === 0 && (
                <span>예매 오픈 시간이 되었습니다!</span>
              )}
            </p>
            <Button onClick={() => setStep(0)} color="secondary" sx={{ mt: 1 }}>날짜 입력으로 돌아가기</Button>
          </div>
        )}
      </Box>
    </LocalizationProvider>
  );
}

export default App;
