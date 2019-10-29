import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';

const AddFlightschedule = (props) =>{
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
		    </DialogContent>
		    <DialogActions>
              <Button onClick={ (event) => props.handleAddFlightOpenClick(event) } color="primary">
                Cancel
             </Button>
             <Button onClick={ (event) => props.handleAddFlightOpenClick(event) } color="primary">
               Submit
             </Button>
            </DialogActions>
		  </Dialog>
		</div>
	)
}

export default AddFlightschedule;