import React, { Component } from 'react';
import HousekeepingList from './HousekeepingListFull';
import HousekeepingFilterDialog from './HousekeepingFilterDialog'
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';
import FilterListIcon from '@material-ui/icons/FilterList';
import Fab from '@material-ui/core/Fab';
import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import RemoveIcon from '@material-ui/icons/Remove';

class HouseKeeping extends Component {
    constructor() {
        super();
        this.state = {
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
         console.log('data: ', data);
         if (data.status == 'success') {
           this.setState({ housekeeping: data.data.logs, 'isLoading': false})
           if (data.data.logs.length > 0) {
            this.setState({empty: false})
          }
         }
        });
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
                      <Grid item sm={1}>
                        <TextField
                          id="outlined-name"
                          label="Start Date"
                          margin="dense"
                          variant="outlined"
                        />
                      </Grid>
                      <RemoveIcon style={{marginBottom: '20px'}} />
                      <Grid item sm={1}>
                        <TextField
                          id="outlined-name"
                          label="End Date"
                          margin="dense"
                          variant="outlined"
                        />
                      </Grid>
                      <Grid item sm={2}>
                        <Fab onClick={console.log('clicked!')} variant="extended">
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