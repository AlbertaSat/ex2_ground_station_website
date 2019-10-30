import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import DateFnsUtils from '@date-io/date-fns';
import {
  DateTimePicker,
  MuiPickersUtilsProvider
} from "@material-ui/pickers";
import { makeStyles } from '@material-ui/core/styles';
import AddIcon from '@material-ui/icons/Add';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  popup: {
  	zIndex: 1500,
  },
});

const AddFlightschedule = (props) =>{
	console.log(props.displayDate);
  	const classes = useStyles();

	return (
		<div>
		  <Dialog 
		    open={props.open} 
		    onclose={ (event) => props.handleAddFlightOpenClick(event) } 
		    aria-labelledby='add-a-flight-schedule'>
		    <DialogTitle id="form-add-a-flightschedule-title">Add Flightschedule</DialogTitle>
		    <DialogContent>
		      <DialogContentText>
		        To add commands to this flight schedule, enter the command name followed by the timestamp.
		      </DialogContentText>
		      <Table aria-label="simple table">
		        {
		          props.thisFlightschedule.map((flighschedule, idx) => (
  					  <TableBody>
            			<TableRow>
              				<TableCell>
                 				<Autocomplete
		      						className={classes.root}
      								options={props.availCommands}
		      						getOptionLabel={option => option.commandName}
		      						style={{ width: 300 }}
		      						classes={{
		            				popup: classes.popup,
		          				}}
		          				onChange={(event) => props.handleAddEvent(event, 'command', idx)}
		      					renderInput={params => (
		        				<TextField {...params} 
		        	 				label="Command" 
		        	 				variant="outlined" 
		        	 				fullWidth 
		        	 				InputLabelProps={{
									shrink: true,
								 }}
					        	/>
					      	    )}
					    	  />
			                </TableCell>
			                <TableCell>
			                  <MuiPickersUtilsProvider utils={DateFnsUtils}>
			                    <DateTimePicker 
			                      label="Timestamp"
			                      inputVariant="outlined"
			                      value={props.thisFlightschedule[idx].timestamp}
			                      onChange={(event) => props.handleAddEvent(event, 'date', idx)}
			                    />
			                  </MuiPickersUtilsProvider>
			                </TableCell>
			              </TableRow>
			          </TableBody>
			          )	
  					)}
              </Table>
                <DialogContentText>
		          <AddIcon 
                    style={{ color: '#4bacb8'}} 
                    onClick={(event) => props.handleAddCommandClick(event)}
                  />
		      </DialogContentText>
		    </DialogContent>
		    <DialogActions>
              <Button onClick={ (event) => props.handleAddFlightOpenClick(event) } color="primary">
                Cancel
             </Button>
             <Button onClick={ (event) => props.addFlightschedule(event) } color="primary">
               Submit
             </Button>
            </DialogActions>
		  </Dialog>
		</div>
	)
}

export default AddFlightschedule;