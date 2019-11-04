import React, { Component } from 'react';
import HousekeepingList from './HousekeepingListFull';

class HouseKeeping extends Component {
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
           this.setState({ housekeeping: data.data.logs, isLoaded: true, empty: false })
           console.log(this.state.housekeeping);
         }
        });
      }

    render() {
        return (
            <div>
                <h1 style={{padding: '10px'}}>HouseKeeping</h1>
                <HousekeepingList housekeeping={this.state.housekeeping} empty={this.state.empty} />
            </div>
        )
    }
}
export default HouseKeeping;