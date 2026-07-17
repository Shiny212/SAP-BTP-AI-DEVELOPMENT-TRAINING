function Message({ type, text }) {
  return (
    <div
      className={
        type === "user"
          ? "message user-message"
          : "message bot-message"
      }
    >
      {text}
    </div>
  );
}

export default Message;