// App.js
import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useNavigate } from 'react-router-dom';
import Basic from './components/Basic';

function Home() {
  const [isHovered, setIsHovered] = useState(false);
  const navigate = useNavigate();

  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <h1 style={styles.title}>Skincare AI</h1>
        <p style={styles.description}>
          Discover your perfect skincare routine with personalized recommendations tailored just for you.
        </p>
        <button
          style={{
            ...styles.button,
            ...(isHovered ? styles.buttonHover : {}),
          }}
          onMouseEnter={() => setIsHovered(true)}
          onMouseLeave={() => setIsHovered(false)}
          onClick={() => navigate('/basic')}
        >
          ★ Get Your Personalized Recommendation ★
        </button>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/basic" element={<Basic />} />
      </Routes>
    </Router>
  );
}

const styles = {
  container: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    background: 'linear-gradient(135deg, #1f1c3c, #3a3d7a)',
    margin: 0,
  },
  card: {
    background: 'rgba(255, 255, 255, 0.9)',
    borderRadius: '16px',
    padding: '40px',
    width: '800px',
    height: '460px',
    textAlign: 'center',
    boxShadow: '0px 6px 25px rgba(0, 0, 0, 0.2)',
  },
  title: {
    fontSize: '70px',
    fontWeight: 'bold',
    background: 'linear-gradient(90deg, #6a5acd, #8a2be2)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    marginBottom: '20px',
    textShadow: '0px 0px 8px rgba(138, 43, 226, 0.6), 0px 0px 15px rgba(106, 90, 205, 0.4)',
  },
  description: {
    fontSize: '24px',
    color: '#000000',
    marginBottom: '40px',
    fontWeight: '500',
    textShadow: '0px 0px 6px rgba(0, 0, 0, 0.4)',
  },
  button: {
    background: 'linear-gradient(90deg, #8e8cff, #b080ff)',
    color: '#000000',
    fontWeight: 'bold',
    fontSize: '20px',
    padding: '14px 24px',
    border: 'none',
    borderRadius: '25px',
    cursor: 'pointer',
    transition: 'background 0.3s ease, transform 0.2s',
    boxShadow: '0px 6px 20px rgba(0, 0, 0, 0.3)',
  },
  buttonHover: {
    background: 'linear-gradient(90deg, #7565c4, #a47ee5)',
    transform: 'scale(1.05)',
  },
};

export default App;
