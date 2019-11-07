import React, { Component } from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';
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
import Select, { components } from 'react-select';
	
const AddFlightschedule = (props) =>{
  	const selects = props.availCommands.map((command) => (
		{label: command.commandName, value: command.id, args: command.no_args}
	))

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

		          	// if flight schedule command is to be removed, dont display it anymore
		            flighschedule.op != 'remove' &&
  					  <TableBody>
            			<TableRow>
              				<TableCell>
              				  <form>
              					<Select 
              						className="basic-single"
        							classNamePrefix="select"
        							name="color"
        							options={selects} 
              						isClearable
        							placeholder="Command"
							        styles={{
							          control: (provided, state) => ({
							          	...provided,
							          	padding: '10px 10px',
							          }),
							        }}
              						onChange={(event) => props.handleAddEvent(event, 'command', idx)}
              						value={{'label': flighschedule.command.command_name, 
              										'value': flighschedule.command.command_id}}
              					/>
              				  </form>
			                </TableCell>
			                <TableCell>
			                  <form>
				                  <MuiPickersUtilsProvider utils={DateFnsUtils}>
				                    <DateTimePicker 
				                      label="Timestamp"
				                      inputVariant="outlined"
				                      value={props.thisFlightschedule[idx].timestamp}
				                      onChange={(event) => props.handleAddEvent(event, 'date', idx)}
				                    />
				                  </MuiPickersUtilsProvider>
			                  </form>
			                </TableCell>
			                <TableCell>
			                	<DeleteIcon 
                                 style={{ color: '#4bacb8'}}
                                 onClick={(event) => props.handleDeleteCommandClick(event, idx)}
                               />
			                </TableCell>
			              </TableRow>
			              <TableRow>
			              	{
			              	  flighschedule.args.map((arg, index) => (
			              	  	<TableCell>
			              	  	  <form>
			              	  		<TextField
          								label="Argument"
          								margin="normal"
          								variant="outlined"
          								defaultValue={arg.argument}
          								onChange={(event) => props.handleChangeArgument(event, idx, index)}
        							/>
        						   </form>
			              	  	</TableCell>
			              	  ))
			              	}
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