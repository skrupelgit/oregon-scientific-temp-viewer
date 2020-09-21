import App from "./components/App";
import ReactDOM from 'react-dom';
import React from 'react'
import { createMuiTheme, makeStyles, ThemeProvider } from '@material-ui/core/styles'

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#534bae',
      main: "#1a237e",
      dark: '#000051',
      contrastText: '#fff',
    },
    secondary: {
      light: '#4c8c4a',
      main: '#1b5e20',
      dark: '#003300',
      contrastText: '#fff',

    },
  },
});


ReactDOM.render(
  <ThemeProvider theme={theme}>
    <App />
    </ThemeProvider>,
    document.getElementById('app')
  );