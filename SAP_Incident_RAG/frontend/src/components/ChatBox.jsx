import { useState } from "react";

import { askQuestion } from "../services/api";

import Loader from "./Loader";
import Message from "./Message";

function ChatBox() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    const userQuestion = question;

    setMessages((previous) => [
      ...previous,
      {
        type: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");

    setLoading(true);

    try {
      const answer = await askQuestion(userQuestion);

      setMessages((previous) => [
        ...previous,
        {
          type: "bot",
          text: answer,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((previous) => [
        ...previous,
        {
          type: "bot",
          text: "Unable to connect to the SAP Knowledge Assistant.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">

      <div className="messages">

        {messages.map((message, index) => (
          <Message
            key={index}
            type={message.type}
            text={message.text}
          />
        ))}

        {loading && <Loader />}

      </div>

      <div className="input-container">

        <input
          type="text"
          placeholder="Ask an SAP Incident question..."
          value={question}
          onChange={(event) =>
            setQuestion(event.target.value)
          }
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              handleAsk();
            }
          }}
        />

        <button onClick={handleAsk}>
          Ask Gemini
        </button>

      </div>

    </div>
  );
}

export default ChatBox;