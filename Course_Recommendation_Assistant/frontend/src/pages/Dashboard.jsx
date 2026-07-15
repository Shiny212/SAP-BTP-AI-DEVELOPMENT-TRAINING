import { Grid } from "@mui/material";

import WelcomeBanner from "../components/common/WelcomeBanner";

import ChatBox from "../components/chat/ChatBox";
import ChatHistory from "../components/chat/ChatHistory";

import CourseList from "../components/recommendation/CourseList";
import RecommendationSummary from "../components/recommendation/RecommendationSummary";
import Metrics from "../components/recommendation/Metrics";
import LearningPath from "../components/recommendation/LearningPath";
import SourceTable from "../components/recommendation/SourceTable";

function Dashboard({
  recommendation,
  setRecommendation,
  history,
  setHistory,
}) {
  return (
    <Grid container spacing={3}>
      {/* ================= LEFT SECTION ================= */}

      <Grid size={{ xs: 12, lg: 8 }}>
        <WelcomeBanner />

        <ChatBox
          setRecommendation={setRecommendation}
          history={history}
          setHistory={setHistory}
        />

        <ChatHistory history={history} />

        <CourseList recommendation={recommendation} />

        <RecommendationSummary
          recommendation={recommendation}
        />
      </Grid>

      {/* ================= RIGHT SECTION ================= */}

      <Grid size={{ xs: 12, lg: 4 }}>
        <Metrics
          recommendation={recommendation}
          history={history}
        />

        <LearningPath
          recommendation={recommendation}
        />

        <SourceTable
          recommendation={recommendation}
        />
      </Grid>
    </Grid>
  );
}

export default Dashboard;