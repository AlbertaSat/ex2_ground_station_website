import React, { useEffect, useState } from 'react';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableRow from '@material-ui/core/TableRow';
import TextField from '@material-ui/core/TextField';
import DeleteIcon from '@material-ui/icons/Delete';
import Button from '@material-ui/core/Button';
import Select from 'react-select';
import Popover from '@material-ui/core/Popover';
import { makeStyles } from '@material-ui/core/styles';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

export const REPEAT_LABELS = {
  repeat_ms: 'Millisecond',
  repeat_sec: 'Second',
  repeat_min: 'Minute',
  repeat_hr: 'Hour',
  repeat_day: 'Day',
  repeat_month: 'Month',
  repeat_year: 'Year'
};

const FlightscheduleCommand = (props) => {
  const [anchorEl, setAnchorEl] = useState(null);
  const [repeats, setRepeats] = useState(props.flightschedule.repeats);

  /**
   * Update command repeat fields
   */
  useEffect(() => {
    setRepeats(props.flightschedule.repeats);
  }, [props.flightschedule.repeats]);

  /**
   * Calculates the offset of a command from the base execution time
   * @param {string} timestamp The timestamp of command execution
   * @param {string} executionTime The base timestamp of the flightschedule
   * @returns The respective second and millisecond offset of the command
   *     from the base timestamp.
   */
  const defaultOffset = (timestamp, executionTime) => {
    if (timestamp == null || executionTime == null) {
      return {
        seconds: null,
        milliseconds: null
      };
    } else {
      let difference = Date.parse(timestamp) - Date.parse(executionTime);
      return {
        seconds: Math.floor(difference / 1000),
        milliseconds: difference % 1000
      };
    }
  };

  const [secondOffset, setSecondOffset] = useState(
    defaultOffset(props.flightschedule.timestamp, props.executionTime)[
      'seconds'
    ]
  );
  const [msOffset, setMsOffset] = useState(
    defaultOffset(props.flightschedule.timestamp, props.executionTime)[
      'milliseconds'
    ]
  );

  /**
   * Updates the second/millisecond offset of the command
   */
  useEffect(() => {
    if (
      props.executionTime != null &&
      !isNaN(secondOffset) &&
      !isNaN(msOffset)
    ) {
      console.log(secondOffset);
      console.log(msOffset);
      const offsetEvent = {
        target: {
          value:
            (parseInt(secondOffset) || 0) * 1000 + (parseInt(msOffset) || 0)
        }
      };
      props.handleAddEvent(offsetEvent, 'offset', props.idx);
    }
  }, [secondOffset, msOffset]);

  const handleOpenRepeat = (e) => {
    setAnchorEl(e.currentTarget);
  };

  const handleCloseRepeat = (e) => {
    setAnchorEl(null);
  };

  const updateRepeat = (event, field, value, idx) => {
    setRepeats((old) => {
      const newRepeat = { ...old, [field]: value };
      // If 'repeat_min' is checked, then so must 'repeat_hr
      if (field === 'repeat_min' && value) newRepeat['repeat_hr'] = true;
      props.handleChangeRepeat(event, idx, newRepeat);
      return newRepeat;
    });
  };

  const useStyles = makeStyles({
    cell: {
      borderBottom: '1px solid rgba(224, 224, 224, 1)',
      paddingTop: '0px'
    },
    argBottom: {
      borderBottom: '0px',
      paddingBottom: '0px'
    }
  });

  const classes = useStyles();

  const popoverOpen = Boolean(anchorEl);

  return (
    <TableBody>
      <TableRow>
        <TableCell
          className={
            props.flightschedule.args.length > 0 ? classes.argBottom : null
          }
          style={{ minWidth: '18em' }}
        >
          <form>
            <Select
              className="basic-single"
              classNamePrefix="select"
              name="color"
              options={props.availCommands}
              isClearable
              placeholder="Command"
              styles={{
                control: (provided, state) => ({
                  ...provided,
                  padding: '10px 10px'
                })
              }}
              onChange={(event) =>
                props.handleAddEvent(event, 'command', props.idx)
              }
              value={{
                label: props.flightschedule.command.command_name,
                value: props.flightschedule.command.command_id
              }}
            />
          </form>
        </TableCell>
        <TableCell
          className={
            props.flightschedule.args.length > 0 ? classes.argBottom : null
          }
        >
          <form>
            <TextField
              id="outlined-basic"
              label="Second Offset"
              variant="outlined"
              type="number"
              value={secondOffset}
              onChange={(event) => setSecondOffset(event.target.value)}
            />
          </form>
          <form>
            <TextField
              id="outlined-basic"
              label="Millisecond Offset"
              variant="outlined"
              type="number"
              value={msOffset}
              onChange={(event) => setMsOffset(event.target.value)}
            />
          </form>
        </TableCell>
        <TableCell
          className={
            props.flightschedule.args.length > 0 ? classes.argBottom : null
          }
        >
          <form>
            <Button onClick={handleOpenRepeat}>Repeat Every...</Button>
            <Popover
              open={popoverOpen}
              anchorEl={anchorEl}
              onClose={handleCloseRepeat}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'center'
              }}
              transformOrigin={{
                vertical: 'top',
                horizontal: 'center'
              }}
            >
              <FormGroup>
                {repeats &&
                  Object.keys(repeats).map((field, idx) => (
                    <FormControlLabel
                      control={
                        <Checkbox
                          // repeat_hr MUST be checked if
                          // repeat_min is also checked
                          checked={
                            field === 'repeat_hr'
                              ? repeats['repeat_min'] || repeats[field]
                              : repeats[field]
                          }
                          disabled={
                            field === 'repeat_hr'
                              ? repeats['repeat_min']
                              : false
                          }
                          onChange={(event) => {
                            updateRepeat(
                              event,
                              field,
                              event.target.checked,
                              props.idx
                            );
                          }}
                        />
                      }
                      label={REPEAT_LABELS[field]}
                      key={idx}
                    />
                  ))}
              </FormGroup>
            </Popover>
          </form>
        </TableCell>
        <TableCell
          className={
            props.flightschedule.args.length > 0 ? classes.argBottom : null
          }
        >
          <Button
            onClick={(event) =>
              props.handleDeleteCommandClick(event, props.idx)
            }
          >
            <DeleteIcon style={{ color: '#4bacb8' }} />
          </Button>
        </TableCell>
      </TableRow>
      <TableRow className={classes.cell}>
        {props.flightschedule.args.map((arg, index) => (
          <TableCell className={classes.cell} key={index}>
            <form>
              <TextField
                label={'Argument #' + (index + 1)}
                margin="normal"
                variant="outlined"
                defaultValue={arg.argument}
                onChange={(event) =>
                  props.handleChangeArgument(event, props.idx, index)
                }
              />
            </form>
          </TableCell>
        ))}
      </TableRow>
    </TableBody>
  );
};

export default FlightscheduleCommand;
