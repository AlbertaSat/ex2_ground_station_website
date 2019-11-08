import React from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DialogActions from '@material-ui/core/DialogActions';

const DeleteFlightschedule = (props) =>{
	return (
		<div>
		  <Dialog 
		    open={props.open} 
		    onclose={ (event) => props.handleDeleteFlightOpenClick(event) } 
		    aria-labelledby='delete-a-flight-schedule'>
		    <DialogTitle id="delete-a-flightschedule-title">Are you sure you want to delete this?</DialogTitle>
		    <DialogContent>
		      <DialogContentText>
		        This flight schedule will be permanently deleted. 
		      </DialogContentText>
		    </DialogContent>
		    <DialogActions>
              <Button onClick={ (event) => props.deleteFlightschedule(event) } color="primary">
                Yes
             </Button>
             <Button onClick={ (event) => props.handleDeleteFlightClose(event) } color="primary">
               No
             </Button>
            </DialogActions>
		  </Dialog>
		</div>
	)
}

export default DeleteFlightschedule;