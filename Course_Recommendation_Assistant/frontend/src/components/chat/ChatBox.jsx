import { useState } from "react";

import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Stack,
  Snackbar,
  Alert,
  Box,
  Chip,
} from "@mui/material";

import { FaPaperPlane } from "react-icons/fa";

import Loading from "../common/Loading";
import { getRecommendation } from "../../api/api";

function ChatBox({
  setRecommendation,
  history,
  setHistory,
}) {
  const [question, setQuestion] = useState("");

  const [loading, setLoading] = useState(false);

  const [open, setOpen] = useState(false);

  const [message, setMessage] = useState("");

  const [severity, setSeverity] = useState("success");

  const handleSubmit = async () => {
    if (!question.trim()) {
      setSeverity("warning");
      setMessage("Please enter your question.");
      setOpen(true);
      return;
    }

    try {
      setLoading(true);

      const response = await getRecommendation(question);

      setRecommendation(response);

      setHistory((previous) => [
        ...previous,
        {
          question,
          answer: response.recommended_courses.join(", "),
          confidence: response.confidence,
        },
      ]);

      setSeverity("success");
      setMessage("Recommendation generated successfully!");
      setOpen(true);

      setQuestion("");
    } catch (error) {
      console.error(error);

      setSeverity("error");
      setMessage(
        error.message || "Unable to connect to FastAPI backend."
      );
      setOpen(true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Card
        elevation={4}
        sx={{
          borderRadius: 3,
          mb: 3,
        }}
      >
        <CardContent>
          <Typography
            variant="h4"
            fontWeight="bold"
            gutterBottom
          >
            🤖 AI Learning Advisor
          </Typography>

          <Typography
            variant="body1"
            color="text.secondary"
            mb={3}
          >
            Describe your background, experience, and learning goals.
            The AI will recommend the most suitable learning path.
          </Typography>

          <Box mb={2}>
            <Stack
              direction="row"
              spacing={1}
              flexWrap="wrap"
            >
              <Chip
                label="Gemini 3.1 Flash Lite"
                color="secondary"
              />

              <Chip
                label="LangChain"
                color="success"
              />

              <Chip
                label="FAISS"
                color="primary"
              />
            </Stack>
          </Box>

          <TextField
            fullWidth
            multiline
            rows={6}
            label="Enter your question"
            placeholder={`Examples:

• I am an SAP ABAP developer with no AI experience.
  Which course should I take first?

• I know Python but not LangChain.
  Suggest a learning roadmap.

• Recommend SAP Business AI courses.`}
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
          />

          <Stack
            direction="row"
            spacing={2}
            mt={3}
          >
            <Button
              variant="contained"
              size="large"
              endIcon={<FaPaperPlane />}
              onClick={handleSubmit}
              disabled={loading}
              sx={{
                borderRadius: 3,
                px: 4,
              }}
            >
              {loading
                ? "Thinking..."
                : "Get Recommendation"}
            </Button>

            <Button
              variant="outlined"
              color="secondary"
              size="large"
              onClick={() => setQuestion("")}
              disabled={loading}
              sx={{
                borderRadius: 3,
              }}
            >
              Clear
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {loading && <Loading />}

      <Snackbar
        open={open}
        autoHideDuration={3000}
        onClose={() => setOpen(false)}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
      >
        <Alert
          severity={severity}
          variant="filled"
          onClose={() => setOpen(false)}
        >
          {message}
        </Alert>
      </Snackbar>
    </>
  );
}

export default ChatBox;