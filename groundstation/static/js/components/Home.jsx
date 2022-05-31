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
      ticker: 0,
      passovers: [],
      checked: (localStorage.getItem('subscribed_to_slack') == 'true') ? true : false,
      popup: false,
      slack_id: ''
    };
    this.updatePassoverProgressBars = this.updatePassoverProgressBars.bind(this);
  }

  updatePassoverProgressBars() {
    // this is just to trigger the state change and re render lol, probably a better way to do it
    this.setState(prevState => ({ ticker: prevState.ticker + 1 }));
  }

  componentDidMount() {
    Promise.all([
      fetch('/api/housekeepinglog?newest-first=true&limit=5'),
      fetch('/api/passovers?next=true&most-recent=true&limit=5',
        { headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('auth_token') } }
      )]).then(([res1, res2]) => {
        return Promise.all([res1.json(), res2.json()])
      }).then(([res1, res2]) => {
        if (res1.status == 'success') {
          this.setState({ housekeeping: res1.data.logs, 'isLoading': false });
          if (res1.data.logs.length > 0) {
            this.setState({ emptyhk: false })
          }
        } if (res2.status == 'success') {
          this.setState({ passovers: res2.data.next_passovers, 'isLoading': false, mostRecentPass: res2.data.most_recent_passover })
          if (res2.data.next_passovers.length > 0 && res2.data.most_recent_passover !== null) {
            this.setState({ emptypassover: false })
            this.timer = setInterval(
              () => this.updatePassoverProgressBars(),
              10000
            );
          }
        }
      });
  }

  isAuthenticated() {
    return !!sessionStorage.getItem('auth_token');
  }

  handleToggleNotifications(event) {
    this.setState({ checked: event.target.checked });
    if (event.target.checked) {
      this.setState({ popup: true });

      let user_id = localStorage.getItem('user_id');
      let url = '/api/users/' + user_id;

      fetch(url, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + sessionStorage.getItem('auth_token')
        }
      }).then(results => {
        return results.json();
      }).then(data => {
        if (data.status == 'success') {
          if (data.data.slack_id != null) {
            this.setState({ slack_id: data.data.slack_id });
          }
        }
      });
    }
    else {
      this.setSlack(false);
    }
  }

  handleClose(pressedCancel = false) {
    if (pressedCancel) {
      this.setState({ popup: false });
      this.setState({ checked: false });
      this.setSlack(false);
    }
    else {
      if (this.state.slack_id == '') {
        return;
      }

      this.setState({ popup: false });
      this.setSlack(true);
    }
  }

  setSlack(is_subscribed) {
    let user_id = localStorage.getItem('user_id');
    let url = '/api/users/' + user_id;
    let data = { slack_id: this.state.slack_id, subscribed_to_slack: is_subscribed };

    localStorage.setItem('subscribed_to_slack', is_subscribed);

    if (!data.subscribed_to_slack) delete data.slack_id; // do not need to set slack id if unsubscribed

    fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + sessionStorage.getItem('auth_token')
      },
      body: JSON.stringify(data)
    }).then(results => {
      console.log(results);
      return results.json();
    }).then(data => {
      console.log(data);
    });
  }

  handleChange(event) {
    this.setState({ slack_id: event.target.value });
  }

  render() {
    const { classes } = this.props;
    return (
      <div className={classes.root}>
        <Grid container spacing={2} alignItems='flex-end'>
          <Grid item sm={10}>
            <div className={classes.pageHeading}>
              <Typography variant="h4" style={{ color: '#28324C' }}>
                OVERVIEW2
              </Typography>
            </div>
          </Grid>
          <Grid item sm={2} style={{ textAlign: 'right' }}>
            {this.isAuthenticated() &&
              <Switch id='notification-switch' checked={this.state.checked} onChange={(event) => this.handleToggleNotifications(event)} />
            }
          </Grid>
          <Dialog open={this.state.popup} onClose={() => this.handleClose(true)}>
            <DialogTitle>Notifications</DialogTitle>
            <DialogContent>
              <DialogContentText>
                To subscribe to slack notifications, enter your slack id (not username!).
              </DialogContentText>
              <TextField
                autoFocus
                margin='dense'
                id='slack-username'
                label='Slack Username'
                type='email'
                fullWidth
                variant='standard'
                value={this.state.slack_id}
                onChange={(event) => this.handleChange(event)}
                error={this.state.slack_id == ''}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => this.handleClose(true)}>Cancel</Button>
              <Button onClick={() => this.handleClose()}>Subscribe</Button>
            </DialogActions>
          </Dialog>
        </Grid>
        <Grid container spacing={2} alignItems='flex-start'>
          <Grid item sm={8}>
            <Paper className="grid-containers">
              <Typography className="header-title" variant="h5">Recent Housekeeping Data</Typography>
              <HousekeepingList isLoading={this.state.isLoading} housekeeping={this.state.housekeeping} empty={this.state.emptyhk} />
            </Paper>
          </Grid>
          <Grid item sm={4}>
            <Paper className="grid-containers">
              <Typography variant="h5">Upcoming Passovers</Typography>
              <Passovers isLoading={this.state.isLoading} passovers={this.state.passovers} empty={this.state.emptypassover} mostRecentPass={this.state.mostRecentPass} />
            </Paper>
          </Grid>
        </Grid>

      </div>
    )
  }
}

export default withStyles(styles)(Home);
