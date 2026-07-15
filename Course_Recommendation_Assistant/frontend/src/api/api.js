import axios from "axios";

// FastAPI Backend URL
const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

// Get Course Recommendation
export const getRecommendation = async (question) => {
  try {
    const response = await API.post("/recommend", {
      question,
    });

    return response.data;
  } catch (error) {
    console.error("API Error:", error);

    if (error.response) {
      throw new Error(
        error.response.data.detail || "Backend Error"
      );
    }

    throw new Error("Unable to connect to FastAPI Backend.");
  }
};

export default API;