import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';

class Home extends Component {
  constructor() {
    super();
    this.state = {
      empty: false,
      isLoaded: false,
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
      if (results.status == 401) { // if data is empty
        this.setState({ empty: true })
      }
      return results.json();
    }).then(data => {
      this.setState({ housekeeping: data.data, isLoaded: true })
      console.log(this.state.housekeeping);
    })
  }

  render() {
    const { isLoaded, housekeeping, error } = this.state;
    return (
      <div>
        <h1>This is our GroundStation!</h1>
        {error ? (
          <div>
            <ErrorOutlineIcon /> There is currently no housekeeping data!
          </div>
        ) : (
          <div></div>
        )}
        {isLoaded && !error ? (
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