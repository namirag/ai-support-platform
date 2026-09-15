import { useEffect, useState } from "react";
import api from "./api";
import "./App.css";
import DocumentUpload from "./DocumentUpload";
import Analytics from "./Analytics";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState({});
  const [analyticsRefresh, setAnalyticsRefresh] = useState(0);

  useEffect(() => {
    const loadMessages = async () => {
      try {
        const response = await api.get("/conversations/1/messages");

        setMessages(
          response.data.map((message) => ({
            id: message.id,
            sender: message.sender,
            content: message.content,
          }))
        );
      } catch (error) {
        console.error("Unable to load conversation history.");
      }
    };

    loadMessages();
  }, []);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const customerQuestion = question;

    setMessages((previous) => [
      ...previous,
      {
        sender: "customer",
        content: customerQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await api.post("/chat", {
        conversation_id: 1,
        question: customerQuestion,
      });

      setMessages((previous) => [
        ...previous,
        {
          id: response.data.ai_message_id,
          sender: "ai",
          content: response.data.answer,
        },
      ]);

      setAnalyticsRefresh((previous) => previous + 1);

      setLoading(false);
    } catch (error) {
      setMessages((previous) => [
        ...previous,
        {
          sender: "ai",
          content: "Unable to connect to the support system.",
        },
      ]);

      setLoading(false);
    }
  };

  const sendFeedback = async (messageId, rating) => {
    try {
      await api.post("/feedback", {
        message_id: messageId,
        rating: rating,
        comment: rating === 5 ? "Helpful" : "Not helpful",
      });

      setFeedbackGiven((previous) => ({
        ...previous,
        [messageId]: rating,
      }));
    } catch (error) {
      console.error("Unable to submit feedback.");
    }
  };

  return (
    <div className="app">
      <h1>AI Customer Support Platform</h1>

      <p>Ask questions and get answers from company documents.</p>

      <DocumentUpload />

      <div className="chat-box">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`message ${
              message.sender === "customer" ? "customer" : "ai"
            }`}
          >
            <div className="message-content">
              {message.content}

              {message.sender === "ai" && message.id && (
                <div>
                  <button
                    onClick={() => sendFeedback(message.id, 5)}
                    disabled={feedbackGiven[message.id]}
                  >
                    {feedbackGiven[message.id] === 5
                      ? "✓ Submitted"
                      : "👍 Helpful"}
                  </button>

                  <button
                    onClick={() => sendFeedback(message.id, 1)}
                    disabled={feedbackGiven[message.id]}
                  >
                    {feedbackGiven[message.id] === 1
                      ? "✓ Submitted"
                      : "👎 Not helpful"}
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message ai">
            <div className="message-content">AI is thinking...</div>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask a support question..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") {
              askQuestion();
            }
          }}
        />

        <button onClick={askQuestion}>Ask</button>
      </div>

      <Analytics refresh={analyticsRefresh} />
    </div>
  );
}

export default App;