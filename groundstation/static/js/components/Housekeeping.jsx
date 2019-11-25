import React, { Component } from 'react';
import HousekeepingList from './HousekeepingListFull';
import Paper from '@material-ui/core/Paper';
import Typography from '@material-ui/core/Typography';

class HouseKeeping extends Component {
    constructor() {
        super();
        this.state = {
          empty: true,
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
                    <Typography variant="h5" displayInline style={{padding: '10px'}}>Housekeeping</Typography>
                    <HousekeepingList isLoading={this.state.isLoading} housekeeping={this.state.housekeeping} empty={this.state.empty} />
                </Paper>
            </div>
        )
    }
}
export default HouseKeeping;