import {
  Card,
  CardContent,
  Skeleton,
  Stack
} from "@mui/material";

function Loading() {

  return (

    <Card
      elevation={3}
      sx={{
        mt:3,
        borderRadius:3
      }}
    >

      <CardContent>

        <Stack spacing={2}>

          <Skeleton
            variant="text"
            width="40%"
            height={40}
          />

          <Skeleton
            variant="rounded"
            height={80}
          />

          <Skeleton
            variant="rounded"
            height={80}
          />

          <Skeleton
            variant="rounded"
            height={80}
          />

        </Stack>

      </CardContent>

    </Card>

  );

}

export default Loading;