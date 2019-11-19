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
  root: {
    width: '100%',
  },
  appBar: {
    position: 'relative',
  },
  title: {
    marginLeft: theme.spacing(2),
    flex: 1,
  },
  paper: {
    marginTop: theme.spacing(3),
    width: '100%',
    overflowX: 'auto',
    marginBottom: theme.spacing(2),
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
		<div className={classes.root}>

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
      <Paper className={classes.paper}>
        {props.housekeeping.map(housekeeping => (
          <Table aria-label="simple table">
              <TableBody>
                <TableRow button key={housekeeping.name}>
                <TableCell onClick={handleClickOpen} component="th" scope="row" style={tableColor(housekeeping.satellite_mode)}>
                  {housekeeping.last_beacon_time}
                </TableCell>
                </TableRow>
              </TableBody>

              {/* Display a HK log in a full screen dialog */}
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

                  {/* HK log data being displayed */}
                  <List>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="ID" secondary={housekeeping.id} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Satellite Mode" secondary={housekeeping.satellite_mode} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Watchdog 1" secondary={housekeeping.watchdog_1} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Watchdog 2" secondary={housekeeping.watchdog_2} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Watchdog 3" secondary={housekeeping.watchdog_3} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="MCU Resets" secondary={housekeeping.no_MCU_resets} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Battery Voltage" secondary={housekeeping.battery_voltage} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Current In" secondary={housekeeping.current_in} />
                  </ListItem>
                  <ListItem >
                    <ListItemText classes={{root: classes.customListItemText}} primary="Current Out" secondary={housekeeping.current_out} />
                  </ListItem>
                  <br></br>

                  {/* Power Channels table */}
                  <ListItem>
                    <Table className={classes.table} size="small" aria-label="dense table">
                      <TableHead>
                        <TableRow>
                          <TableCell width="40%">Power Channel</TableCell>
                          <TableCell width="30%" align="left">Enabled</TableCell>
                          <TableCell width="30%" align="left">Current (mA)</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        {housekeeping.channels.map(channel => (
                          <TableRow key={channel.channel_no}>
                            <TableCell component="th" scope="row">
                              {channel.channel_no}
                            </TableCell>
                            <TableCell align="left">{channel.enabled.toString()}</TableCell>
                            <TableCell align="left">{channel.current}</TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </ListItem><br></br>

                  {/* Solar Panels table */}
                  <ListItem>
                    <Table className={classes.table} size="small" aria-label="dense table">
                      <TableHead>
                        <TableRow>
                          <TableCell width="70%">Solar Panel</TableCell>
                          <TableCell width="30%" align="left">Current (mA)</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow key={1}>
                          <TableCell component="th" scope="row" >{1}</TableCell>
                          <TableCell align="left">{housekeeping.panel_1_current}</TableCell>
                        </TableRow>
                        <TableRow key={2}>
                          <TableCell component="th" scope="row">{2}</TableCell>
                          <TableCell align="left">{housekeeping.panel_2_current}</TableCell>
                        </TableRow>
                        <TableRow key={3}>
                          <TableCell component="th" scope="row">{3}</TableCell>
                          <TableCell align="left">{housekeeping.panel_3_current}</TableCell>
                        </TableRow>
                        <TableRow key={4}>
                          <TableCell component="th" scope="row">{4}</TableCell>
                          <TableCell align="left">{housekeeping.panel_4_current}</TableCell>
                        </TableRow>
                        <TableRow key={5}>
                          <TableCell component="th" scope="row">{5}</TableCell>
                          <TableCell align="left">{housekeeping.panel_5_current}</TableCell>
                        </TableRow>
                        <TableRow key={6}>
                          <TableCell component="th" scope="row">{6}</TableCell>
                          <TableCell align="left">{housekeeping.panel_6_current}</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </ListItem><br></br>

                  {/* Temperatures table */}
                  <ListItem>
                    <Table className={classes.table} size="small" aria-label="dense table">
                      <TableHead>
                        <TableRow>
                          <TableCell width="70%">Temperature Location</TableCell>
                          <TableCell width="30%" align="left">Temperature (°C)</TableCell>
                        </TableRow>
                      </TableHead>
                      <TableBody>
                        <TableRow key={1}>
                          <TableCell component="th" scope="row">{1}</TableCell>
                          <TableCell align="left">{housekeeping.temp_1}</TableCell>
                        </TableRow>
                        <TableRow key={2}>
                          <TableCell component="th" scope="row">{2}</TableCell>
                          <TableCell align="left">{housekeeping.temp_2}</TableCell>
                        </TableRow>
                        <TableRow key={3}>
                          <TableCell component="th" scope="row">{3}</TableCell>
                          <TableCell align="left">{housekeeping.temp_3}</TableCell>
                        </TableRow>
                        <TableRow key={4}>
                          <TableCell component="th" scope="row">{4}</TableCell>
                          <TableCell align="left">{housekeeping.temp_4}</TableCell>
                        </TableRow>
                        <TableRow key={5}>
                          <TableCell component="th" scope="row">{5}</TableCell>
                          <TableCell align="left">{housekeeping.temp_5}</TableCell>
                        </TableRow>
                        <TableRow key={6}>
                          <TableCell component="th" scope="row">{6}</TableCell>
                          <TableCell align="left">{housekeeping.temp_6}</TableCell>
                        </TableRow>
                      </TableBody>
                    </Table>
                  </ListItem><br></br>

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
