import { createTheme } from "@mui/material/styles";

const theme = createTheme({

    palette: {

        mode: "light",

        primary: {
            main: "#1565C0"
        },

        secondary: {
            main: "#7B1FA2"
        },

        success: {
            main: "#2E7D32"
        },

        background: {
            default: "#F4F6F8",
            paper: "#FFFFFF"
        }

    },

    typography: {

        fontFamily: [
            "Poppins",
            "Roboto",
            "Arial",
            "sans-serif"
        ].join(","),

        h4: {

            fontWeight: 700

        },

        h5: {

            fontWeight: 600

        },

        h6: {

            fontWeight: 600

        }

    },

    shape: {

        borderRadius: 12

    }

});

export default theme;