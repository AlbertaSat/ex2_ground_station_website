import React, { Component } from 'react';
import FlightSchedule from './components/FlightSchedule';
import { Route, Switch } from 'react-router-dom';

class App extends Component{
    render() {
       return (
       		<div>
       			<Switch>
       				<Route exact path='/' render={() => (
		                <div>
		                    <h1>Hello World, this is our groundstation!</h1>
		                </div>
		            )} />
       				<Route exact path='/flightschedule' component={FlightSchedule}/>
       			</Switch>
        	</div>
       )
    }

}

export default App;