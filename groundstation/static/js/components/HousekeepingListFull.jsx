import React, { Component } from 'react';

import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Paper from '@material-ui/core/Paper';
import { withStyles } from '@material-ui/core/styles';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import WarningIcon from '@material-ui/icons/Warning';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';
import Dialog from '@material-ui/core/Dialog';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Slide from '@material-ui/core/Slide';
import LinearProgress from '@material-ui/core/LinearProgress';
import HousekeepingDialog from './HousekeepingDialog';

const styles = {
  root: {
    width: '100%',
  },
  appBar: {
    position: 'relative',
  },
  title: {
    marginLeft: '10px',
    flex: 1,
  },
  paper: {
    marginTop: '10px',
    width: '100%',
    overflowX: 'auto',
    marginBottom: '10px',
  },
  table: {
    minWidth: 650,
  },
  customListItemText: {
    display: 'flex',
    alignItems: 'baseline',
    justifyContent: 'space-between',
    maxWidth: '78%',
  },
};

const Transition = React.forwardRef(function Transition(props, ref) {
  return <Slide direction="up" ref={ref} {...props} />;
});

function modeIcon(status){
	if(status == "Passive" || status == "Active Mission"){
		return <CheckCircleIcon style={{ fill: '#479b4e' }}/>
	}else{
		return <WarningIcon style={{ fill: '#721c24' }}/>
	}
}

function tableColor(status){
  if(status == "Passive" || status == "Active Mission"){
    return {borderLeft: 'solid 8px #479b4e'}
  }else{
    return {borderLeft: 'solid 8px #721c24'}
  }
  //#c48b16 Warning
  //#f44336 Danger
}
// class FlightSchedule extends Component{
// const HousekeepingLogListFull = (props) => {
class HousekeepingLogListFull extends Component {
  constructor(){
		super();
		this.state = {
      open: false,
      selectedHousekeeping: {
        id: null,
        satelliteMode: null,
        batteryVoltage: null,
        currentIn: null,
        currentOut: null,
        lastBeaconTime: null,
        noMCUResets: null,
        channels: []
      }
    },
    this.handleOpenClick = this.handleOpenClick.bind(this)
    this.handleClose = this.handleClose.bind(this)
	}
  componentDidMount() {
    console.log(this.props);
    if (this.props.isLoading) {
      return (
        <div>
          <LinearProgress />
        </div>
      )
    }
    if (this.props.empty && !this.props.isLoading) {
      return (
        <div>
          <ErrorOutlineIcon /> There is currently no housekeeping data!
        </div>
      )
    }
  }

  handleOpenClick(housekeeping) {
    console.log(housekeeping)
    this.setState({
      open: !this.state.open,
      selectedHousekeeping: housekeeping
    })
  }

  handleClose() {
    this.setState({
      open: false
    })
  }
  

  render() {
    const { classes } = this.props;
	return (
		<div className={classes.root}>
      <div>
      <Paper className={classes.paper}>
        {/* (event) => { func1(event); func2();} */}
        {this.props.housekeeping.map(housekeeping => (
          <Table aria-label="simple table">
              <TableBody>
                <TableRow button key={housekeeping.name} onClick={() => this.handleOpenClick(housekeeping)}>
                <TableCell width="15%" component="th" scope="row" style={tableColor(housekeeping.satellite_mode)}>
                  {housekeeping.last_beacon_time}
                </TableCell>
                <TableCell component="th" scope="row">
                  {housekeeping.satellite_mode}
                </TableCell>
                </TableRow>
              </TableBody>
          </Table>

          ))}
          <HousekeepingDialog 
          housekeeping={this.state.selectedHousekeeping}
          open={this.state.open}
          handleClose={this.handleClose}
          />
      </Paper>
      </div>

		</div>
	)}
}
export default withStyles(styles)(HousekeepingLogListFull);
