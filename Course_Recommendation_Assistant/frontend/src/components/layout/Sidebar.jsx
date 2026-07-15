import {
  Drawer,
  Toolbar,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Typography,
  Avatar,
  Box,
  useMediaQuery,
  useTheme,
} from "@mui/material";

import {
  FaHome,
  FaRobot,
  FaBook,
  FaRoad,
  FaChartBar,
  FaHistory,
  FaInfoCircle,
  FaGraduationCap,
} from "react-icons/fa";

const drawerWidth = 260;

const menuItems = [
  {
    title: "Dashboard",
    icon: <FaHome />,
  },
  {
    title: "AI Assistant",
    icon: <FaRobot />,
  },
  {
    title: "Recommended Courses",
    icon: <FaBook />,
  },
  {
    title: "Learning Path",
    icon: <FaRoad />,
  },
  {
    title: "Analytics",
    icon: <FaChartBar />,
  },
  {
    title: "Conversation History",
    icon: <FaHistory />,
  },
  {
    title: "About",
    icon: <FaInfoCircle />,
  },
];

function Sidebar({
  mobileOpen,
  handleDrawerToggle,
}) {
  const theme = useTheme();

  const isMobile = useMediaQuery(
    theme.breakpoints.down("md")
  );

  const drawer = (
    <>
      <Toolbar />

      {/* Profile */}

      <Box
        sx={{
          textAlign: "center",
          py: 4,
        }}
      >
        <Avatar
          sx={{
            width: 70,
            height: 70,
            bgcolor: "primary.main",
            mx: "auto",
          }}
        >
          <FaGraduationCap size={28} />
        </Avatar>

        <Typography
          variant="h6"
          mt={2}
          fontWeight="bold"
        >
          Student Dashboard
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
        >
          SAP Business AI
        </Typography>
      </Box>

      <Divider />

      {/* Navigation */}

      <List>
        {menuItems.map((item, index) => (
          <ListItemButton
            key={index}
            sx={{
              mx: 1,
              my: 0.5,
              borderRadius: 2,

              "&:hover": {
                bgcolor: "primary.main",
                color: "white",

                "& .MuiListItemIcon-root": {
                  color: "white",
                },
              },
            }}
          >
            <ListItemIcon>{item.icon}</ListItemIcon>

            <ListItemText
              primary={item.title}
            />
          </ListItemButton>
        ))}
      </List>

      <Divider sx={{ mt: 2 }} />

      {/* Footer */}

      <Box
        sx={{
          mt: "auto",
          p: 2,
        }}
      >
        <Typography
          variant="caption"
          color="text.secondary"
        >
          Version 1.0
        </Typography>

        <Typography
          fontWeight="bold"
        >
          Gemini 3.1 Flash Lite
        </Typography>

        <Typography
          variant="body2"
          color="text.secondary"
        >
          React • FastAPI • LangChain
        </Typography>
      </Box>
    </>
  );

  return (
    <Box
      component="nav"
      sx={{
        width: {
          md: drawerWidth,
        },
        flexShrink: {
          md: 0,
        },
      }}
    >
      {/* Mobile Drawer */}

      <Drawer
        variant="temporary"
        open={mobileOpen}
        onClose={handleDrawerToggle}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: {
            xs: "block",
            md: "none",
          },

          "& .MuiDrawer-paper": {
            width: drawerWidth,
          },
        }}
      >
        {drawer}
      </Drawer>

      {/* Desktop Drawer */}

      <Drawer
        variant="permanent"
        sx={{
          display: {
            xs: "none",
            md: "block",
          },

          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
        open
      >
        {drawer}
      </Drawer>
    </Box>
  );
}

export default Sidebar;