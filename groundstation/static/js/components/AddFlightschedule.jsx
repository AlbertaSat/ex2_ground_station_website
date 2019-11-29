import React, { useEffect, useRef } from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import DeleteIcon from '@material-ui/icons/Delete';
import DialogActions from '@material-ui/core/DialogActions';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import moment from "moment";
import 'moment-timezone';
import MomentUtils from '@date-io/moment';
import {
  DateTimePicker,
  MuiPickersUtilsProvider
} from "@material-ui/pickers";
import { makeStyles } from '@material-ui/core/styles';
import AddIcon from '@material-ui/icons/Add';
import Select from 'react-select';
import Grid from '@material-ui/core/Grid';
	
const AddFlightschedule = (props) =>{
  	const selects = props.availCommands.map((command) => (
		{label: command.command_name, value: command.command_id, args: command.num_arguments}
	))

	const useStyles = makeStyles({
	  cell: {
	  	borderBottom: '1px solid rgba(224, 224, 224, 1)',
	  	paddingTop: '0px',
	  },
	  argBottom: {
	  	borderBottom: '0px',
	  	paddingBottom: '0px',
	  },
	});

	const classes = useStyles();

	function convertTimestamp(timestamp, executionTime){
		if(timestamp == null || executionTime == null){
			return null
		}else{
			//console.log(Date.parse(timestamp) - executionTime.getTime());
			return (Date.parse(timestamp) - Date.parse(executionTime)) / 1000;
		}
	}

	moment.tz.setDefault("UTC")

	return (
		<div>
		  <Dialog 
		    open={props.open} 
		    onclose={ (event) => props.handleAddFlightOpenClick(event) } 
		    aria-labelledby='add-a-flight-schedule'>
		    <DialogTitle id="form-add-a-flightschedule-title">
		    	Add/Edit Flightschedule
		    </DialogTitle>
		    <DialogContent>
		      <DialogContentText>
		        To add commands to this flight schedule, enter the command name followed by the timestamp, 
		        and the arguments if applicable.
		      </DialogContentText>
		      <Grid container spacing={2} style={{marginTop: '2em'}}>
		      	<Grid item xs={5}>
	              <form>
					  <MuiPickersUtilsProvider moment={moment} utils={MomentUtils}>
              <DateTimePicker 
                  label="Execution Time"
                  inputVariant="outlined"
                  value={props.executionTime}
                  onChange={(event) => props.handleExecutionTimeChange(event)}
              />
					  </MuiPickersUtilsProvider>
				  </form>
				</Grid>
          <Grid item xs={7}>
            <Button style={{color: '#3f51b5', fontSize: '1rem'}}
              onClick={ (event) => props.handleQueueClick(event) }
            >
                  {(props.status == 1)? 'Dequeue' : 'Queue' }
              </Button>
          </Grid>
			  </Grid>
		      <Table aria-label="simple table">
		        {
		          props.thisFlightschedule.map((flighschedule, idx) => (

		          	// if flight schedule command is to be removed, dont display it anymore
		            flighschedule.op != 'remove' &&
  					  <TableBody>
                <TableRow>
                    <TableCell className={(flighschedule.args.length > 0)? classes.argBottom : null }
                          style={{minWidth: '18em'}}
                    >
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
                    <TableCell className={(flighschedule.args.length > 0)? classes.argBottom : null}>
                      <form>
                        <TextField
                    id="outlined-basic"
                    label="Delta Time"
                    variant="outlined"
                    type="number"
                    defaultValue={convertTimestamp(flighschedule.timestamp, props.executionTime)}
                    onChange={(event) => props.handleAddEvent(event, 'date', idx)}
                  />
                      </form>
                    </TableCell>
                    <TableCell className={(flighschedule.args.length > 0)? classes.argBottom : null }>
                      <Button
                        onClick={(event) => props.handleDeleteCommandClick(event, idx)}
                      >
                        <DeleteIcon 
                                  style={{ color: '#4bacb8'}}
                                />
                            </Button>
                    </TableCell>
                  </TableRow>
                  <TableRow className={classes.cell}>
                    {
                      flighschedule.args.map((arg, index) => (
                        <TableCell className={classes.cell}>
                          <form>
                          <TextField
                        label={"Argument #" + (index + 1)}
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
			          ))}
              </Table>
                <DialogContentText>
                	<Button
                		onClick={(event) => props.handleAddCommandClick(event)}
                	>
			          <AddIcon 
	                    style={{ color: '#4bacb8'}} 
	                  />
	                </Button>
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