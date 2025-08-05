import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [formData, setFormData] = useState({
    difficulty: '중',
    player_count: '4명',
    main_objectives: '자원을 모아 왕국 건설\n적 점령지 파괴',
    rules: '턴제 진행\n행동 포인트 사용',
    win_conditions: '모든 건물 완성\n상대 진영 제거',
    fail_conditions: '자원 고갈\n병력 전멸'
  });

  const [feedback, setFeedback] = useState(null);

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async () => {
    try {
      const payload = {
        difficulty: formData.difficulty,
        player_count: formData.player_count,
        main_objectives: formData.main_objectives.split('\n'),
        rules: formData.rules.split('\n'),
        win_conditions: formData.win_conditions.split('\n'),
        fail_conditions: formData.fail_conditions.split('\n'),
      };
      const res = await axios.post('http://localhost:8000/api/feedback/balance', payload);
      setFeedback(res.data.balanceAnalysis);
    } catch (error) {
      console.error('분석 실패:', error);
    }
  };

  return (
    <div className="App">
      <div className="sidebar">
        <span role="img" aria-label="menu">🏠</span> [기획] 워크스페이스
      </div>
      <div className="header">
        <span>에이블러</span>
        <span role="img" aria-label="user">👤</span>
      </div>
      <div className="content">
        <h2>밸런싱 및 난이도 조정</h2>
        <div>
          <label>게임명: <b>할리갈리2</b></label>
        </div>
        <div className="block-row">
          <div className="block">
            <label>난이도</label>
            <input name="difficulty" value={formData.difficulty} onChange={handleChange} />
          </div>
          <div className="block">
            <label>인원</label>
            <input name="player_count" value={formData.player_count} onChange={handleChange} />
          </div>
        </div>
        <div className="block-row">
          <div className="block">
            <label>주요 목표</label><br />
            <textarea name="main_objectives" value={formData.main_objectives} onChange={handleChange} />
          </div>
          <div className="block">
            <label>행동규칙</label><br />
            <textarea name="rules" value={formData.rules} onChange={handleChange} />
          </div>
        </div>
        <div className="block-row">
          <div className="block">
            <label>승리조건</label><br />
            <textarea name="win_conditions" value={formData.win_conditions} onChange={handleChange} />
          </div>
          <div className="block">
            <label>패배, 탈락 조건</label><br />
            <textarea name="fail_conditions" value={formData.fail_conditions} onChange={handleChange} />
          </div>
        </div>
        <div className="buttons">
          <button>임시저장</button>
          <button>이전</button>
          <button onClick={handleSubmit}>다음</button>
        </div>
        {feedback && (
          <div className="feedback">
            <h3>분석 결과</h3>
            <p><b>시뮬레이션 요약:</b> {feedback.simulationSummary}</p>
            <p><b>문제점:</b></p>
            <ul>{feedback.issuesDetected.map((issue, i) => <li key={i}>{issue}</li>)}</ul>
            <p><b>추천사항:</b></p>
            <ul>{feedback.recommendations.map((rec, i) => <li key={i}>{rec}</li>)}</ul>
            <p><b>밸런스 점수:</b> {feedback.balanceScore}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;