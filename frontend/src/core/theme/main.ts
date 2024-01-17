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

    MuiInputLabel: {
      defaultProps: {
        disableAnimation: true,
        shrink: true,
      },
      styleOverrides: {
        root: ({ theme }) => ({
          position: 'relative',
          transform: 'none',
          marginBottom: 6,
        }),
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
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          // remove default styling
          '& fieldset': {
            top: 0,
          },

          '& legend': {
            top: 0,
            span: { display: 'none' },
          },
        },
        notchedOutline: {
          borderRadius: 12,
          '& .Mui-focused': {
            borderColor: '#fff !imporatant',
          },
        },
      },
    },
    MuiInputBase: {
      defaultProps: {
        size: 'small',
      },
      styleOverrides: {
        root: {
          color: 'white',
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
    MuiSelect: {
      defaultProps: {
        size: 'small',
      },
    },

    MuiLink: {
      styleOverrides: {
        root: {
          color: 'white',
          textDecoration: 'underline',
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
    text: {
      secondary: 'grey',
    },

    divider: 'rgba(255, 255, 255, 0.12)',
  },
});
