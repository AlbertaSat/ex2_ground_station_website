import React from 'react';
import Routes from './routes'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Countdown from './components/Countdown';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
// import './App.css';

const styles = {
  navbarLinks: {
    color: '#fff',
    "&:hover": {
        color: "#4bacb8"
      }
  } 
}


function App(props) {
  const { classes } = props;
    return (
       		<div>
                <div className="menu-bar">
                    <AppBar position="static">
                        <Toolbar>
                            <Typography variant="h6">
                              <a className="link-items indent" href="/">
                                <img 
                                  src='https://albertasat.ca/wp-content/uploads/sites/43/2019/06/FINALLOGO_RGB_White.png' 
                                  style={{maxWidth: '55px'}}
                                />
                              </a>
                            </Typography>
                            <Typography className="menu-links" style={{display: 'inline-flex', alignItems: 'center'}}>
                                <a 
                                  className={`link-items ${classes.navbarLinks}`}
                                  href="/livecommands" >
                                    Live Commands
                                  </a>
                                <a 
                                  className={`link-items ${classes.navbarLinks}`} 
                                  href="/housekeeping">
                                  Housekeeping
                                </a>
                                <a 
                                  className={`link-items ${classes.navbarLinks}`} 
                                  href="/flightschedule">
                                  Flight Schedule
                                </a>
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