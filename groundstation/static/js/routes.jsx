import React from 'react';
import { Switch, Route} from 'react-router-dom';
import FlightSchedule from './components/FlightSchedule';
import Home from './components/Home';
import LiveCommands from './components/LiveCommands';
import HouseKeeping from './components/Housekeeping';
import Login from './components/Login';
import Logout from './components/Logout';
import Logs from './components/ViewLogs';
import Help from './components/Help';

const Routes = () => (
    <Switch>
        <Route exact path='/' component={Home} />
        <Route exact path='/flightschedule' component={FlightSchedule}/>
        <Route exact path='/livecommands' component={LiveCommands}/>
        <Route exact path='/housekeeping' component={HouseKeeping}/>
        <Route exact path='/login' component={Login}/>
        <Route exact path='/logout' component={Logout}/>
        <Route exact path='/logs' component={Logs}/>
        <Route exact path='/help' component={Help}/>
    </Switch>

)

export default Routes;