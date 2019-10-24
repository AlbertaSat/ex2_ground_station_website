import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Grid from '@material-ui/core/Grid';
import Paper from '@material-ui/core/Paper';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';

class Home extends Component {
  constructor() {
    super();
    this.state = {
      empty: true,
      isLoaded: false,
      housekeeping: {
        id: null,
        satelliteMode: null,
        batteryVoltage: null,
        currentIn: null,
        currentOut: null,
        lastBeaconTime: null,
        noMCUResets: null
      },
      flightschedule: {
        id: null,
        creationDate: null,
        timeStamp: null,
        uploadDate: null,
        flightscheduleCommands: {
          command_id: null,
          timeStamp: null
        }
      }
    };
  }

  componentDidMount() {
    fetch('/api/housekeepinglog')
    .then(results => {
      return results.json();
    }).then(data => {
      console.log('data: ', data);
      if (data.status == 'success') {
        this.setState({ housekeeping: data.data.logs, isLoaded: true, empty: false })
        console.log(this.state.housekeeping);
      }
    })
  }

  render() {
    const { isLoaded, housekeeping, empty } = this.state;
    const flightschedule = [
      {id: 1, creationDate: '2019-10-10 17:17:52', timeStamp: '2019-10-10 17:17:52', uploadDate: '2019-10-10 17:17:52',
        commands: [{
        commandId: 1,
        commandName: 'ping',
        timeStamp: '2019-10-10 17:17:52'
        },
        {commandId: 2,
        commandName: 'ddos',
        timeStamp: '2019-10-10 17:17:52'
        }
      ]},
      {id: 2, creationDate: '2019-10-10 17:17:52', timeStamp: '2019-10-10 17:17:52', uploadDate: '2019-10-10 17:17:52',
        commands: [{
        commandId: 1,
        commandName: 'destroy',
        timeStamp: '2019-10-10 17:17:52'
        },
        {commandId: 2,
          commandName: 'ping',
          timeStamp: '2019-10-10 17:17:52'
        }
      ]},
      {id: 3, creationDate: '2019-10-10 17:17:52', timeStamp: '2019-10-10 17:17:52', uploadDate: '2019-10-10 17:17:52',
        commands: [{
        commandId: 1,
        commandName: 'ping',
        timeStamp: '2019-10-10 17:17:52'
        }]
      }];
    if (empty) {
      return (
        <div>
        <ErrorOutlineIcon /> There is currently no housekeeping data!
        </div>
      )
    }
    console.log(flightschedule);
    return (
      <div>
        
        <Grid container spacing={2}>
          <Grid item sm>
            <Paper className="grid-containers">
              <h4 className="container-text">Recent Housekeeping Data</h4>
              
              {housekeeping.map(housekeeping => (
                <ExpansionPanel key={housekeeping.name}>
                  <ExpansionPanelSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                  >
                    <Typography>{housekeeping.lastBeaconTime}</Typography>
                  </ExpansionPanelSummary>
                  <ExpansionPanelDetails>
                    <Table aria-label="simple table">
                      <TableHead>
                        <TableRow>
                          <TableCell>ID</TableCell>
                          <TableCell align="right">Satellite Mode</TableCell>
                          <TableCell align="right">Battery Voltage</TableCell>
                          <TableCell align="right">Current In</TableCell>
                          <TableCell align="right">Current Out</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell component="th" scope="row">
                            {housekeeping.id}
                          </TableCell>
                          <TableCell align="right">{housekeeping.satelliteMode}</TableCell>
                          <TableCell align="right">{housekeeping.batteryVoltage}</TableCell>
                          <TableCell align="right">{housekeeping.currentIn}</TableCell>
                          <TableCell align="right">{housekeeping.currentOut}</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </ExpansionPanelDetails>
                </ExpansionPanel>
              ))}
            </Paper>
          </Grid>

          <Grid item sm>
            <Paper className="grid-containers">
              <h4 className="container-text">Upcoming Flight Schedules</h4>
              {flightschedule.map(flightschedule => (
                <ExpansionPanel key={flightschedule.id}>
                  <ExpansionPanelSummary
                    expandIcon={<ExpandMoreIcon />}
                    aria-controls="panel1a-content"
                    id="panel1a-header"
                  >
                    <Table aria-label="simple table">
                      <TableHead>
                        <TableRow>
                          <TableCell>ID</TableCell>
                          <TableCell align="right">Creation Date</TableCell>
                          <TableCell align="right">Upload Date</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow>
                          <TableCell component="th" scope="row">
                            {flightschedule.id}
                          </TableCell>
                          <TableCell align="right">{flightschedule.creationDate}</TableCell>
                          <TableCell align="right">{flightschedule.uploadDate}</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </ExpansionPanelSummary>
                  <ExpansionPanelDetails>
                    <Table aria-label="simple table">
                      <TableHead>
                        <TableRow>
                          <TableCell>ID</TableCell>
                          <TableCell align="right">Command Name</TableCell>
                          <TableCell align="right">Time Stamp</TableCell>
                        </TableRow>
                      </TableHead>
                   {flightschedule.commands.map(commands => (
                      <TableBody>
                        <TableRow>
                          <TableCell component ="th" scope="row">
                            {commands.commandId}
                          </TableCell>
                          <TableCell align="right">{commands.commandName}</TableCell>
                          <TableCell align="right">{commands.timeStamp}</TableCell>
                        </TableRow>
                      </TableBody>
                    ))} 
                   </Table>
                  </ExpansionPanelDetails>
                </ExpansionPanel>
              ))}
            </Paper>
          </Grid>
        </Grid>

        </div>
    )
  }
}
export default Home;