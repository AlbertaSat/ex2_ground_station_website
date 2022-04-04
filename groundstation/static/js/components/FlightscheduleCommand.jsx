import React from "react";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableRow from "@material-ui/core/TableRow";
import TextField from "@material-ui/core/TextField";
import DeleteIcon from "@material-ui/icons/Delete";
import Button from "@material-ui/core/Button";
import Select from "react-select";
import { makeStyles } from "@material-ui/core/styles";

const FlightscheduleCommand = (props) => {
  const selects = props.availCommands.map((command) => ({
    label: command.command_name,
    value: command.command_id,
    args: command.num_arguments,
  }));

  const useStyles = makeStyles({
    cell: {
      borderBottom: "1px solid rgba(224, 224, 224, 1)",
      paddingTop: "0px",
    },
    argBottom: {
      borderBottom: "0px",
      paddingBottom: "0px",
    },
  });

  const classes = useStyles();

  function convertTimestamp(timestamp, executionTime) {
    if (timestamp == null || executionTime == null) {
      return null;
    } else {
      //console.log(Date.parse(timestamp) - executionTime.getTime());
      return (Date.parse(timestamp) - Date.parse(executionTime)) / 1000;
    }
  }

  return (
    <TableBody>
      <TableRow>
        <TableCell
          className={props.flightschedule.args.length > 0 ? classes.argBottom : null}
          style={{ minWidth: "18em" }}
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
                  padding: "10px 10px",
                }),
              }}
              onChange={(event) => props.handleAddEvent(event, "command", props.idx)}
              value={{
                label: props.flightschedule.command.command_name,
                value: props.flightschedule.command.command_id,
              }}
            />
          </form>
        </TableCell>
        <TableCell
          className={props.flightschedule.args.length > 0 ? classes.argBottom : null}
        >
          <form>
            <TextField
              id="outlined-basic"
              label="Delta Time"
              variant="outlined"
              type="number"
              defaultValue={convertTimestamp(
                props.flightschedule.timestamp,
                props.executionTime
              )}
              onChange={(event) => props.handleAddEvent(event, "date", props.idx)}
            />
          </form>
        </TableCell>
        <TableCell
          className={props.flightschedule.args.length > 0 ? classes.argBottom : null}
        >
          <form>
            <Button>Repeat Settings</Button>
          </form>
        </TableCell>
        <TableCell
          className={props.flightschedule.args.length > 0 ? classes.argBottom : null}
        >
          <Button
            onClick={(event) => props.handleDeleteCommandClick(event, props.idx)}
          >
            <DeleteIcon style={{ color: "#4bacb8" }} />
          </Button>
        </TableCell>
      </TableRow>
      <TableRow className={classes.cell}>
        {props.flightschedule.args.map((arg, index) => (
          <TableCell className={classes.cell}>
            <form>
              <TextField
                label={"Argument #" + (index + 1)}
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
