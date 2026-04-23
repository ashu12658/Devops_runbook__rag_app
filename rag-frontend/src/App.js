import React, { useState } from "react";

function App() {

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMessage = { role: "user", text: message };
    setMessages(prev => [...prev, userMessage]);

    setLoading(true);

    try {

      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          query: message
        })
      });

      const data = await response.json();

      const botMessage = {
        role: "bot",
        text: data.answer
      };

      setMessages(prev => [...prev, botMessage]);

    } catch (err) {

      setMessages(prev => [
        ...prev,
        { role: "bot", text: "⚠️ Server error" }
      ]);

    }

    setMessage("");
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (

    <div style={styles.page}>

      <div style={styles.app}>

        {/* 🔥 HEADER */}
        <div style={styles.header}>
          <div>
            <h2 style={styles.title}>Developer Runbook RAG</h2>
            <p style={styles.subtitle}>AI Troubleshooting Agent</p>
          </div>
          <span style={styles.tag}>RAG SYSTEM</span>
        </div>

        {/* CHAT */}
        <div style={styles.chatBox}>

          {messages.length === 0 && (
            <div style={styles.placeholder}>
              Ask about logs, deployments, Docker, CI/CD issues...
            </div>
          )}

          {messages.map((msg, i) => (
            <div
              key={i}
              style={msg.role === "user" ? styles.userMsg : styles.botMsg}
            >
              {msg.text}
            </div>
          ))}

          {loading && (
            <div style={styles.loading}>Thinking...</div>
          )}

        </div>

        {/* INPUT */}
        <div style={styles.inputArea}>

          <div style={styles.glowBorder}>
            <div style={styles.inputWrapper}>

              <input
                type="text"
                placeholder="Ask a DevOps issue..."
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKey}
                style={styles.input}
              />

              <button onClick={sendMessage} style={styles.button}>
                Send →
              </button>

            </div>
          </div>

        </div>

      </div>

    </div>
  );
}

const styles = {

  page: {
    height: "100vh",
    background: "linear-gradient(135deg,#020617,#0f172a,#1e293b)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    fontFamily: "Inter, sans-serif"
  },

  app: {
    width: "920px",
    height: "85vh",
    background: "#0f172a",
    borderRadius: "16px",
    display: "flex",
    flexDirection: "column",
    boxShadow: "0 30px 80px rgba(0,0,0,0.7)"
  },

  header: {
    padding: "22px",
    borderBottom: "1px solid #1e293b",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    color: "white"
  },

  title: {
    margin: 0,
    fontSize: "20px",
    fontWeight: "600"
  },

  subtitle: {
    margin: 0,
    fontSize: "12px",
    color: "#64748b"
  },

  tag: {
    color: "#38bdf8",
    fontSize: "12px",
    letterSpacing: "1px"
  },

  chatBox: {
    flex: 1,
    padding: "20px",
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: "16px"
  },

  placeholder: {
    textAlign: "center",
    color: "#64748b",
    marginTop: "120px"
  },

  userMsg: {
    alignSelf: "flex-end",
    background: "#2563eb",
    color: "white",
    padding: "14px 18px",
    borderRadius: "12px",
    maxWidth: "70%"
  },

  botMsg: {
    alignSelf: "flex-start",
    background: "#1e293b",
    color: "#e2e8f0",
    padding: "14px 18px",
    borderRadius: "12px",
    maxWidth: "75%",
    lineHeight: "1.6",
    whiteSpace: "pre-wrap"
  },

  loading: {
    color: "#38bdf8"
  },

  inputArea: {
    padding: "18px",
    borderTop: "1px solid #1e293b"
  },

  glowBorder: {
    padding: "1.5px",
    borderRadius: "14px",
    background: "linear-gradient(270deg, #38bdf8, #6366f1, #a855f7, #38bdf8)",
    backgroundSize: "300% 300%",
    animation: "glowMove 8s ease infinite"
  },

  inputWrapper: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    background: "#020617",
    borderRadius: "12px",
    padding: "6px"
  },

  input: {
    flex: 1,
    padding: "12px",
    border: "none",
    background: "transparent",
    color: "white",
    outline: "none",
    fontSize: "14px"
  },

  button: {
    background: "#3b82f6",
    border: "none",
    color: "white",
    padding: "10px 16px",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "14px",
    transition: "0.2s"
  }

};

export default App;