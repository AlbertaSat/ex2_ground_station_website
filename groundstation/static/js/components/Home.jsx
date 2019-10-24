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
    if (empty) {
      return (
        <div>
        <ErrorOutlineIcon /> There is currently no housekeeping data!
        </div>
      )
    }
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
                          <TableCell align="right">SatelliteMode</TableCell>
                          <TableCell align="right">BatteryVoltage</TableCell>
                          <TableCell align="right">CurrentIn</TableCell>
                          <TableCell align="right">CurrentOut</TableCell>
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
            </Paper>
          </Grid>
        </Grid>

        </div>

        // {isLoaded ? (
        //   <div>
        //     <p>Id: {housekeeping.id}</p>
        //     <p>satelliteMode: {housekeeping.satelliteMode}</p>
        //     <p>batteryVoltage: {housekeeping.batteryVoltage}</p>
        //     <p>currentIn: {housekeeping.currentIn}</p>
        //     <p>currentOut: {housekeeping.currentOut}</p>
        //     <p>lastBeaconTime: {housekeeping.lastBeaconTime}</p>
        //     <p>noMCUResets: {housekeeping.noMCUResets}</p>
        //   </div>
        // // If there is a delay in data, let's let the user know it's loading
        // ) : (
        //   <CircularProgress />
        // )}
      // </div>
    )
  }
}
export default Home;