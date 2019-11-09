import React from 'react'

import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Paper from '@material-ui/core/Paper';
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

const useStyles = makeStyles(theme => ({
    appBar: {
      position: 'relative',
    },
    title: {
      marginLeft: theme.spacing(2),
      flex: 1,
    },
  }));
  
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

const HousekeepingLogListFull = (props) => {
	if (props.empty) {
      return (
        <div>
        	<ErrorOutlineIcon /> There is currently no housekeeping data!
        </div>
      )
    }
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);
  
    const handleClickOpen = () => {
      setOpen(true);
    };
  
    const handleClose = () => {
      setOpen(false);
    };
	return (
		<div>
            <div>
                {/* <Dialog fullScreen open={open} onClose={handleClose} TransitionComponent={Transition}>
                    <AppBar className={classes.appBar}>
                    <Toolbar>
                        <IconButton edge="start" color="inherit" onClick={handleClose} aria-label="close">
                        <CloseIcon />
                        </IconButton>
                        <Typography variant="h6" className={classes.title}>
                        Sound
                        </Typography>
                        <Button autoFocus color="inherit" onClick={handleClose}>
                        save
                        </Button>
                    </Toolbar>
                    </AppBar>
                    <List>
                    <ListItem button>
                        <ListItemText primary="Phone ringtone" secondary="Titania" />
                    </ListItem>
                    <Divider />
                    <ListItem button>
                        <ListItemText primary="Default notification ringtone" secondary="Tethys" />
                    </ListItem>
                    </List>
                </Dialog> */}
            </div>

            <div>
            <Paper>
            {props.housekeeping.map(housekeeping => (
                <Table aria-label="simple table">
                    <TableBody>
                    
                        
                        <TableRow button key={housekeeping.name}>
                        <TableCell onClick={handleClickOpen} component="th" scope="row" style={tableColor(housekeeping.satellite_mode)}>
                            {housekeeping.last_beacon_time}
                        </TableCell>
                        </TableRow>
                    </TableBody>
                    <Dialog fullScreen open={open} onClose={handleClose} TransitionComponent={Transition}>
                        <AppBar>
                        <Toolbar>
                            <IconButton edge="start" color="inherit" onClick={handleClose} aria-label="close">
                            <CloseIcon />
                            </IconButton>
                            <Typography variant="h6" className={classes.title}>
                            {housekeeping.last_beacon_time}
                            </Typography>
                        </Toolbar>
                        </AppBar>
                        <List>
                        <ListItem >
                            <ListItemText primary="ID" secondary={housekeeping.id} />
                        </ListItem>
                        <Divider />
                        <ListItem >
                            <ListItemText primary="Satellite Mode" secondary={housekeeping.satellite_mode} />
                        </ListItem>
                        <ListItem >
                            <ListItemText primary="Battery Voltage" secondary={housekeeping.battery_voltage} />
                        </ListItem>
                        <Divider />
                        <ListItem >
                            <ListItemText primary="Current In" secondary={housekeeping.current_in} />
                        </ListItem>
                        <Divider />
                        <ListItem >
                            <ListItemText primary="Current Out" secondary={housekeeping.current_out} />
                        </ListItem>
                        {/*}
                        <ListItem >
                            <ListItemText primary="Watchdog 1" secondary={6600} />
                        </ListItem>*/}

                        <ListItem>
                          <Table aria-label="simple table">
                            <TableHead>
                              <TableRow>
                                <TableCell 
                                    style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Power Channel
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Enabled
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Current
                                </TableCell>
                              </TableRow>
                            </TableHead>
                            {/*
                            {flightschedule.commands.map(commands => (
                              <TableBody>
                                  <TableRow>
                                    <TableCell component ="th" scope="row">
                                      {commands.flightschedule_command_id}
                                    </TableCell>
                                    <TableCell align="right">{commands.command.command_name}</TableCell>
                                    <TableCell align="right">{commands.timestamp}</TableCell>
                                  </TableRow>
                              </TableBody>
                            ))}
                            */}
                          </Table>
                        </ListItem>

                        <ListItem>
                          <Table aria-label="simple table">
                            <TableHead>
                              <TableRow>
                                <TableCell 
                                    style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Watchdog 1
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Watchdog 2
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Watchdog 3
                                </TableCell>
                              </TableRow>
                            </TableHead>
                            {/*
                            {flightschedule.commands.map(commands => (
                              <TableBody>
                                  <TableRow>
                                    <TableCell component ="th" scope="row">
                                      {commands.flightschedule_command_id}
                                    </TableCell>
                                    <TableCell align="right">{commands.command.command_name}</TableCell>
                                    <TableCell align="right">{commands.timestamp}</TableCell>
                                  </TableRow>
                              </TableBody>
                            ))}
                            */}
                          </Table>
                        </ListItem>

                        <ListItem>
                          <Table aria-label="simple table">
                            <TableHead>
                              <TableRow>
                                <TableCell 
                                    style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Solar Panel
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Current
                                </TableCell>
                              </TableRow>
                            </TableHead>
                            {/*
                            {flightschedule.commands.map(commands => (
                              <TableBody>
                                  <TableRow>
                                    <TableCell component ="th" scope="row">
                                      {commands.flightschedule_command_id}
                                    </TableCell>
                                    <TableCell align="right">{commands.command.command_name}</TableCell>
                                    <TableCell align="right">{commands.timestamp}</TableCell>
                                  </TableRow>
                              </TableBody>
                            ))}
                            */}
                          </Table>
                        </ListItem>

                        <ListItem>
                          <Table aria-label="simple table">
                            <TableHead>
                              <TableRow>
                                <TableCell 
                                    style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Temp 1
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Temp 2
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Temp 3
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Temp 4
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Temp 5
                                </TableCell>
                                <TableCell 
                                  align="left"
                                  style={{backgroundColor: '#fff', color: '#000', paddingTop: '8px', paddingBottom: '8px'}}>
                                    Temp 6
                                </TableCell>
                              </TableRow>
                            </TableHead>
                            {/*
                            {flightschedule.commands.map(commands => (
                              <TableBody>
                                  <TableRow>
                                    <TableCell component ="th" scope="row">
                                      {commands.flightschedule_command_id}
                                    </TableCell>
                                    <TableCell align="right">{commands.command.command_name}</TableCell>
                                    <TableCell align="right">{commands.timestamp}</TableCell>
                                  </TableRow>
                              </TableBody>
                            ))}
                            */}
                          </Table>
                        </ListItem>
                        

                        </List>
                    </Dialog>
                </Table>
                
                ))}
            </Paper>
            </div>
		</div>
	)
};
export default HousekeepingLogListFull;