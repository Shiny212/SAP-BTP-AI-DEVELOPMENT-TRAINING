import { useContext } from "react";

import {
  AppBar,
  Toolbar,
  Typography,
  Chip,
  IconButton,
  Box,
} from "@mui/material";

import MenuIcon from "@mui/icons-material/Menu";
import { LightMode, DarkMode } from "@mui/icons-material";

import { FaGraduationCap } from "react-icons/fa";

import { ColorModeContext } from "../../context/ThemeContext";

function Header({ handleDrawerToggle }) {
  const colorMode = useContext(ColorModeContext);

  return (
    <AppBar
      position="fixed"
      elevation={4}
      sx={{
        background:
          "linear-gradient(90deg,#1565C0,#1976D2,#42A5F5)",
        zIndex: (theme) => theme.zIndex.drawer + 1,
      }}
    >
      <Toolbar>

        {/* Mobile Menu */}

        <IconButton
          color="inherit"
          edge="start"
          onClick={handleDrawerToggle}
          sx={{
            mr: 2,
            display: {
              xs: "block",
              md: "none",
            },
          }}
        >
          <MenuIcon />
        </IconButton>

        {/* Logo */}

        <FaGraduationCap
          size={30}
          style={{ marginRight: 15 }}
        />

        {/* Title */}

        <Box sx={{ flexGrow: 1 }}>
          <Typography
            variant="h5"
            fontWeight="bold"
          >
            Course Recommendation Assistant
          </Typography>

          <Typography
            variant="body2"
            sx={{
              opacity: 0.9,
            }}
          >
            AI Powered Learning Recommendation System
          </Typography>
        </Box>

        {/* Gemini */}

        <Chip
          label="Gemini 3.1 Flash Lite"
          color="secondary"
          sx={{
            mr: 2,
            display: {
              xs: "none",
              sm: "flex",
            },
          }}
        />

        {/* Theme */}

        <IconButton
          color="inherit"
          onClick={colorMode.toggleColorMode}
        >
          {colorMode.mode === "light" ? (
            <DarkMode />
          ) : (
            <LightMode />
          )}
        </IconButton>
      </Toolbar>
    </AppBar>
  );
}

export default Header;