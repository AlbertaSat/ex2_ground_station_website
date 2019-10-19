import React, { Component } from 'react';

class Home extends Component {
  constructor() {
    super();
    this.state = {
      isLoading: false,
      housekeeping: {
        id: null,
        satelliteMode: null,
        batteryVoltage: null,
        currentIn: null,
        currentOut: null,
        lastBeaconTime: null,
        noMCUResets: null
      }
    };
  }

  componentDidMount() {
    this.state.isLoading = true;
    fetch('/api/housekeepinglog/1')
    .then(results => {
      return results.json();
    }).then(data => {
      this.state.isLoading = false;
      this.state.housekeeping.id = data.data.id;
      this.state.housekeeping.satelliteMode = data.data.satelliteMode;
      this.state.housekeeping.batteryVoltage = data.data.batteryVoltage;
      this.state.housekeeping.currentIn = data.data.currentIn;
      this.state.housekeeping.currentOut = data.data.currentOut;
      this.state.housekeeping.lastBeaconTime = data.data.lastBeaconTime;
      this.state.housekeeping.noMCUResets = data.data.noMCUResets;
      console.log(this.state.housekeeping);
    })
  }

  render() {
    return (
      <div>
        <h1>This is our GroundStation!</h1>
      </div>
    )
  }
}
export default Home;