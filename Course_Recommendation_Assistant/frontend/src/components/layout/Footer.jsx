import {
  Box,
  Typography,
  Divider,
  Stack,
  Chip,
} from "@mui/material";

import {
  FaReact,
  FaPython,
  FaDatabase,
  FaRobot,
} from "react-icons/fa";

function Footer() {
  return (
    <Box
      sx={{
        mt: 6,
        mb: 2,
      }}
    >
      <Divider sx={{ mb: 3 }} />

      <Stack
        spacing={2}
        alignItems="center"
      >
        <Typography
          variant="h6"
          fontWeight="bold"
        >
          🎓 Course Recommendation Assistant
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          textAlign="center"
        >
          AI-powered learning recommendation system built using
          React, FastAPI, LangChain, FAISS, and Gemini 3.1 Flash Lite.
        </Typography>

        <Stack
          direction="row"
          spacing={1}
          flexWrap="wrap"
          justifyContent="center"
        >
          <Chip
            icon={<FaReact />}
            label="React"
            color="primary"
          />

          <Chip
            icon={<FaPython />}
            label="FastAPI"
            color="success"
          />

          <Chip
            icon={<FaDatabase />}
            label="FAISS"
            color="secondary"
          />

          <Chip
            icon={<FaRobot />}
            label="Gemini 3.1 Flash Lite"
            color="warning"
          />
        </Stack>

        <Typography
          variant="body2"
          color="text.secondary"
        >
          © 2026 All Rights Reserved
        </Typography>

        <Typography
          variant="caption"
          color="text.secondary"
        >
          Developed for SAP BTP AI Development
        </Typography>
      </Stack>
    </Box>
  );
}

export default Footer;