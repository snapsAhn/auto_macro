import React, { useState } from 'react';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { DatePicker, TimePicker } from '@mui/x-date-pickers';
import { TextField, Button, Box } from '@mui/material';
import { ko } from 'date-fns/locale';

function App() {
  const [date, setDate] = useState(null);
  const [time, setTime] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    // 날짜와 시간 포맷 변환 예시
    const dateStr = date ? date.toISOString().slice(0, 10) : '';
    const timeStr = time ? time.toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit' }) : '';
    alert(`예매 날짜: ${dateStr}\n예매 시간: ${timeStr}`);
    // 실제로는 Flask API로 POST 요청
  };

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={ko}>
      <Box sx={{ maxWidth: 400, mx: 'auto', mt: 5, p: 3, border: '1px solid #eee', borderRadius: 2 }}>
        <h1>예매 매크로</h1>
        <form onSubmit={handleSubmit}>
          <DatePicker
            label="예매 날짜"
            value={date}
            onChange={setDate}
            renderInput={(params) => <TextField {...params} fullWidth margin="normal" required />}
          />
          <TimePicker
            label="예매 시간"
            value={time}
            onChange={setTime}
            renderInput={(params) => <TextField {...params} fullWidth margin="normal" required />}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth sx={{ mt: 2 }}>
            매크로 시작
          </Button>
        </form>
      </Box>
    </LocalizationProvider>
  );
}

export default App;
