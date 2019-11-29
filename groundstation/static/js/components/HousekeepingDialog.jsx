import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Dialog from '@material-ui/core/Dialog';
import ListItemText from '@material-ui/core/ListItemText';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import IconButton from '@material-ui/core/IconButton';
import CloseIcon from '@material-ui/icons/Close';
import Typography from '@material-ui/core/Typography';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
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
const HousekeepingDialog = (props) => {
    const classes = useStyles();
    return (
          /* Display a HK log in a full screen dialog */
            <Dialog fullScreen open={props.open} onClose={() => props.handleClose()} TransitionComponent={Transition}>
            <AppBar>
            <Toolbar>
                <IconButton edge="start" color="inherit" onClick={() => props.handleClose()} aria-label="close">
                <CloseIcon />
                </IconButton>
                <Typography variant="h6" className={classes.title}>
                {props.housekeeping.last_beacon_time}
                </Typography>
            </Toolbar>
            </AppBar>

            {/* HK log data being displayed */}
            <List>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="ID" secondary={props.housekeeping.id} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Satellite Mode" secondary={props.housekeeping.satellite_mode} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Watchdog 1" secondary={props.housekeeping.watchdog_1} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Watchdog 2" secondary={props.housekeeping.watchdog_2} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Watchdog 3" secondary={props.housekeeping.watchdog_3} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="MCU Resets" secondary={props.housekeeping.no_MCU_resets} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Battery Voltage" secondary={props.housekeeping.battery_voltage} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Current In" secondary={props.housekeeping.current_in} />
            </ListItem>
            <ListItem >
                <ListItemText classes={{root: classes.customListItemText}} primary="Current Out" secondary={props.housekeeping.current_out} />
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
                    {props.housekeeping.channels.map(channel => (
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
                    <TableCell align="left">{props.housekeeping.panel_1_current}</TableCell>
                    </TableRow>
                    <TableRow key={2}>
                    <TableCell component="th" scope="row">{2}</TableCell>
                    <TableCell align="left">{props.housekeeping.panel_2_current}</TableCell>
                    </TableRow>
                    <TableRow key={3}>
                    <TableCell component="th" scope="row">{3}</TableCell>
                    <TableCell align="left">{props.housekeeping.panel_3_current}</TableCell>
                    </TableRow>
                    <TableRow key={4}>
                    <TableCell component="th" scope="row">{4}</TableCell>
                    <TableCell align="left">{props.housekeeping.panel_4_current}</TableCell>
                    </TableRow>
                    <TableRow key={5}>
                    <TableCell component="th" scope="row">{5}</TableCell>
                    <TableCell align="left">{props.housekeeping.panel_5_current}</TableCell>
                    </TableRow>
                    <TableRow key={6}>
                    <TableCell component="th" scope="row">{6}</TableCell>
                    <TableCell align="left">{props.housekeeping.panel_6_current}</TableCell>
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
                    <TableCell align="left">{props.housekeeping.temp_1}</TableCell>
                    </TableRow>
                    <TableRow key={2}>
                    <TableCell component="th" scope="row">{2}</TableCell>
                    <TableCell align="left">{props.housekeeping.temp_2}</TableCell>
                    </TableRow>
                    <TableRow key={3}>
                    <TableCell component="th" scope="row">{3}</TableCell>
                    <TableCell align="left">{props.housekeeping.temp_3}</TableCell>
                    </TableRow>
                    <TableRow key={4}>
                    <TableCell component="th" scope="row">{4}</TableCell>
                    <TableCell align="left">{props.housekeeping.temp_4}</TableCell>
                    </TableRow>
                    <TableRow key={5}>
                    <TableCell component="th" scope="row">{5}</TableCell>
                    <TableCell align="left">{props.housekeeping.temp_5}</TableCell>
                    </TableRow>
                    <TableRow key={6}>
                    <TableCell component="th" scope="row">{6}</TableCell>
                    <TableCell align="left">{props.housekeeping.temp_6}</TableCell>
                    </TableRow>
                </TableBody>
                </Table>
            </ListItem><br></br>

            </List>
        </Dialog>
    )
}

export default HousekeepingDialog;