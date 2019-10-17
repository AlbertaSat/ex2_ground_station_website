import React from 'react';
import { Switch, Route} from 'react-router-dom';
import FlightSchedule from './components/FlightSchedule';
import Home from './components/Home'
import LiveCommands from './components/LiveCommands';

const Routes = () => (
    <Switch>
        <Route exact path='/' component={Home} />
        <Route exact path='/flightschedule' component={FlightSchedule}/>
        <Route exact path='/livecommands' component={LiveCommands}/>
    </Switch>

)

export default Routes;