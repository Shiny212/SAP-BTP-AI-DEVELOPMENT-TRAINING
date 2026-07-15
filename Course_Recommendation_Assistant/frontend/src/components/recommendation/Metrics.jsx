import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  LinearProgress,
} from "@mui/material";

import {
  FaBullseye,
  FaClock,
  FaBook,
  FaComments,
} from "react-icons/fa";

function MetricCard({
  title,
  value,
  subtitle,
  icon,
  color,
  progress = null,
}) {
  return (
    <Card
      elevation={4}
      sx={{
        borderRadius: 3,
        height: "100%",
        transition: "0.3s",
        "&:hover": {
          transform: "translateY(-5px)",
          boxShadow: 10,
        },
      }}
    >
      <CardContent>
        <Box
          display="flex"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography
            variant="subtitle1"
            fontWeight="bold"
          >
            {title}
          </Typography>

          <Box
            sx={{
              color,
              fontSize: 30,
            }}
          >
            {icon}
          </Box>
        </Box>

        <Typography
          variant="h4"
          mt={2}
          fontWeight="bold"
          color={color}
        >
          {value}
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
          mt={1}
        >
          {subtitle}
        </Typography>

        {progress !== null && (
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{
              mt: 2,
              height: 8,
              borderRadius: 5,
            }}
          />
        )}
      </CardContent>
    </Card>
  );
}

function Metrics({
  recommendation,
  history,
}) {
  if (!recommendation) return null;

  const confidence = Math.round(
    recommendation.confidence * 100
  );

  return (
    <Grid container spacing={2}>

      <Grid size={{ xs: 12 }}>
        <MetricCard
          title="Confidence"
          value={`${confidence}%`}
          subtitle="AI Prediction Score"
          icon={<FaBullseye />}
          color="#1565C0"
          progress={confidence}
        />
      </Grid>

      <Grid size={{ xs: 12 }}>
        <MetricCard
          title="Learning Hours"
          value={recommendation.total_learning_hours}
          subtitle="Estimated Study Time"
          icon={<FaClock />}
          color="#2E7D32"
        />
      </Grid>

      <Grid size={{ xs: 12 }}>
        <MetricCard
          title="Recommended Courses"
          value={
            recommendation.recommended_courses.length
          }
          subtitle="Courses Selected"
          icon={<FaBook />}
          color="#7B1FA2"
        />
      </Grid>

      <Grid size={{ xs: 12 }}>
        <MetricCard
          title="Conversations"
          value={history?.length || 0}
          subtitle="Questions Asked"
          icon={<FaComments />}
          color="#F57C00"
        />
      </Grid>

    </Grid>
  );
}

export default Metrics;