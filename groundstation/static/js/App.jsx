import React from 'react';
import Routes from './routes'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
// import './App.css';

const styles = {
  navbarLinks: {
    color: '#fff',
    "&:hover": {
        color: "#55c4d3"
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
                              <a className="link-items" href="/">
                                <img 
                                  src='https://albertasat.ca/wp-content/uploads/sites/43/2019/06/FINALLOGO_RGB_White.png' 
                                  style={{maxWidth: '55px'}}
                                />
                              </a>
                              <a className="indent">AlbertaSat</a>
                            </Typography>
                            <Typography className="menu-links">
                                <a 
                                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}` }
                                  href="/livecommands" >
                                    Live Commands
                                  </a>
                                <a 
                                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`} 
                                  href="/housekeeping">
                                  Housekeeping
                                </a>
                                <a 
                                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`} 
                                  href="/flightschedule">
                                  Flight Schedule
                                </a>
                                <a
                                  className={`link-items hvr-underline-from-center ${classes.navbarLinks}`}
                                  href="/logs">
                                  Logs
                                </a>
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