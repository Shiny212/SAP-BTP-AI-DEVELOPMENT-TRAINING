import {
  Card,
  CardContent,
  Typography,
  Divider,
  Box,
  Chip,
} from "@mui/material";

import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
} from "@mui/lab";

import {
  FaBookOpen,
  FaGraduationCap,
  FaRocket,
} from "react-icons/fa";

function LearningPath({ recommendation }) {
  if (!recommendation) {
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
          >
            🛣 Learning Path
          </Typography>

          <Typography
            mt={2}
            color="text.secondary"
          >
            Ask a question to generate your personalized learning roadmap.
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
        >
          🛣 Learning Path
        </Typography>

        <Divider sx={{ my: 2 }} />

        <Timeline
          sx={{
            p: 0,
            "& .MuiTimelineItem-root:before": {
              flex: 0,
              padding: 0,
            },
          }}
        >
          {recommendation.learning_sequence.map(
            (step, index) => (
              <TimelineItem key={index}>
                <TimelineSeparator>

                  <TimelineDot color="primary">
                    {index ===
                    recommendation.learning_sequence.length - 1 ? (
                      <FaRocket />
                    ) : index === 0 ? (
                      <FaGraduationCap />
                    ) : (
                      <FaBookOpen />
                    )}
                  </TimelineDot>

                  {index !==
                    recommendation.learning_sequence.length - 1 && (
                    <TimelineConnector />
                  )}
                </TimelineSeparator>

                <TimelineContent>

                  <Box
                    sx={{
                      p: 2,
                      borderRadius: 2,
                      bgcolor: "background.default",
                    }}
                  >
                    <Typography
                      fontWeight="bold"
                    >
                      Step {index + 1}
                    </Typography>

                    <Typography mt={1}>
                      {step}
                    </Typography>

                    <Chip
                      size="small"
                      sx={{ mt: 1 }}
                      color="primary"
                      label={`Stage ${index + 1}`}
                    />

                  </Box>

                </TimelineContent>

              </TimelineItem>
            )
          )}
        </Timeline>

      </CardContent>
    </Card>
  );
}

export default LearningPath;