import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';

import HousekeepingList from './HousekeepingListFull';
import Passovers from './Passovers';
import Countdown from './Countdown';

const styles = {
  root: {
    width: '100%'
  },
  pageHeading: {
    padding: '10px 40px',
    display: 'inline-flex',
    alignItems: 'center'
  }
};


class Home extends Component {
  constructor() {
    super();
    this.state = {
      emptyhk: true,
      emptypassover: true,
      isLoading: true,
      housekeeping: [{
        id: null,
        satelliteMode: null,
        batteryVoltage: null,
        currentIn: null,
        currentOut: null,
        lastBeaconTime: null,
        noMCUResets: null
      }],
      passovers: []
    };
  }

  componentDidMount() {
    // console.log(localStorage.getItem('auth_token'))
    Promise.all([
      fetch('/api/housekeepinglog?limit=5'),
      fetch('/api/passovers?next=true&limit=10',
      {headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}}
    )]).then(([res1, res2]) => {
      return Promise.all([res1.json(), res2.json()])
    }).then(([res1, res2]) => {
      console.log(res2);
      if(res1.status == 'success'){
        this.setState({ housekeeping: res1.data.logs, 'isLoading': false});
        if (res1.data.logs.length > 0) {
          this.setState({emptyhk: false})
        }
      }if(res2.status == 'success'){
        this.setState({passovers: res2.data.next_passovers, 'isLoading': false})
        console.log(res2.data.next_passovers.length)
        if (res2.data.next_passovers.length > 0) {
          this.setState({emptypassover: false})
        }
      }
    });
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <Grid container spacing={2} alignItems='flex-end'>
          <Grid item sm={12}>
            <div className={classes.pageHeading}>
              <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                OVERVIEW
              </Typography>
              {/*
              <Typography variant="h7" displayInline style={{marginLeft: '20px', borderBottom : '2px solid #28324C', color: '28324C'}}>
                Updates every 30 seconds
              </Typography>
              */}
            </div>
          </Grid>
        </Grid>
        <Grid container spacing={2} alignItems='flex-start'>
          <Grid item sm={8}>
            <Paper className="grid-containers">
              <Typography className="header-title" variant="h5" displayInline>Recent Housekeeping Data</Typography>
              <HousekeepingList isLoading={this.state.isLoading} housekeeping={this.state.housekeeping} empty={this.state.emptyhk} />
            </Paper>
          </Grid>
          <Grid item sm={4}>
            <Paper className="grid-containers">
              <Typography variant="h5" displayInline style={{padding: '10px'}}>Upcoming Passovers</Typography>
              <Passovers isLoading={this.state.isLoading} passovers={this.state.passovers} empty={this.state.emptypassover}/>
            </Paper>
          </Grid>
        </Grid>

        </div>
    )
  }
}

export default withStyles(styles)(Home);
