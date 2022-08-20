import React, { useEffect, useRef } from 'react';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import Button from '@material-ui/core/Button';
import Table from '@material-ui/core/Table';

import moment from 'moment';
import 'moment-timezone';
import MomentUtils from '@date-io/moment';
import { DateTimePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import AddIcon from '@material-ui/icons/Add';
import Grid from '@material-ui/core/Grid';
import DialogActions from '@material-ui/core/DialogActions';

import FlightscheduleCommand from './FlightscheduleCommand';

const AddFlightschedule = (props) => {
  moment.tz.setDefault('UTC');
  return (
    <div>
      <Dialog
        open={props.open}
        onclose={(event) => props.handleAddFlightOpenClick(event)}
        aria-labelledby="add-a-flight-schedule"
        maxWidth="md"
        fullWidth
      >
        <DialogTitle id="form-add-a-flightschedule-title">
          Add/Edit Flightschedule
        </DialogTitle>
        <DialogContent style={{ minHeight: '65vh' }}>
          <DialogContentText>
            To add commands to this flight schedule, enter the command name
            followed by the timestamp, and the arguments if applicable.
          </DialogContentText>
          <Grid container spacing={1} style={{ marginTop: '2em' }}>
            <Grid item>
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
            <Grid item>
              <Button
                style={{ color: '#3f51b5', fontSize: '1rem' }}
                onClick={(event) => props.handleQueueClick(event)}
              >
                {props.status == 1 ? 'Dequeue' : 'Queue'}
              </Button>
            </Grid>
          </Grid>
          <Table aria-label="simple table">
            {props.thisFlightschedule.map(
              (flightschedule, idx) =>
                // if flight schedule command is to be removed, dont display it anymore
                flightschedule.op != 'remove' && (
                  <FlightscheduleCommand
                    flightschedule={flightschedule}
                    idx={idx}
                    key={idx}
                    executionTime={props.executionTime}
                    availCommands={props.availCommands}
                    handleChangeRepeat={props.handleChangeRepeat}
                    handleAddEvent={props.handleAddEvent}
                    handleDeleteCommandClick={props.handleDeleteCommandClick}
                    handleChangeArgument={props.handleChangeArgument}
                  />
                )
            )}
          </Table>
          <DialogContentText>
            <Button onClick={(event) => props.handleAddCommandClick(event)}>
              <AddIcon style={{ color: '#4bacb8' }} />
            </Button>
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={(event) => props.handleAddFlightOpenClick(event)}
            color="primary"
          >
            Cancel
          </Button>
          <Button
            onClick={(event) => props.addFlightschedule(event)}
            color="primary"
          >
            Submit
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
};

export default AddFlightschedule;
