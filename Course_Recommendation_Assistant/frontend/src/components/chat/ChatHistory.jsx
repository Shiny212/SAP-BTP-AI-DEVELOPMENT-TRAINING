import {
  Card,
  CardContent,
  Typography,
  Avatar,
  Stack,
  Paper,
  Divider,
  Chip,
  Box,
} from "@mui/material";

import {
  FaRobot,
  FaUserGraduate,
} from "react-icons/fa";

function ChatHistory({ history }) {
  if (!history || history.length === 0) {
    return (
      <Card
        elevation={3}
        sx={{
          mt: 3,
          borderRadius: 3,
        }}
      >
        <CardContent>
          <Typography
            variant="h5"
            fontWeight="bold"
            gutterBottom
          >
            💬 Conversation History
          </Typography>

          <Typography color="text.secondary">
            No conversations yet.
            <br />
            Ask your first question to receive an AI recommendation.
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card
      elevation={4}
      sx={{
        mt: 3,
        borderRadius: 3,
      }}
    >
      <CardContent>
        <Typography
          variant="h5"
          fontWeight="bold"
          gutterBottom
        >
          💬 Conversation History
        </Typography>

        {history.map((chat, index) => (
          <Box key={index} mb={4}>
            {/* USER */}

            <Stack
              direction="row"
              justifyContent="flex-end"
              spacing={2}
              mb={2}
            >
              <Paper
                elevation={2}
                sx={{
                  p: 2,
                  bgcolor: "primary.main",
                  color: "white",
                  maxWidth: "70%",
                  borderRadius: 3,
                }}
              >
                <Typography fontWeight="bold">
                  👤 You
                </Typography>

                <Typography mt={1}>
                  {chat.question}
                </Typography>
              </Paper>

              <Avatar
                sx={{
                  bgcolor: "primary.main",
                }}
              >
                <FaUserGraduate />
              </Avatar>
            </Stack>

            {/* AI */}

            <Stack
              direction="row"
              spacing={2}
            >
              <Avatar
                sx={{
                  bgcolor: "success.main",
                }}
              >
                <FaRobot />
              </Avatar>

              <Paper
                elevation={2}
                sx={{
                  p: 2,
                  bgcolor: "background.paper",
                  maxWidth: "75%",
                  borderRadius: 3,
                }}
              >
                <Typography
                  fontWeight="bold"
                  color="success.main"
                  gutterBottom
                >
                  🤖 AI Assistant
                </Typography>

                <Typography
                  variant="subtitle2"
                  gutterBottom
                >
                  Recommended Courses
                </Typography>

                {chat.answer
                  .split(",")
                  .map((course, i) => (
                    <Typography key={i}>
                      • {course.trim()}
                    </Typography>
                  ))}

                <Divider sx={{ my: 2 }} />

                <Chip
                  label={`Confidence ${(chat.confidence * 100).toFixed(0)}%`}
                  color="success"
                />
              </Paper>
            </Stack>
          </Box>
        ))}
      </CardContent>
    </Card>
  );
}

export default ChatHistory;