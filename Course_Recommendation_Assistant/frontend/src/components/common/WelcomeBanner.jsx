import {
  Card,
  CardContent,
  Typography,
  Stack,
  Chip,
  Box,
} from "@mui/material";

import {
  FaRobot,
  FaDatabase,
  FaPython,
  FaReact,
} from "react-icons/fa";

function WelcomeBanner() {
  return (
    <Card
      elevation={5}
      sx={{
        mb: 3,
        borderRadius: 4,
        background:
          "linear-gradient(135deg,#1976D2,#42A5F5)",
        color: "white",
      }}
    >
      <CardContent>

        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >

          <Box>

            <Typography
              variant="h4"
              fontWeight="bold"
            >
              👋 Welcome
            </Typography>

            <Typography mt={1}>
              AI Course Recommendation Platform
            </Typography>

            <Typography
              variant="body2"
              sx={{
                opacity: 0.9,
                mt: 1,
              }}
            >
              Personalized AI learning roadmap powered by
              LangChain + Gemini + FastAPI
            </Typography>

            <Stack
              direction="row"
              spacing={1}
              mt={2}
              flexWrap="wrap"
            >
              <Chip
                icon={<FaRobot />}
                label="Gemini 3.1 Flash Lite"
                color="secondary"
              />

              <Chip
                icon={<FaDatabase />}
                label="FAISS"
                color="success"
              />

              <Chip
                icon={<FaPython />}
                label="FastAPI"
                color="warning"
              />

              <Chip
                icon={<FaReact />}
                label="React"
                color="primary"
              />
            </Stack>

          </Box>

          <Typography
            sx={{
              fontSize: 70,
            }}
          >
            🤖
          </Typography>

        </Box>

      </CardContent>
    </Card>
  );
}

export default WelcomeBanner;