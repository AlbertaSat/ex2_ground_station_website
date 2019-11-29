import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import HousekeepingList from './HousekeepingListFull';
import Passovers from './Passovers';

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
      ticker:0,
      passovers: []
    };
    this.updatePassoverProgressBars = this.updatePassoverProgressBars.bind(this);
  }

  updatePassoverProgressBars() {
    // this is just to trigger the state change and re render lol, probably a better way to do it
    this.setState(prevState => ({ticker: prevState.ticker + 1}));
  }

  componentDidMount() {
    Promise.all([
      fetch('/api/housekeepinglog?newest-first=true&limit=5'),
      fetch('/api/passovers?next=true&most-recent=true&limit=5',
      {headers: {'Authorization':'Bearer '+ localStorage.getItem('auth_token')}}
    )]).then(([res1, res2]) => {
      return Promise.all([res1.json(), res2.json()])
    }).then(([res1, res2]) => {
      if(res1.status == 'success'){
        this.setState({ housekeeping: res1.data.logs, 'isLoading': false});
        if (res1.data.logs.length > 0) {
          this.setState({emptyhk: false})
        }
      }if(res2.status == 'success'){
        this.setState({passovers: res2.data.next_passovers, 'isLoading': false, mostRecentPass: res2.data.most_recent_passover})
        if (res2.data.next_passovers.length > 0 && res2.data.most_recent_passover !== null) {
          this.setState({emptypassover: false})
          this.timer = setInterval(
            () => this.updatePassoverProgressBars(),
            10000
          );
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
              <Typography variant="h5" displayInline>Upcoming Passovers</Typography>
              <Passovers isLoading={this.state.isLoading} passovers={this.state.passovers} empty={this.state.emptypassover} mostRecentPass={this.state.mostRecentPass}/>
            </Paper>
          </Grid>
        </Grid>

        </div>
    )
  }
}

export default withStyles(styles)(Home);
