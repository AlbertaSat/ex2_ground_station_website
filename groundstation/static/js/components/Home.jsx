import React, { Component } from 'react';
import Grid from '@material-ui/core/Grid';
import Fab from '@material-ui/core/Fab';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import { withStyles } from '@material-ui/core/styles';
import Paper from '@material-ui/core/Paper';
import HousekeepingList from './HousekeepingListFull';
import Passovers from './Passovers';
import Switch from "@material-ui/core/Switch";
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';

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
      passovers: [],
      checked: false,
      popup: false
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

  handleToggleNotifications(event) {
    //const notifications = localStorage.getItem('notifications');
    //let updated_notifs = (notifications == 'true') ? 'false' : 'true';
    //localStorage.setItem('notifications', updated_notifs);

    this.setState({checked: event.target.checked });
    if (event.target.checked) this.setState({popup: true});
  }

  handleClose() {
    this.setState({popup: false});
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <Grid container spacing={2} alignItems='flex-end'>
          <Grid item sm={12}>
            <div className={classes.pageHeading}>
              <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                TEST 15
              </Typography>
            </div>
          </Grid>
          <Grid style={{ justifyContent: 'flex-end'}}>
            <Switch checked={this.state.checked} onChange={(event) => this.handleToggleNotifications(event)}/>
          </Grid>
          
          <Dialog open={this.state.popup} onClose={() => this.handleClose()}>
            <DialogTitle>Notifications</DialogTitle>
            <DialogContent>
              <DialogContentText>
                To subscribe to notifications, enter your slack username.
              </DialogContentText>
              <TextField
                autoFocus
                margin='dense'
                id='slack-username'
                label='Slack Username'
                type='email'
                fullWidth
                variant='standard'
                />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => this.handleClose()}>Cancel</Button>
              <Button onClick={() => this.handleClose()}>Subscribe</Button>
            </DialogActions>
          </Dialog>


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
