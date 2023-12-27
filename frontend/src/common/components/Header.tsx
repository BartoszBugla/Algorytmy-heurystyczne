import { AppBar, Button, IconButton, Toolbar, Typography } from '@mui/material';

const Header = () => {
  return (
    <AppBar position='static'>
      <Toolbar>
        <IconButton
          size='large'
          edge='start'
          color='inherit'
          aria-label='menu'
          sx={{ mr: 2 }}
        ></IconButton>
        <Typography variant='h6' component='div' sx={{ flexGrow: 1 }}>
          Algorytmy metaheurystyczne
        </Typography>
        <Button color='inherit'>Lista algorytmów</Button>
        <Button color='inherit'>Lista funkcji</Button>
      </Toolbar>
    </AppBar>
  );
};

export { Header };
