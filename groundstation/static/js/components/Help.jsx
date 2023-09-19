import React, { useEffect, useState } from 'react';
import moment from 'moment';
import 'moment-timezone';
import MomentUtils from '@date-io/moment';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import AddIcon from '@material-ui/icons/Add';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import { DateTimePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import TextField from '@material-ui/core/TextField';
import Fab from '@material-ui/core/Fab';
import { REPEAT_LABELS } from './FlightscheduleCommand';
import Popover from '@material-ui/core/Popover';
import FormGroup from '@material-ui/core/FormGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';

const Help = () => {
  moment.tz.setDefault('UTC');
  const [commands, setCommands] = useState([]);
  const [repeatAnchor, setRepeatAnchor] = useState(null);
  const [dummyRepeats, setDummyRepeats] = useState({
    repeat_ms: false,
    repeat_sec: false,
    repeat_min: false,
    repeat_hr: false,
    repeat_day: false,
    repeat_month: false,
    repeat_year: false
  });

  useEffect(() => {
    moment.tz.setDefault('UTC');
    fetch('./api/telecommands', {
      headers: {
        Authorization: 'Bearer ' + sessionStorage.getItem('auth_token')
      }
    })
      .then((results) => {
        return results.json();
      })
      .then((data) => {
        if (data.status === 'success') setCommands(data.data.telecommands);
        else console.error('Error loading telecommands');
      });
  }, []);

  const handleOpenRepeat = (e) => {
    setRepeatAnchor(e.currentTarget);
  };

  const handleCloseRepeat = (e) => {
    setRepeatAnchor(null);
  };

  const updateRepeat = (event, field, value) => {
    setDummyRepeats((old) => {
      const newRepeat = { ...old, [field]: value };
      if (field === 'repeat_min' && value) newRepeat['repeat_hr'] = true;
      return newRepeat;
    });
  };

  const popoverOpen = Boolean(repeatAnchor);

  return (
    <div>
      <Typography variant="h4" style={{ color: '#28324C' }}>
        Help Page
      </Typography>
      <Paper
        className="Flight Schedule"
        style={{ marginTop: '20px', marginBottom: '20px' }}
      >
        <Typography variant="h5" style={{ padding: '10px' }}>
          Flight Schedule
        </Typography>
        <Typography
          variant="body1"
          style={{ paddingLeft: '20px', paddingRight: '20px' }}
        >
          The Flight Schedule page allows you to build, edit, and queue flight
          schedules.
        </Typography>
        <Typography
          variant="body1"
          style={{ paddingLeft: '20px', paddingRight: '20px' }}
        >
          Flight Schedules are colour coded based on their status: Grey is a
          draft flight schedule,
          <Paper
            style={{
              marginLeft: '20px',
              borderLeft: 'solid 8px #A9A9A9',
              marginBottom: '10px',
              marginTop: '10px',
              marginRight: '20px'
            }}
          >
            <div style={{ fontWeight: 'bold', marginLeft: '4px' }}>
              Draft Flight Schedule
            </div>
          </Paper>
          blue is the currently queued flight schedule,
          <Paper
            style={{
              marginLeft: '20px',
              borderLeft: 'solid 8px #4bacb8',
              marginBottom: '10px',
              marginTop: '10px',
              marginRight: '20px'
            }}
          >
            <div style={{ fontWeight: 'bold', marginLeft: '4px' }}>
              Queued Flight Schedule
            </div>
          </Paper>
          and green means that the flight schedule has already been uploaded to
          the satellite.
          <Paper
            style={{
              marginLeft: '20px',
              borderLeft: 'solid 8px #479b4e',
              marginBottom: '10px',
              marginTop: '10px',
              marginRight: '20px'
            }}
          >
            <div style={{ fontWeight: 'bold', marginLeft: '4px' }}>
              Uploaded Flight Schedule
            </div>
          </Paper>
          In the event that an upload failed, the flight schedule will be
          highlighted red and an{' '}
          <a
            href="https://github.com/AlbertaSat/ex2_ground_station_software/blob/master/schedule_error_codes.txt"
            target="_blank"
            rel="noreferrer"
          >
            error code
          </a>{' '}
          will be displayed below it. The flight schedule would be put back into
          draft mode so you can edit it.
          <Paper
            style={{
              marginLeft: '20px',
              borderLeft: 'solid 8px #fc3c35',
              marginBottom: '10px',
              marginTop: '10px',
              marginRight: '20px'
            }}
          >
            <div style={{ fontWeight: 'bold', marginLeft: '4px' }}>
              Failed Flight Schedule
            </div>
            <div
              style={{
                fontSize: '14px',
                color: '#fc3c35',
                marginLeft: '4px'
              }}
            >
              UPLOAD FAILED | Error Code: 1
            </div>
          </Paper>
          Only one flight schedule may be queued at a time and a queued schedule
          will be automatically uploaded to the satellite during the next
          passover. It is also possible to upload a schedule manually via the
          live commands.
        </Typography>
        <Typography
          variant="body1"
          style={{ paddingLeft: '20px', paddingRight: '20px' }}
        >
          A Flight schedule can be edited using{' '}
          <EditIcon style={{ color: '#4bacb8' }} />, or deleted with{' '}
          <DeleteIcon style={{ color: '#4bacb8' }} />, and you can add a new
          flight schedule using:
          <Fab>
            <AddIcon style={{ color: '#4bacb8', fontSize: '2rem' }} />
          </Fab>
        </Typography>
        <Typography variant="h6" style={{ paddingLeft: '20px' }}>
          Editing/Creating a Flight Schedule:
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingBottom: '10px',
            paddingRight: '20px'
          }}
        >
          When editing/creating a flight schedule, you first set an execution
          time (UTC) in the execution time box:
          <form style={{ paddingTop: '10px' }}>
            <MuiPickersUtilsProvider utils={MomentUtils}>
              <DateTimePicker label="Execution Time" inputVariant="outlined" />
            </MuiPickersUtilsProvider>
          </form>
          This is the time at which the set of commands will be executed. You
          can add commands using the <AddIcon style={{ color: '#4bacb8' }} />{' '}
          icon which allows you to select from the list of available commands.
          Then, you fill in the relevant arguments based on the command and set
          a delay (in seconds and milliseconds) in when you want the command to
          execute after the execution time.
          <form>
            <TextField
              id="outlined-basic"
              label="Second Offset"
              variant="outlined"
              type="number"
            />
            <TextField
              id="outlined-basic"
              label="Millisecond Offset"
              variant="outlined"
              type="number"
            />
          </form>
          For each command, you can also specify the regularity of each command,
          if you want it to repeat at certain intervals. (eg. repeat every
          second, minute, hour, etc.). Note that if a command is set to repeat
          every minute, it will also repeat every hour.
          <form>
            <Button onClick={handleOpenRepeat}>Repeat Every...</Button>
            <Popover
              open={popoverOpen}
              anchorEl={repeatAnchor}
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
                {Object.keys(dummyRepeats).map((field, idx) => (
                  <FormControlLabel
                    control={
                      <Checkbox
                        // repeat_hr MUST be checked if
                        // repeat_min is also checked
                        checked={
                          field === 'repeat_hr'
                            ? dummyRepeats['repeat_min'] || dummyRepeats[field]
                            : dummyRepeats[field]
                        }
                        disabled={
                          field === 'repeat_hr'
                            ? dummyRepeats['repeat_min']
                            : false
                        }
                        onChange={(event) => {
                          updateRepeat(event, field, event.target.checked);
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
          You can also delete any command in the flight schedule using the{' '}
          <DeleteIcon style={{ color: '#4bacb8' }} /> for that command.
        </Typography>
      </Paper>
      <Paper className="Housekeeping" style={{ marginBottom: '20px' }}>
        <Typography variant="h5" style={{ padding: '10px' }}>
          Housekeeping
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingRight: '20px',
            paddingBottom: '10px'
          }}
        >
          Use Housekeeping to view the status and health of the satellite. Each
          housekeeping log contains information about the satellite, such as the
          watchdog timers, as well as voltages. A housekeeping file with a green
          tag means that the housekeeping log is healthy and detected no issues,
          <Paper
            style={{
              marginLeft: '20px',
              borderLeft: 'solid 8px #479b4e',
              marginBottom: '10px',
              marginTop: '10px',
              marginRight: '20px'
            }}
          >
            <div style={{ fontWeight: 'bold', marginLeft: '4px' }}>
              Healthy Housekeeping Log
            </div>
          </Paper>
          whereas a red tag signifies that there may be an issue with the
          satellite.
          <Paper
            style={{
              marginLeft: '20px',
              borderLeft: 'solid 8px #721c24',
              marginBottom: '10px',
              marginTop: '10px',
              marginRight: '20px'
            }}
          >
            <div style={{ fontWeight: 'bold', marginLeft: '4px' }}>
              Critical Housekeeping Log
            </div>
          </Paper>
          You can also filter housekeeping logs by timestamp using the filter
          options.
        </Typography>
      </Paper>
      <Paper className="Live Commands" style={{ marginBottom: '20px' }}>
        <Typography variant="h5" style={{ padding: '10px' }}>
          Live Commands
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingRight: '20px',
            paddingBottom: '10px'
          }}
        >
          Send telecommands to the satellite via the live commands page.
          Commands are formatted as "prefix.command_name(arg1,arg2,arg3,...) "
          where the number and content of arguments differ for each command. For
          commands with no arguments, the format is "prefix.command_name()". See
          below for a list of valid telecommands.
          <Typography variant="h6" style={{ marginTop: '5px' }}>
            Telecommands:
          </Typography>
          <Typography variant="h7" style={{ marginTop: '5px' }}>
            <strong>command_name</strong>
            <span style={{ fontStyle: 'italic' }}>{' (arguments)'}</span>
          </Typography>
          <Paper
            style={{
              marginTop: '10px',
              marginBottom: '15px',
              maxHeight: '60vh',
              overflow: 'auto',
              borderStyle: 'solid',
              borderColor: 'black'
            }}
          >
            {commands.map((command) =>
              !!command.about_info ? (
                <Typography variant="body1" style={{ paddingLeft: '10px' }}>
                  <strong>{command.command_name.slice(4)}</strong>
                  {command.arg_labels != null ? (
                    <span style={{ fontStyle: 'italic' }}>
                      {' (' + command.arg_labels + ')'}
                    </span>
                  ) : null}
                  {command.about_info != null ? (
                    <p style={{ paddingLeft: '5%' }}>{command.about_info}</p>
                  ) : null}
                  {command.return_labels != null ? (
                    <p style={{ paddingLeft: '5%' }}>
                      {'Returns: ' + command.return_labels}
                    </p>
                  ) : null}
                  <hr></hr>
                </Typography>
              ) : null
            )}
          </Paper>
          The Live Commands page displays any messages sent to or received from
          the satellite communications module. Note that the live commands
          window will only display the commands for the duration you are on the
          page. To view a complete history of the communications with the
          satellite, go to the Logs page. The messages will be from one of a
          username (i.e. a human operator), the satellite ("comm"), or sent as
          part of an automated script ("automation").
        </Typography>
      </Paper>
      <Paper
        className="AutomatedCommandSequence"
        style={{ marginBottom: '20px' }}
      >
        <Typography variant="h5" style={{ padding: '10px' }}>
          Automated Command Sequence
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingBottom: '10px',
            paddingRight: '20px'
          }}
        >
          The Automated Command Sequence page displays a table of the current
          automated command sequence: a list of commands that will automatically
          be sent to the satellite upon the start of a passover. Only admin
          users have the ability to update the sequence. Commands can be added,
          removed, and their order in the sequence updated using the navigation
          tools.
        </Typography>
      </Paper>
      <Paper className="Logs" style={{ marginBottom: '20px' }}>
        <Typography variant="h5" style={{ padding: '10px' }}>
          Logs
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingBottom: '10px',
            paddingRight: '20px'
          }}
        >
          The Logs page displays all of the communications to and from the
          satellite. To update the page, press the Refresh button. All messages
          will be denoted as from one of a username (i.e. a human operator), the
          satellite ("comm"), or sent as part of an automated script
          ("automation"). If a message is queued, it will be sent to the
          satellite during its next passover. Admin users can also de-queue
          messages before they are sent, and re-queue messages after they are
          sent. Non-admin users can also do so, but only for commands they have
          issued.
        </Typography>
      </Paper>
      <Paper className="Timer" style={{ marginBottom: '20px' }}>
        <Typography variant="h5" style={{ padding: '10px' }}>
          Passover Timer
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingBottom: '10px',
            paddingRight: '20px'
          }}
        >
          On the navigation bar, you will see a timer. This denotes when the
          next satellite passover is scheduled. If the timer is yellow, it is
          counting down until the next expected passover. When an expected
          passover begins, the timer will turn green and begin counting up
          signifying how much time has elapsed during the current passover. Once
          a passover ends, the timer will turn yellow again and begin counting
          down until the next passover.
        </Typography>
      </Paper>
      <Paper className="Reset Password" style={{ marginBottom: '20px' }}>
        <Typography variant="h5" style={{ padding: '10px' }}>
          Password Reset
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingBottom: '10px',
            paddingRight: '20px'
          }}
        >
          Using the dropdown from the profile icon, users can reset their
          password.
        </Typography>
      </Paper>
      <Paper className="Manage Users">
        <Typography variant="h5" style={{ padding: '10px' }}>
          Managing Users
        </Typography>
        <Typography
          variant="body1"
          style={{
            paddingLeft: '20px',
            paddingBottom: '10px',
            paddingRight: '20px'
          }}
        >
          Using the dropdown from the profile icon, admin users can register new
          users, as well as manage the users that they have registered. Note
          that admin users cannot be deleted, even by the admin user that
          created them.
        </Typography>
      </Paper>
    </div>
  );
};

export default Help;
