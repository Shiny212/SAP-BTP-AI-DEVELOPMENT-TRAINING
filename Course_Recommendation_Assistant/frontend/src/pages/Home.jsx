import { useState } from "react";

import {
  Box,
  Toolbar,
} from "@mui/material";

import Header from "../components/layout/Header";
import Sidebar from "../components/layout/Sidebar";
import Footer from "../components/layout/Footer";

import Dashboard from "./Dashboard";

const drawerWidth = 260;

function Home() {

  const [recommendation, setRecommendation] = useState(null);

  const [history, setHistory] = useState([]);

  const [mobileOpen, setMobileOpen] = useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen((prev) => !prev);
  };

  return (
    <Box sx={{ display: "flex" }}>

      {/* Header */}
      <Header
        handleDrawerToggle={handleDrawerToggle}
      />

      {/* Sidebar */}
      <Sidebar
        mobileOpen={mobileOpen}
        handleDrawerToggle={handleDrawerToggle}
      />

      {/* Main Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          width: {
            md: `calc(100% - ${drawerWidth}px)`,
          },
          bgcolor: "background.default",
          minHeight: "100vh",
          p: 3,
        }}
      >
        {/* Prevent content from going under AppBar */}
        <Toolbar />

        <Dashboard
          recommendation={recommendation}
          setRecommendation={setRecommendation}
          history={history}
          setHistory={setHistory}
        />

        <Footer />
      </Box>
    </Box>
  );
}

export default Home;