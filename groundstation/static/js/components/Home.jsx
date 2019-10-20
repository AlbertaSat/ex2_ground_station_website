import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';

class Home extends Component {
  constructor() {
    super();
    this.state = {
      isLoading: false,
      housekeeping: null
      // {
      //   id: null,
      //   satelliteMode: null,
      //   batteryVoltage: null,
      //   currentIn: null,
      //   currentOut: null,
      //   lastBeaconTime: null,
      //   noMCUResets: null
      // }
    };
  }

  componentDidMount() {
    fetch('/api/housekeepinglog/1')
    .then(results => {
      return results.json();
    }).then(data => {
      this.setState({ housekeeping: data.data, isLoading: true })
      console.log(this.state.housekeeping);
    })
  }

  render() {
    const { isLoading, housekeeping } = this.state;
    return (
      <div>
        <h1>This is our GroundStation!</h1>
        {isLoading ? (
          <div>
            <p>Id: {housekeeping.id}</p>
            <p>satelliteMode: {housekeeping.satelliteMode}</p>
            <p>batteryVoltage: {housekeeping.batteryVoltage}</p>
            <p>currentIn: {housekeeping.currentIn}</p>
            <p>currentOut: {housekeeping.currentOut}</p>
            <p>lastBeaconTime: {housekeeping.lastBeaconTime}</p>
            <p>noMCUResets: {housekeeping.noMCUResets}</p>
          </div>
        // If there is a delay in data, let's let the user know it's loading
        ) : (
          <CircularProgress />
        )}
      </div>
    )
  }
}
export default Home;