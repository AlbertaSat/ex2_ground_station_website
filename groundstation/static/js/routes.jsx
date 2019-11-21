import React from 'react';
import { Switch, Route} from 'react-router-dom';
import FlightSchedule from './components/FlightSchedule';
import Home from './components/Home';
import LiveCommands from './components/LiveCommands';
import HouseKeeping from './components/Housekeeping';
import Login from './components/Login';
import Logs from './components/ViewLogs';

const Routes = () => (
    <Switch>
        <Route exact path='/' component={Home} />
        <Route exact path='/flightschedule' component={FlightSchedule}/>
        <Route exact path='/livecommands' component={LiveCommands}/>
        <Route exact path='/housekeeping' component={HouseKeeping}/>
        <Route exact path='/login' component={Login}/>
        <Route exact path='/logs' component={Logs}/>
    </Switch>

)

export default Routes;