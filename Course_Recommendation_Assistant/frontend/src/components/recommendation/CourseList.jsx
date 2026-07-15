import { Typography, Box } from "@mui/material";
import CourseCard from "./CourseCard";

function CourseList({ recommendation }) {
  if (!recommendation) return null;

  return (
    <Box mt={4}>
      <Typography
        variant="h4"
        fontWeight="bold"
        gutterBottom
      >
        📘 Recommended Courses
      </Typography>

      <Typography
        variant="body1"
        color="text.secondary"
        mb={3}
      >
        Based on your background and learning goals, these are the best
        courses to follow in sequence.
      </Typography>

      {recommendation.recommended_courses.map((course, index) => {
        const metadata = recommendation.source_metadata.find(
          (item) => item.course_name === course
        );

        return (
          <CourseCard
            key={index}
            course={course}
            metadata={metadata}
          />
        );
      })}
    </Box>
  );
}

export default CourseList;