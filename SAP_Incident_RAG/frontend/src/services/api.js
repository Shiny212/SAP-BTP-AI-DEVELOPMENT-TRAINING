import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
});

export async function askQuestion(question) {
  const response = await api.post("/ask", {
    question,
  });

  return response.data.answer;
}

export default api;