import React from 'react';
import Routes from './routes';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Countdown from './components/Countdown';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import ClickAwayListener from '@material-ui/core/ClickAwayListener';
import Grow from '@material-ui/core/Grow';
import Paper from '@material-ui/core/Paper';
import Popper from '@material-ui/core/Popper';
import MenuItem from '@material-ui/core/MenuItem';
import MenuList from '@material-ui/core/MenuList';
import { makeStyles } from '@material-ui/core/styles';

const styles = {
  navbarLinks: {
    color: '#fff',
    '&:hover': {
      color: '#55c4d3'
    }
  }
};
const useStyles = makeStyles((theme) => ({
  navbarLinks: {
    color: '#fff',
    '&:hover': {
      color: '#55c4d3'
    }
  }
}));

function isAuthenticated() {
  const hasSessionToken = !!sessionStorage.getItem('auth_token');
  if (hasSessionToken) return hasSessionToken;

  // if user had ticked "remember me" when logging in, auth info would be in localStorage
  if (!!localStorage.getItem('auth_token')) {
    sessionStorage.setItem('auth_token', localStorage.getItem('auth_token'));
    sessionStorage.setItem('username', localStorage.getItem('username'));
    return true;
  }
  return false;
}

var username = null;

function App() {
  const [isAdmin, setIsAdmin] = React.useState(false);
  if (isAuthenticated()) {
    username = sessionStorage.getItem('username');

    const auth_token = sessionStorage.getItem('auth_token');
    fetch(`/api/users/${auth_token}`)
      .then((results) => {
        return results.json();
      })
      .then((data) => {
        if (data.status === 'success') {
          setIsAdmin(data.data.is_admin);
        } else {
          console.error('Unexpected error occured:');
        }
      });
  }
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);

  const anchorRef = React.useRef(null);

  const handleToggle = () => {
    setOpen((prevOpen) => !prevOpen);
  };

  const handleClose = (event) => {
    if (anchorRef.current && anchorRef.current.contains(event.target)) {
      return;
    }

    setOpen(false);
  };

  function handleListKeyDown(event) {
    if (event.key === 'Tab') {
      event.preventDefault();
      setOpen(false);
    }
  }

  // return focus to the button when we transitioned from !open -> open
  const prevOpen = React.useRef(open);
  React.useEffect(() => {
    if (prevOpen.current === true && open === false) {
      anchorRef.current.focus();
    }

    prevOpen.current = open;
  }, [open]);
  return (
    <div>
      <div className="menu-bar">
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6">
              <a className="link-items" href="/">
                <img
                  src="https://albertasat.ca/wp-content/uploads/sites/43/2019/06/FINALLOGO_RGB_White.png"
                  style={{ maxWidth: '55px' }}
                />
              </a>
              <a className="indent" href="/">
                AlbertaSat
              </a>
            </Typography>
            <Typography
              className="menu-links"
              style={{ display: 'inline-flex', alignItems: 'center' }}
            >
              {isAuthenticated() && (
                <a
                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                  href="/automatedcommandsequence"
                >
                  Automated Command Sequence
                </a>
              )}
              {isAuthenticated() && (
                <a
                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                  href="/livecommands"
                >
                  Live Commands
                </a>
              )}
              <a
                className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                href="/housekeeping"
              >
                Housekeeping
              </a>
              {isAuthenticated() && (
                <a
                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                  href="/flightschedule"
                >
                  Flight Schedule
                </a>
              )}
              {isAuthenticated() && (
                <a
                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                  href="/logs"
                >
                  Logs
                </a>
              )}
              {isAuthenticated() && (
                <a
                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                  href="/help"
                >
                  Help
                </a>
              )}
              {!isAuthenticated() && (
                <a
                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                  href="/login"
                >
                  Login
                </a>
              )}

              {isAuthenticated() && (
                <div style={{ marginLeft: '3em' }}>
                  <Button
                    ref={anchorRef}
                    aria-controls={open ? 'menu-list-grow' : undefined}
                    aria-haspopup="true"
                    onClick={handleToggle}
                  >
                    <Avatar style={{ backgroundColor: '#55c4d3' }}>
                      {username.charAt(0).toUpperCase()}
                    </Avatar>
                  </Button>
                  <Popper
                    open={open}
                    anchorEl={anchorRef.current}
                    role={undefined}
                    transition
                    disablePortal
                  >
                    {({ TransitionProps, placement }) => (
                      <Grow
                        {...TransitionProps}
                        style={{
                          transformOrigin:
                            placement === 'bottom'
                              ? 'center top'
                              : 'center bottom'
                        }}
                      >
                        <Paper>
                          <ClickAwayListener onClickAway={handleClose}>
                            <MenuList
                              autoFocusItem={open}
                              id="menu-list-grow"
                              onKeyDown={handleListKeyDown}
                            >
                              <MenuItem disabled>{username}</MenuItem>
                              {isAdmin && (
                                <MenuItem onClick={handleClose}>
                                  <a
                                    style={{ color: 'rgb(40, 50, 76)' }}
                                    href="/manageusers"
                                  >
                                    Manage Users
                                  </a>
                                </MenuItem>
                              )}
                              <MenuItem onClick={handleClose}>
                                <a
                                  style={{ color: 'rgb(40, 50, 76)' }}
                                  href="/resetpassword"
                                >
                                  Reset Password
                                </a>
                              </MenuItem>
                              <MenuItem onClick={handleClose}>
                                <a
                                  style={{ color: 'rgb(40, 50, 76)' }}
                                  href="/logout"
                                >
                                  Logout
                                </a>
                              </MenuItem>
                            </MenuList>
                          </ClickAwayListener>
                        </Paper>
                      </Grow>
                    )}
                  </Popper>
                </div>
              )}
              <Countdown />
            </Typography>
          </Toolbar>
        </AppBar>
      </div>
      <div className="route-container">
        <Routes />
      </div>
    </div>
  );
}

export default withStyles(styles)(App);
