import React from 'react';
import Routes from './routes'
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
// import './App.css';


function App() {
    return (
       		<div>
                <div className="menu-bar">
                    <AppBar position="static">
                        <Toolbar>
                            <Typography variant="h6">
                            <a className="link-items indent" href="/">AlbertaSat</a>
                            </Typography>
                            <Typography className="menu-links">
                                <a className="link-items secondary" href="/livecommands">Live Commands</a>
                                <a className="link-items secondary" href="/flightschedule">Flight Schedule</a>
                            </Typography>
                        </Toolbar>
                    </AppBar>
                </div>
                <Routes />
        	</div>
       );
    }

export default App;