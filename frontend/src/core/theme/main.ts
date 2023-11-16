import { green, purple } from '@mui/material/colors';
import { createTheme } from '@mui/material/styles';

export const mainTheme = createTheme({
  components: {
    MuiTypography: {
      styleOverrides: {
        root: {
          color: 'white',
        },
      },
    },

    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundColor: '#1c1c1c',
          border: '1px solid gray',
          borderRadius: '0.5rem',
        },
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '1.5rem',
          boxShadow: 'none',
        },
      },
    },
  },
  palette: {
    mode: 'dark',

    primary: {
      main: purple[500],
    },
    secondary: {
      main: green[500],
    },

    divider: 'rgba(255, 255, 255, 0.12)',
  },
});
