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
  const classes = useStyles();

  const [isAdmin, setIsAdmin] = React.useState(false);
  const [openUserMenu, setOpenUserMenu] = React.useState(false);
  const [openUtilMenu, setOpenUtilMenu] = React.useState(false);

  const userMenuAnchor = React.useRef(null);
  const utilMenuAnchor = React.useRef(null);

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

  const handleToggleUserMenu = () => {
    setOpenUserMenu((prevOpen) => !prevOpen);
  };

  const handleToggleUtilMenu = () => {
    setOpenUtilMenu((prevOpen) => !prevOpen);
  };

  const handleCloseUserMenu = (event) => {
    if (
      userMenuAnchor.current &&
      userMenuAnchor.current.contains(event.target)
    ) {
      return;
    }

    setOpenUserMenu(false);
  };

  const handleCloseUtilMenu = (event) => {
    if (
      utilMenuAnchor.current &&
      utilMenuAnchor.current.contains(event.target)
    ) {
      return;
    }

    setOpenUtilMenu(false);
  };

  function handleListKeyDown(event) {
    if (event.key === 'Tab') {
      event.preventDefault();
      setOpenUserMenu(false);
      setOpenUtilMenu(false);
    }
  }

  // return focus to the button when we transitioned from !open -> open
  const prevOpenUser = React.useRef(openUserMenu);
  const prevOpenUtil = React.useRef(openUtilMenu);

  React.useEffect(() => {
    if (prevOpenUser.current === true && openUserMenu === false) {
      userMenuAnchor.current.focus();
    }
    if (prevOpenUtil.current === true && openUtilMenu === false) {
      utilMenuAnchor.current.focus();
    }
    prevOpenUser.current = openUserMenu;
    prevOpenUtil.current = openUtilMenu;
  }, [openUserMenu, openUtilMenu]);

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
                <div>
                  <a
                    className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                    ref={utilMenuAnchor}
                    aria-controls={openUtilMenu ? 'menu-list-grow' : undefined}
                    aria-haspopup="true"
                    onClick={handleToggleUtilMenu}
                  >
                    Utilities
                  </a>
                  <Popper
                    open={openUtilMenu}
                    anchorEl={utilMenuAnchor.current}
                    role={undefined}
                    placement="bottom-end"
                    transition
                    disablePortal
                  >
                    {({ TransitionProps, placement }) => (
                      <Grow
                        {...TransitionProps}
                        style={{
                          transformOrigin:
                            placement === 'bottom'
                              ? 'right bottom'
                              : 'right top'
                        }}
                      >
                        <Paper>
                          <ClickAwayListener onClickAway={handleCloseUtilMenu}>
                            <MenuList>
                              <MenuItem onClick={handleCloseUtilMenu}>
                                <a
                                  style={{
                                    color: 'rgb(40, 50, 76)',
                                    width: '100%'
                                  }}
                                  href="/automatedcommandsequence"
                                >
                                  Automated Command Sequence
                                </a>
                              </MenuItem>
                              <MenuItem onClick={handleCloseUtilMenu}>
                                <a
                                  style={{
                                    color: 'rgb(40, 50, 76)',
                                    width: '100%'
                                  }}
                                  href="/flightschedule"
                                >
                                  Flightschedules
                                </a>
                              </MenuItem>
                              <MenuItem onClick={handleCloseUtilMenu}>
                                <a
                                  style={{
                                    color: 'rgb(40, 50, 76)',
                                    width: '100%'
                                  }}
                                  href="/ftp"
                                >
                                  FTP
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
                    ref={userMenuAnchor}
                    aria-controls={openUserMenu ? 'menu-list-grow' : undefined}
                    aria-haspopup="true"
                    onClick={handleToggleUserMenu}
                  >
                    <Avatar style={{ backgroundColor: '#55c4d3' }}>
                      {username.charAt(0).toUpperCase()}
                    </Avatar>
                  </Button>
                  <Popper
                    open={openUserMenu}
                    anchorEl={userMenuAnchor.current}
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
                          <ClickAwayListener onClickAway={handleCloseUserMenu}>
                            <MenuList
                              autoFocusItem={openUserMenu}
                              id="menu-list-grow"
                              onKeyDown={handleListKeyDown}
                            >
                              <MenuItem disabled>{username}</MenuItem>
                              {isAdmin && (
                                <MenuItem onClick={handleCloseUserMenu}>
                                  <a
                                    style={{ color: 'rgb(40, 50, 76)' }}
                                    href="/manageusers"
                                  >
                                    Manage Users
                                  </a>
                                </MenuItem>
                              )}
                              <MenuItem onClick={handleCloseUserMenu}>
                                <a
                                  style={{ color: 'rgb(40, 50, 76)' }}
                                  href="/resetpassword"
                                >
                                  Reset Password
                                </a>
                              </MenuItem>
                              <MenuItem onClick={handleCloseUserMenu}>
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
