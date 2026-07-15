import { createContext, useMemo, useState } from "react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";

export const ColorModeContext = createContext();

export default function ThemeContextProvider({ children }) {
  const [mode, setMode] = useState("light");

  const colorMode = useMemo(
    () => ({
      toggleColorMode: () =>
        setMode((prev) => (prev === "light" ? "dark" : "light")),
      mode,
    }),
    [mode]
  );

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,

          primary: {
            main: "#1565C0",
          },

          secondary: {
            main: "#7B1FA2",
          },

          background: {
            default: mode === "light" ? "#F4F6F8" : "#121212",
            paper: mode === "light" ? "#FFFFFF" : "#1E1E1E",
          },
        },

        typography: {
          fontFamily: "Poppins, Roboto, Arial",
        },

        shape: {
          borderRadius: 14,
        },
      }),
    [mode]
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}