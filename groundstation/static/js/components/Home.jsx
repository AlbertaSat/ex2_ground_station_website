import React, { Component } from 'react';
import CircularProgress from '@material-ui/core/CircularProgress';
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';

class Home extends Component {
  loadingIndicator(isLoaded){

  }

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
      }
    };
  }

  componentDidMount() {
    fetch('/api/housekeepinglog/1')
    .then(results => {
      return results.json();
    }).then(data => {
      console.log('data: ', data);
      if (data.status == 'success') {
        this.setState({ housekeeping: data.data, isLoaded: true, empty: false })
        console.log(this.state.housekeeping);
      }
    })
  }

  render() {
    const { isLoaded, housekeeping, empty } = this.state;
    if (empty) {
      return (
        <div>
        <ErrorOutlineIcon /> There is currently no housekeeping data!
        </div>
      )
    }
    return (
      <div>
        <h1>This is our GroundStation!</h1>
        {isLoaded ? (
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