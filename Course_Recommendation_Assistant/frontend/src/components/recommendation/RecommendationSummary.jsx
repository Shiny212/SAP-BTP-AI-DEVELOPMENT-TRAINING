import {
  Card,
  CardContent,
  Typography,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Stack,
  Box,
} from "@mui/material";

import {
  FaLightbulb,
  FaBook,
  FaArrowRight,
  FaCheckCircle,
} from "react-icons/fa";

function RecommendationSummary({ recommendation }) {
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
            💡 AI Recommendation Summary
          </Typography>

          <Typography
            mt={2}
            color="text.secondary"
          >
            Submit a question to receive an AI-generated explanation,
            recommended learning path, and prerequisites.
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

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
          mb={2}
        >
          <Typography
            variant="h5"
            fontWeight="bold"
          >
            💡 AI Recommendation Summary
          </Typography>

          <Chip
            color="success"
            label={`${(
              recommendation.confidence * 100
            ).toFixed(0)}% Confidence`}
          />
        </Stack>

        <Divider sx={{ mb: 2 }} />

        {/* WHY */}

        <Typography
          variant="h6"
          gutterBottom
        >
          Why these courses?
        </Typography>

        <Box
          sx={{
            bgcolor: "background.default",
            p: 2,
            borderRadius: 2,
          }}
        >
          <Typography>
            {recommendation.reason}
          </Typography>
        </Box>

        <Divider sx={{ my: 3 }} />

        {/* PREREQUISITES */}

        <Typography
          variant="h6"
          gutterBottom
        >
          📚 Prerequisites
        </Typography>

        <List dense>
          {recommendation.prerequisites.map(
            (item, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  <FaBook color="#1976D2" />
                </ListItemIcon>

                <ListItemText primary={item} />
              </ListItem>
            )
          )}
        </List>

        <Divider sx={{ my: 3 }} />

        {/* LEARNING PATH */}

        <Typography
          variant="h6"
          gutterBottom
        >
          🚀 Suggested Learning Order
        </Typography>

        <List dense>
          {recommendation.learning_sequence.map(
            (item, index) => (
              <ListItem key={index}>
                <ListItemIcon>
                  <FaArrowRight color="#2E7D32" />
                </ListItemIcon>

                <ListItemText primary={item} />
              </ListItem>
            )
          )}
        </List>

        <Divider sx={{ my: 3 }} />

        {/* AI STATUS */}

        <Stack
          direction="row"
          spacing={2}
          flexWrap="wrap"
        >
          <Chip
            icon={<FaLightbulb />}
            label="AI Recommendation"
            color="primary"
          />

          <Chip
            icon={<FaCheckCircle />}
            label="Verified Learning Path"
            color="success"
          />
        </Stack>

      </CardContent>
    </Card>
  );
}

export default RecommendationSummary;