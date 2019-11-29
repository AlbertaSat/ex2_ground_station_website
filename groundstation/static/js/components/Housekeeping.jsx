import React, { Component } from 'react';
import HousekeepingList from './HousekeepingListFull';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import FilterListIcon from '@material-ui/icons/FilterList';
import Fab from '@material-ui/core/Fab';
import Grid from '@material-ui/core/Grid';
import moment from "moment";
import 'moment-timezone';
import MomentUtils from '@date-io/moment';
import {
  DateTimePicker,
  MuiPickersUtilsProvider
} from "@material-ui/pickers";
import ClearIcon from '@material-ui/icons/Clear';

class HouseKeeping extends Component {
  constructor() {
    moment.tz.setDefault("UTC");
    super();
    this.state = {
      startDate: null,
      startDateError: false,
      endDate: null,
      endDateError: false,
      open: false,
      empty: true,
      isLoading: true,
      housekeeping: [{
            id: null,
            satelliteMode: null,
            batteryVoltage: null,
            currentIn: null,
            currentOut: null,
            lastBeaconTime: null,
            noMCUResets: null,
            channels: []
      }],
      flightschedule: []
    };
  }

  componentDidMount() {
    fetch('/api/housekeepinglog?newest-first=true')
      .then(results => {
        return results.json();
      }).then(data => {
        if (data.status == 'success') {
          this.setState({ housekeeping: data.data.logs, 'isLoading': false })
          if (data.data.logs.length > 0) {
            this.setState({ empty: false })
          }
        }
      });
  }

  handleStartDateChange(event) {
    this.setState({ startDate: event._d.toISOString() })
  }
  handleEndDateChange(event) {
    this.setState({ endDate: event._d.toISOString() })
  }

  handleFilter() {
    if (this.state.endDate == null && this.state.startDate == null) {
      this.setState({ startDateError: true });
      this.setState({ endDateError: true });
    } else if (this.state.startDate == null) {
      this.setState({ startDateError: true })
    } else if (this.state.endDate == null) {
      this.setState({ endDateError: true })
    } else {
      let queryString = "?last_beacon_time=ge-" + this.state.startDate + "&last_beacon_time=le-" + this.state.endDate + "&newest-first=true"
      fetch('/api/housekeepinglog' + queryString)
        .then(results => {
          return results.json();
        }).then(data => {
          if (data.status == 'success') {
            this.setState({ housekeeping: data.data.logs, 'isLoading': false })
            if (data.data.logs.length > 0) {
              this.setState({ empty: false })
            } else {
              this.setState({ empty: true })
            }
          }
        })
    }
  }

  handleClearFilter() {
    this.setState({ startDate: null, endDate: null })
    this.setState({ startDateError: false });
    this.setState({ endDateError: false });
    fetch('/api/housekeepinglog?newest-first=true')
      .then(results => {
        return results.json();
      }).then(data => {
        if (data.status == 'success') {
          this.setState({ housekeeping: data.data.logs, 'isLoading': false })
          if (data.data.logs.length > 0) {
            this.setState({ empty: false })
          } else {
            this.setState({ empty: true })
          }
        }
      })
  }

  render() {
    return (
      <div>
        <Paper className="grid-containers">
          <div>
            <Grid container spacing={2} alignItems='flex-end'>
              <Grid item sm={2}>
                <Typography variant="h5" displayInline style={{ padding: '10px' }}>Housekeeping</Typography>
              </Grid>
              <Grid item sm={6}>
                <Grid container spacing={1} alignItems='flex-end'>
                  <Grid item sm={3}>
                    <form>
                      <MuiPickersUtilsProvider moment={moment} utils={MomentUtils}>
                        <DateTimePicker
                          label="Start Date"
                          showTodayButton
                          onChange={(event) => { this.handleStartDateChange(event) }}
                          value={this.state.startDate}
                          style={{ width: '100%' }}
                          name="startdate"
                          error={this.state.startDateError}
                        />
                      </MuiPickersUtilsProvider>
                    </form>
                  </Grid>
                  <Grid item sm={3}>
                    <form>
                      <MuiPickersUtilsProvider moment={moment} utils={MomentUtils}>
                        <DateTimePicker
                          label="End Date"
                          showTodayButton
                          onChange={(event) => { this.handleEndDateChange(event) }}
                          value={this.state.endDate}
                          style={{ width: '100%' }}
                          name="enddate"
                          error={this.state.endDateError}
                        />
                      </MuiPickersUtilsProvider>
                    </form>
                  </Grid>
                  <Grid item sm={2}>
                    <Fab ref="filter-button" onClick={() => { this.handleFilter() }} variant="extended" name="filter"
                      style={{ fontSize: '0.75rem', height: '40px', marginBottom: '20px', backgroundColor: '#55c4d3' }}>
                      <FilterListIcon />
                      Filter
                    </Fab>
                  </Grid>
                  <Grid item xs={2}>
                    <Fab onClick={() => { this.handleClearFilter() }} variant="extended" name="clear"
                      style={{ fontSize: '0.75rem', height: '40px', marginBottom: '20px', backgroundColor: '#55c4d3' }}>
                      <ClearIcon />
                      Clear
                    </Fab>
                  </Grid>
                </Grid>
              </Grid>
            </Grid>
          </div>
          <HousekeepingList isLoading={this.state.isLoading} housekeeping={this.state.housekeeping} empty={this.state.empty} />
        </Paper>
      </div>
    )
  }
}
export default HouseKeeping;
