import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

import HousekeepingList from './HousekeepingList';
import FlightScheduleList from './FlightScheduleList'
import Countdown from './Countdown'

const styles = {
  root: {
    padding: '42px',
    display: 'inline-flex',
    alignItems: 'center'
  },
};


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
    const { classes } = this.props;
    console.log({classes});
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

    console.log(flightschedule);
    return (
      <div>
        <Grid container spacing={2} alignItems='flex-end'>
          <Grid item sm={8}>
            <div className={classes.root}>
              <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                OVERVIEW
              </Typography>
              <Typography variant="h7" displayInline style={{marginLeft: '20px', borderBottom : '2px solid #28324C', color: '28324C'}}>
                Updates every 30 seconds
              </Typography>
            </div>
          </Grid>
          <Grid item sm={4}>
            <Countdown />
          </Grid>
        </Grid>
        <Grid container spacing={2} alignItems='flex-start'>
          <Grid item sm={8}>
            <HousekeepingList housekeeping={this.state.housekeeping} empty={this.state.empty} />
          </Grid>
          <Grid item sm={4}>
            <FlightScheduleList flightschedule={flightschedule} isMinified={true}/>
          </Grid>
        </Grid>

        </div>
    )
  }
}

export default withStyles(styles)(Home);