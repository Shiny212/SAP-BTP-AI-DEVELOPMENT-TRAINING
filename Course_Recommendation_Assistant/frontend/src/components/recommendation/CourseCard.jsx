import {
  Card,
  CardContent,
  Typography,
  Chip,
  Stack,
  Divider,
  Box,
} from "@mui/material";

import {
  FaGraduationCap,
  FaClock,
  FaSignal,
  FaCheckCircle,
} from "react-icons/fa";

function getLevelColor(level) {
  if (!level) return "default";

  const text = level.toLowerCase();

  if (text.includes("beginner")) return "success";

  if (text.includes("intermediate")) return "primary";

  if (text.includes("advanced")) return "secondary";

  return "default";
}

function CourseCard({ course, metadata }) {
  return (
    <Card
      elevation={4}
      sx={{
        mt: 2,
        borderRadius: 3,
        transition: "0.3s",
        cursor: "pointer",

        "&:hover": {
          transform: "translateY(-5px)",
          boxShadow: 10,
        },
      }}
    >
      <CardContent>

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >

          <Stack
            direction="row"
            spacing={2}
            alignItems="center"
          >

            <FaGraduationCap
              color="#1976D2"
              size={30}
            />

            <Typography
              variant="h6"
              fontWeight="bold"
            >
              {course}
            </Typography>

          </Stack>

          <Chip
            icon={<FaCheckCircle />}
            label="Recommended"
            color="success"
          />

        </Stack>

        <Divider sx={{ my: 2 }} />

        <Box
          display="flex"
          gap={2}
          flexWrap="wrap"
        >

          <Chip
            icon={<FaSignal />}
            label={metadata?.experience_level || "N/A"}
            color={getLevelColor(metadata?.experience_level)}
            variant="outlined"
          />

          <Chip
            icon={<FaClock />}
            label={metadata?.duration || "N/A"}
            color="primary"
            variant="outlined"
          />

        </Box>

      </CardContent>
    </Card>
  );
}

export default CourseCard;