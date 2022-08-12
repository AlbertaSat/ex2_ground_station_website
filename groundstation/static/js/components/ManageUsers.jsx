import React, { Component, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import AddCircleIcon from '@material-ui/icons/AddCircle';
import Dialog from '@material-ui/core/Dialog';

const UserEntry = (props) => {
  const [isEditing, setIsEditing] = useState(false);
  const [username, setUsername] = useState(props.user.username);
  const [tempUsername, setTempUsername] = useState(props.user.username);
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  function cancelHandler() {
    setIsDeleteDialogOpen(false);
    setIsEditing(false);
    setUsername(username);
    setTempUsername('');
    setPassword('');
    setError('');
    setSuccess('');
  }

  function openDeleteDialog() {
    setIsDeleteDialogOpen(true);
  }

  function editHandler() {
    setIsEditing(true);
    setTempUsername(username);
    setPassword('');
    setError('');
    setSuccess('');
  }

  function deleteHandler() {
    let auth_token;
    if (!!sessionStorage.getItem('auth_token')) {
      auth_token = sessionStorage.getItem('auth_token');
    }
    if (!!localStorage.getItem('auth_token')) {
      sessionStorage.setItem('auth_token', localStorage.getItem('auth_token'));
      auth_token = localStorage.getItem('auth_token');
    }

    const post_data = {
      id_to_delete: props.user.id
    };
    fetch('/api/users/' + auth_token, {
      method: 'DELETE',
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
        if (data.status == 'success') {
          console.log(data.status);
          setIsDeleteDialogOpen(false);
          setSuccess('');
          setError('');
          props.rerenderList();
        } else {
          console.error('Unexpected error occurred.');
          console.error(data);
          setSuccess('');
          setError('Error occurred. User was not deleted successfully.');
        }
      });
  }

  function handleUsernameChange(event) {
    setTempUsername(event.target.value);
  }

  function handlePasswordChange(event) {
    setPassword(event.target.value);
  }

  function saveHandler() {
    if (password == '') {
      setError('Please enter a password');
      return;
    }
    let auth_token;
    if (!!sessionStorage.getItem('auth_token')) {
      auth_token = sessionStorage.getItem('auth_token');
    }
    if (!!localStorage.getItem('auth_token')) {
      sessionStorage.setItem('auth_token', localStorage.getItem('auth_token'));
      auth_token = localStorage.getItem('auth_token');
    }

    const post_data = {
      username: tempUsername,
      password: password,
      id: props.user.id
    };

    // also when is encode_auth_token called?
    // also drop-down getting too long, maybe remove add users row
    fetch('/api/users/' + auth_token, {
      method: 'PATCH',
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
        if (data.status == 'success') {
          setUsername(tempUsername);
          setTempUsername('');
          setPassword('');
          setError('');
          setIsEditing(false);
          setSuccess('User successfully updated');
        } else {
          console.error('Unexpected error occurred.');
          console.error(data);
          setError(data.message);
          setSuccess('');
        }
      });
  }

  return (
    <div
      style={{
        display: 'flex',
        justifyContent: 'space-between',
        marginBottom: '2%',
        marginLeft: '2%',
        marginRight: '2%',
        marginTop: '2%',
        backgroundColor: 'rgb(242,242,242)',
        alignItems: 'center'
      }}
    >
      <Dialog
        open={isDeleteDialogOpen}
        fullWidth={true}
        focused={true}
        justifyContent="middle"
      >
        <div style={{ padding: '5%', width: 'max-content', margin: 'auto' }}>
          <p>Are you sure you want to delete this user?</p>
        </div>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-evenly',
            paddingBottom: '5%'
          }}
        >
          <span>
            <Button onClick={deleteHandler} variant="outlined" colour="primary">
              Delete
            </Button>
          </span>
          <span>
            <Button onClick={cancelHandler} variant="outlined">
              Cancel
            </Button>
          </span>
        </div>
      </Dialog>
      {!isEditing ? (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <p
            style={{
              marginTop: '2%',
              marginLeft: '5%',
              marginBottom: '1%',
              width: 'min-content'
            }}
          >
            Username: <strong>{username}</strong>
          </p>
        </div>
      ) : (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>
              <TextField
                style={{ width: '95%' }}
                required
                id="outlined-required"
                label="Username"
                name="username"
                margin="normal"
                variant="outlined"
                value={tempUsername}
                onChange={(event) => handleUsernameChange(event)}
                error={!(error === '')}
              />
            </span>
            <span>
              <TextField
                style={{ width: '95%' }}
                required
                id="outlined-required"
                label="New Password"
                name="password"
                margin="normal"
                variant="outlined"
                value={password}
                onChange={(event) => handlePasswordChange(event)}
                error={!(error === '')}
              />
            </span>
          </div>
        </div>
      )}
      {!(error === '') ? (
        <div>
          <Typography style={{ color: 'red', width: 'min-content' }}>
            {error}
          </Typography>
        </div>
      ) : null}
      {!(success === '') ? (
        <div>
          <Typography style={{ color: 'green', width: 'min-content' }}>
            {success}
          </Typography>
        </div>
      ) : null}
      {props.user.is_admin && (
        <div vertical-align="center">
          <p style={{ fontStyle: 'italic' }}>{'(Admin)'}</p>
        </div>
      )}
      {!isEditing ? (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <span>
            <Button color="primary" onClick={editHandler} variant="outlined">
              Edit
            </Button>
          </span>
          {!props.user.is_admin && (
            <span>
              <Button
                color="primary"
                onClick={openDeleteDialog}
                variant="outlined"
              >
                Delete
              </Button>
            </span>
          )}
        </div>
      ) : (
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <span>
            <Button color="primary" onClick={cancelHandler} variant="outlined">
              Cancel
            </Button>
          </span>
          <span>
            <Button color="primary" onClick={saveHandler} variant="outlined">
              Save
            </Button>
          </span>
        </div>
      )}
    </div>
  );
};

class ManageUsers extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      is_empty: false,
      error_message: ''
    };
    this.handleDelete = this.handleDelete.bind(this);
  }

  handleRefresh() {
    const auth_token = sessionStorage.getItem('auth_token');
    fetch('/api/users', { headers: { Authorization: 'Bearer ' + auth_token } })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.status == 'success') {
          this.setState({
            users: data.data.users,
            is_empty: false
          });
        } else {
          console.log('get failed');
          this.setState({
            is_empty: true,
            error_message: 'error fetching users'
          });
        }
      });
  }

  componentDidMount() {
    this.handleRefresh();
  }

  handleDelete() {
    this.handleRefresh();
  }

  handleError() {
    if (!(this.state.error_message === '')) {
      return (
        <div>
          <Typography style={{ color: 'red' }}>
            {this.state.error_message}
          </Typography>
        </div>
      );
    }
  }

  render() {
    return (
      <div>
        {this.handleError()}
        <div style={{ padding: '20px', textAlign: 'center' }}>
          <Typography variant="h4" style={{ color: '#28324C' }}>
            Manage Users
          </Typography>
        </div>

        <div>
          <Button
            style={{
              marginBottom: '1%'
            }}
            color="primary"
            href="/adduser"
            variant="outlined"
          >
            <AddCircleIcon viewBox="-2 -2 30 30"></AddCircleIcon>
            Add User
          </Button>
        </div>

        <div>
          <Paper style={{ paddingTop: '2%', paddingBottom: '2%' }}>
            <div>
              {this.state.users.map((user) => (
                <UserEntry
                  autoScroll={false}
                  user={user}
                  rerenderList={this.handleDelete}
                />
              ))}
            </div>
          </Paper>
        </div>
      </div>
    );
  }
}

export default ManageUsers;
