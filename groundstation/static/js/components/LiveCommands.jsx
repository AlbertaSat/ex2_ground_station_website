import React, { Component } from 'react';
import CommunicationsList from './CommunicationsListFull';
import Paper from '@material-ui/core/Paper';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import LinearProgress from '@material-ui/core/LinearProgress';
import Typography from '@material-ui/core/Typography';
import { Checkbox, FormControlLabel, FormGroup } from '@material-ui/core';
import Select from 'react-select';

// Taken from ex2_ground_station_software/src/groundStation/system.py
const SAT_PREFIX = [
  { value: 'ex2', label: 'EX2' },
  { value: 'yuk', label: 'YUK' },
  { value: 'ari', label: 'ARI' },
  { value: 'eps', label: 'EPS' }
];

const satCliStyles = {
  control: (provided, state) => ({
    ...provided,
    width: '128px'
  })
};

function getNewMessages(last_id, ignore) {
  var new_messages = new Promise((resolve, reject) => {
    fetch('/api/communications?last_id=' + last_id + '&ignore_sender=' + ignore)
      .then((results) => {
        return results.json();
      })
      .then((data) => {
        if (data.status == 'success') {
          resolve(data.data.messages);
        } else {
          resolve([]);
        }
      });
  });
  return new_messages;
}

class LiveCommands extends Component {
  constructor(props) {
    super(props);
    this.state = {
      splashJobsLeft: 2,
      isEmpty: false,
      validTelecommands: [],
      last_id: undefined,
      errorMessage: '',
      textBoxValue: '',
      displayLog: [],
      isSatCli: false,
      currentSatCli: {
        value: 'ex2',
        label: 'EX2'
      }
    };
    this.handleChangeCommand = this.handleChangeCommand.bind(this);
    this.handleToggleSatCli = this.handleToggleSatCli.bind(this);
    this.handleChangeSatCli = this.handleChangeSatCli.bind(this);
    this.formatToSatCliCommand = this.formatToSatCliCommand.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
    this.telecommandIsValid = this.telecommandIsValid.bind(this);
    this.updateMessages = this.updateMessages.bind(this);
  }

  componentDidMount() {
    fetch('/api/telecommands', {
      headers: {
        Authorization: 'Bearer ' + sessionStorage.getItem('auth_token')
      }
    })
      .then((results) => {
        return results.json();
      })
      .then((data) => {
        if (data.status == 'success') {
          this.setState((prevState) => ({
            validTelecommands: data.data.telecommands,
            isEmpty: false,
            splashJobsLeft: prevState.splashJobsLeft - 1
          }));
        } else {
          console.error('Error loading telecommands!');
          console.error(data);
        }
      });
    fetch('/api/communications?max=true', {
      headers: {
        Authorization: 'Bearer ' + sessionStorage.getItem('auth_token')
      }
    })
      .then((results) => {
        return results.json();
      })
      .then((data) => {
        if (data.status == 'success') {
          const max_message = data.data.messages[0];
          let max_message_id;
          if (max_message !== undefined) {
            max_message_id = max_message.message_id;
          } else {
            max_message_id = -1;
          }
          this.setState((prevState) => ({
            last_id: max_message_id,
            splashJobsLeft: prevState.splashJobsLeft - 1
          }));
        } else {
          console.error('Unexpected error occured:');
          console.error(data);
        }
      });
    this.poll_timer = setInterval(() => this.updateMessages(), 1000);
  }

  componentWillUnmount() {
    clearInterval(this.poll_timer);
  }

  updateMessages() {
    if (this.state.splashJobsLeft > 0) {
      console.log('splash jobs left!');
      return;
    }
    getNewMessages(this.state.last_id, sessionStorage.getItem('username')).then(
      (new_messages) => {
        let last_message = new_messages[new_messages.length - 1];
        if (last_message !== undefined) {
          // let displayable_messages = new_messages.map(message => ({type:'server-message', data:message}))
          this.setState((prevState) => ({
            displayLog: [...prevState.displayLog, ...new_messages],
            last_id: last_message.message_id
          }));
        }
      }
    );
  }

  telecommandIsValid(telecommand_string) {
    // sat_cli commands act like bash commands so they bypass validation
    if (this.state.isSatCli) return true;

    const str = telecommand_string.trim();

    // Check for matching closing ')'
    const openIndex = str.indexOf('(');
    if (openIndex === -1) {
      return false;
    }
    const closeIndex = str.indexOf(')');
    if (closeIndex === -1 || closeIndex !== str.length - 1) {
      return false;
    }

    // Check if command name is valid
    const command_name = str.substring(0, openIndex);
    const matching_command = this.state.validTelecommands.find((element) => {
      if (element.command_name === command_name) {
        return element;
      }
    });
    if (matching_command === undefined) {
      return false;
    }

    // Check if command has the correct number of arguments
    const args =
      openIndex + 1 === closeIndex
        ? [] // Prevents [""] which has length 1
        : str.substring(openIndex + 1, closeIndex).split(',');
    if (matching_command.num_arguments !== args.length) {
      return false;
    }

    return true;
  }

  handleChangeCommand(event) {
    this.setState({ textBoxValue: event.target.value });
  }

  handleToggleSatCli(event) {
    this.setState({ isSatCli: event.target.checked });
  }

  handleChangeSatCli(event) {
    this.setState({
      currentSatCli: {
        value: event.value,
        label: event.label
      }
    });
  }

  formatToSatCliCommand(text) {
    return `${this.state.currentSatCli.value}.cli.send_cmd(${text.length},${text})`;
  }

  handleKeyPress(event) {
    if (event.key === 'Enter') {
      const text = event.target.value;
      if (this.telecommandIsValid(text)) {
        const post_data = {
          timestamp: new Date(Date.now()).toISOString(),
          message: this.state.isSatCli
            ? this.formatToSatCliCommand(text)
            : text,
          sender: sessionStorage.getItem('username'),
          receiver: 'comm',
          is_queued: true
        };

        fetch('/api/communications', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer ' + sessionStorage.getItem('auth_token')
          },
          body: JSON.stringify(post_data)
        })
          .then((results) => {
            return results.json();
          })
          .then((data) => {
            if (data.status === 'success') {
              this.setState((prevState) => ({
                displayLog: [...prevState.displayLog, data.data],
                errorMessage: '',
                textBoxValue: ''
              }));
            } else {
              console.error('Unexpected error occured:');
              console.error(data);
            }
          });
      } else {
        this.setState({ errorMessage: 'Invalid Telecommand' });
      }
    } else if (event.key === 'ArrowUp') {
      // TODO (nice to have): Next level: store input history for easy re-send
      console.log(event.key);
    } else if (event.key === 'ArrowDown') {
      console.log(event.key);
    }
  }

  render() {
    if (this.state.splashJobsLeft > 0) {
      return (
        <div>
          <LinearProgress />
        </div>
      );
    }
    return (
      <div>
        <div>
          <Paper style={{ height: '70%', overflow: 'auto' }}>
            <Typography
              className="header-title"
              variant="h5"
              style={{ padding: '10px', margin: '20px' }}
            >
              Live Commands
            </Typography>
            <CommunicationsList
              autoScroll={true}
              displayLog={this.state.displayLog}
              isEmpty={this.state.isEmpty}
              showQueueButton={false}
            />
          </Paper>
        </div>
        <div>
          <TextField
            id="user-input-textbox"
            label="Enter Telecommand"
            margin="normal"
            variant="outlined"
            style={{ width: '100%', backgroundColor: 'white' }}
            value={this.state.textBoxValue}
            onChange={(event) => this.handleChangeCommand(event)}
            onKeyDown={(event) => this.handleKeyPress(event)}
            error={!(this.state.errorMessage === '')}
          />
        </div>
        <FormGroup row>
          <FormControlLabel
            control={
              <Checkbox
                checked={this.state.isSatCli}
                onChange={this.handleToggleSatCli}
              />
            }
            label="Send as CLI command to:"
          />
          <Select
            className="basic-single"
            classNamePrefix="select"
            menuPlacement="top"
            options={SAT_PREFIX}
            value={this.state.currentSatCli}
            onChange={this.handleChangeSatCli}
            styles={satCliStyles}
          />
        </FormGroup>
      </div>
    );
  }
}

export default LiveCommands;
