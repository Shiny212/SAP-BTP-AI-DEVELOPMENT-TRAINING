import {
  Card,
  CardContent,
  Typography,
  Divider,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  TableContainer,
  Paper,
  Chip,
} from "@mui/material";

function getLevelColor(level) {
  if (!level) return "default";

  const text = level.toLowerCase();

  if (text.includes("beginner")) return "success";

  if (text.includes("intermediate")) return "primary";

  if (text.includes("advanced")) return "secondary";

  return "default";
}

function SourceTable({ recommendation }) {
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
            📂 Source Metadata
          </Typography>

          <Typography
            mt={2}
            color="text.secondary"
          >
            Source information will appear after generating a recommendation.
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
          📂 Source Metadata
        </Typography>

        <Divider sx={{ my: 2 }} />

        <TableContainer
          component={Paper}
          sx={{
            maxHeight: 350,
            borderRadius: 2,
          }}
        >
          <Table stickyHeader>

            <TableHead>

              <TableRow>

                <TableCell
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "primary.main",
                    color: "white",
                  }}
                >
                  Course ID
                </TableCell>

                <TableCell
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "primary.main",
                    color: "white",
                  }}
                >
                  Course Name
                </TableCell>

                <TableCell
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "primary.main",
                    color: "white",
                  }}
                >
                  Level
                </TableCell>

                <TableCell
                  sx={{
                    fontWeight: "bold",
                    bgcolor: "primary.main",
                    color: "white",
                  }}
                >
                  Duration
                </TableCell>

              </TableRow>

            </TableHead>

            <TableBody>

              {recommendation.source_metadata.map(
                (course, index) => (
                  <TableRow
                    key={index}
                    hover
                    sx={{
                      "&:nth-of-type(even)": {
                        bgcolor: "#f8f9fa",
                      },
                    }}
                  >
                    <TableCell>
                      {course.course_id}
                    </TableCell>

                    <TableCell>
                      <Typography
                        fontWeight="bold"
                      >
                        {course.course_name}
                      </Typography>
                    </TableCell>

                    <TableCell>
                      <Chip
                        size="small"
                        label={
                          course.experience_level
                        }
                        color={getLevelColor(
                          course.experience_level
                        )}
                      />
                    </TableCell>

                    <TableCell>
                      <Chip
                        size="small"
                        color="info"
                        label={course.duration}
                      />
                    </TableCell>

                  </TableRow>
                )
              )}

            </TableBody>

          </Table>
        </TableContainer>

      </CardContent>
    </Card>
  );
}

export default SourceTable;