import React, { Component, useState } from 'react';
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
import RemoveIcon from '@material-ui/icons/Remove';

class HouseKeeping extends Component {
    constructor() {
        super();
        this.state = {
          startDate: null,
          endDate: null,
          open: false,
          empty: true,
          isLoading: true,
          housekeeping: {
            id: null,
            satelliteMode: null,
            batteryVoltage: null,
            currentIn: null,
            currentOut: null,
            lastBeaconTime: null,
            noMCUResets: null
          },
          flightschedule: []
        };
        
      }
    
      componentDidMount() {
        fetch('/api/housekeepinglog')
        .then(results => {
         return results.json();
        }).then(data => {
         if (data.status == 'success') {
           this.setState({ housekeeping: data.data.logs, 'isLoading': false})
           if (data.data.logs.length > 0) {
            this.setState({empty: false})
          }
         }
        });
      }

      handleStartDateChange(event) {
        console.log(event._d.toISOString())
        this.setState({startDate: event._d.toISOString()})
      }
      handleEndDateChange(event) {
        this.setState({endDate: event._d.toISOString()})
      }

      handleFilter() {
        let queryString = "?last_beacon_time=ge-" + this.state.startDate + "&last_beacon_time=le-" + this.state.endDate
        fetch('/api/housekeepinglog' + queryString)
        .then(results => {
          return results.json();
        }).then(data => {
          if (data.status == 'success') {
            this.setState({ housekeeping: data.data.logs, 'isLoading': false})
            if (data.data.logs.length > 0) {
             this.setState({empty: false})
           }else {
             this.setState({empty: true})
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
                        <Typography variant="h5" displayInline style={{padding: '10px'}}>Housekeeping</Typography>
                      </Grid>
                      <Grid item sm={2}>
                        <form>
                        <MuiPickersUtilsProvider moment={moment} utils={MomentUtils}>
                        <DateTimePicker
                          label="Start Date"
                          format="MMM d YYYY hh:mm a"
                          showTodayButton
                          onChange={(event) => {this.handleStartDateChange(event)}}
                          value={this.state.startDate}
                        />
                        </MuiPickersUtilsProvider>
                        </form>
                      </Grid>
                      <RemoveIcon style={{marginBottom: '20px'}} />
                      <Grid item sm={2}>
                        <form>
                      <MuiPickersUtilsProvider moment={moment} utils={MomentUtils}>
                        <DateTimePicker
                          label="End Date"
                          format="MMM d YYYY hh:mm a"
                          showTodayButton
                          onChange={(event) => {this.handleEndDateChange(event)}}
                          value={this.state.endDate}
                        />
                        </MuiPickersUtilsProvider>
                        </form>
                      </Grid>
                      <Grid item sm={2}>
                        <Fab onClick={() => {this.handleFilter()}} variant="extended" style={{height: '40px', marginBottom: '5px'}}>
                          <FilterListIcon />
                          Filter
                        </Fab>
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