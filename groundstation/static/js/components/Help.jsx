import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import AddIcon from '@material-ui/icons/Add';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import moment from "moment";
import 'moment-timezone';
import MomentUtils from '@date-io/moment';
import {
  DateTimePicker,
  MuiPickersUtilsProvider
} from "@material-ui/pickers";
import TextField from '@material-ui/core/TextField';
import Fab from '@material-ui/core/Fab';

class Help extends Component {
    constructor(){
        super();
        this.state = {
            commands : []
        }
    }

    componentDidMount(){
        fetch('./api/telecommands',{headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}})
        .then(results => {
            return results.json();
        }).then(data => {
            if (data.status == 'success') {
                this.setState(prevState => ({
                    commands: data.data.telecommands
                }));
            } else {
                // NOTE: should do something here maybe
                console.log("Error loading telecommands!");
            }
        });
    }

    render(){
        moment.tz.setDefault("UTC");
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
                        Flight Schedules are colour coded based on their status. Grey is a draft flight schedule,
                        <Paper style={{marginLeft: '20px', borderLeft: 'solid 8px #A9A9A9', marginBottom: '10px', marginRight: '20px'}}>
                            <div style={{fontWeight: 'bold'}}>
                                Draft Flight Schedule
                            </div>
                        </Paper>
                        blue is the currently queued flight schedule,
                        <Paper style={{marginLeft: '20px', borderLeft: 'solid 8px #4bacb8', marginBottom: '10px', marginRight: '20px'}}>
                            <div style={{fontWeight: 'bold'}}>
                                Queued Flight Schedule
                            </div>
                        </Paper>
                        and green means that the flight schedule has already been uploaded to the satellite.
                        <Paper style={{marginLeft: '20px', borderLeft: 'solid 8px #479b4e', marginBottom: '10px', marginRight: '20px'}}>
                            <div style={{fontWeight: 'bold'}}>
                                Uploaded Flight Schedule
                            </div>
                        </Paper>
                        Only one flight schedule may be queued at a time and a queued schedule will be
                        automatically uploaded to the satellite during the next passover. It is
                        also possible to upload a schedule manually via the live commands.
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px'}}>
                        A Flight schedule can be edited using <EditIcon style={{ color: '#4bacb8' }}/>, 
                        or deleted with <DeleteIcon style={{ color: '#4bacb8'}}/>,
                        and you can add a new flight schedule using:     
                        <Fab>
                            <AddIcon 
                                style={{ color: '#4bacb8', fontSize: '2rem'}} 
                            />
                        </Fab>
                    </Typography> 
                    <Typography variant="h6" style={{paddingLeft: '20px'}}>
                        Editing/Creating a Flight Schedule: 
                    </Typography>                   
                    <Typography variant="body1" style={{paddingLeft: '20px'}}>
                        When editing/creating a flight schedule, you first set an execution time
                        in the execution time box:
                        <form style={{paddingTop: '10px'}}>
                            <MuiPickersUtilsProvider utils={MomentUtils}>
                                <DateTimePicker 
                                    label="Execution Time"
                                    inputVariant="outlined"
                                />
                            </MuiPickersUtilsProvider>
                        </form> 
                        This is the time that the set of commands will be executed. You can add
                        commands using the <AddIcon style={{color: '#4bacb8'}}/> icon which allows you 
                        to select from the list of available commands. Then, you fill in the relevant
                        arguments which will depend on the command and set a delta time in the delta time field:
                        <form>
                            <TextField
                                id="outlined-basic"
                                label="Delta Time"
                                variant="outlined"
                                type="number"
                            />
                        </form>
                        The delta time is an offset from the scheduled time in seconds. This means the command
                        will execute x seconds after the scheduled time. You can also delete any command in 
                        the flight schedule using the <DeleteIcon style={{ color: '#4bacb8'}}/> to the right of
                        the command.
                    </Typography> 
                </Paper>
                <Paper className="Housekeeping" style={{marginBottom: '20px'}}>
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Housekeeping
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        Use Housekeeping to view the status and health of the satellite.
                        Each housekeeping log contains information about the satellite like
                        the watchdog timers as well as voltages. A housekeeping file with
                        a green tag means that the housekeeping log is healthy and detected 
                        no issues
                        <Paper style={{marginLeft: '20px', borderLeft: 'solid 8px #479b4e', marginBottom: '10px', marginRight: '20px'}}>
                            <div style={{fontWeight: 'bold'}}>
                                Healthy Housekeeping Log
                            </div>
                        </Paper>
                        Whereas a red tag signifies that there may be an issue with the satellite
                        <Paper style={{marginLeft: '20px', borderLeft: 'solid 8px #721c24', marginBottom: '10px', marginRight: '20px'}}>
                            <div style={{fontWeight: 'bold'}}>
                                Critical Housekeeping Log
                            </div>
                        </Paper>
                        You can also filter housekeeping logs by timestamp using the filter options
                    </Typography>
                </Paper>
                <Paper className="Live Commands" style={{marginBottom: '20px'}}>
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Live Commands
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        Send telecommands to the satellite via the live commands page.
                        Commands are formatted as "command_name arg1 arg2 ... "
                        where the number and content of arguments will differ based
                        on the command being sent.
                        The list of valid telecommands is:
                        <Paper style={{marginBottom: '20px'}}>
                            <Typography variant="h6">
                                Telecommands
                            </Typography>
                            {this.state.commands.map((command) => (
                                // console.log(command.command_name) 
                                // console.log()
                                <Typography variant="body1" style={{ paddingLeft: '10px' }}>
                                    Name: {command.command_name} <br/>Number of Arguments: {command.num_arguments}
                                </Typography>
                            ))}
                        </Paper>
                        The live commands page displays any messages sent to or received from the satellite
                        communications module. Note that the live commands window will only display the commands
                        for the duration you are on the page. To view a complete history of the communications with
                        the satellite, go to the logs page. The messages will be from one of a username (ie a human 
                        operator), the satellite (comm), or sent as part of an automated script (automation). 
                    </Typography>
                </Paper> 
                <Paper className="Logs" style={{marginBottom: '20px' }}>
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Logs
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        The logs page displays all of the communications to and from the satellite.
                        To update the page, press the refresh button. All messages will be denoted
                        as from one of a username (ie a human operator), the satellite (comm), or 
                        sent as part of an automated script (automation).
                    </Typography>
                </Paper>
                <Paper className="Timer">
                    <Typography variant="h5" displayInline style={{ padding: '10px' }}>
                        Passover Timer
                    </Typography>
                    <Typography variant="body1" style={{paddingLeft: '20px' }}>
                        On the navigation bar, you will see a timer. This denotes when the next
                        scheduled satellite passover is. If the timer is yellow, it is counting down until
                        the next expected passover. When an expected passover begins, the timer
                        will turn green and begin counting up signifying how much time has elapsed
                        during the current passover. Once a passover ends, the timer will turn 
                        yellow again and begin counting down until the next passover.
                    </Typography>
                </Paper>
            </div>       
        )   
    }
}

export default Help;