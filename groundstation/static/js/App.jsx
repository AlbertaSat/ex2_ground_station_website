import React, { Component } from 'react';
import FlightSchedule from './components/FlightSchedule';
import Home from './components/Home'
import { Route, Switch } from 'react-router-dom';
import LiveCommands from './components/LiveCommands';

class App extends Component{
    render() {
       return (
       		<div>
       			<Switch>
       				<Route exact path='/' component={Home} />
       				<Route exact path='/flightschedule' component={FlightSchedule}/>
					<Route exact path='/livecommands' component={LiveCommands}/>
       			</Switch>
        	</div>
       )
    }

}

export default App;