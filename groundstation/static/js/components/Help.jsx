import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';

class Help extends Component {
    constructor(){
        super();
        this.state = {
        }
    }

    render(){
        return (
            <div>
                <Typography variant="h4" style={{color: '#28324C'}}>
                    Help Page
                </Typography>
                <Paper className="Flight Schedule" style={{marginTop: '20px', marginBottom: '20px'}}>
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Flight Schedule
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        The flight schedule page allows you to build, edit, and queue flight schedules
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        Flight Schedules are colour coded based on their status. Grey is a draft,
                        blue is the currently queued flight schedule, and green means that the 
                        flight schedule has already been uploaded to the satellite. Only one 
                        flight schedule may be queued at a time and a queued schedule will be
                        automatically uploaded to the satellite during the next passover. It is
                        also possible to upload a schedule manually via the live commands.
                    </Typography>
                </Paper>
                <Paper className="Housekeeping" style={{marginBottom: '20px'}}>
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Housekeeping
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        Use Housekeeping to view the status and health of the satellite.
                    </Typography>
                </Paper>
                <Paper className="Live Commands">
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Live Commands
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        Send commands to the satellite via the live commands page
                        commands are formatted as "command_name arg1 arg2 ... "
                        where the number and content of arguments will differ based
                        on the command being sent.
                    </Typography>
                </Paper> 
            </div>       
        )   
    }
}

export default Help;