import React, { Component, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import CommunicationsList from './CommunicationsListFull';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import AddCircleIcon from '@material-ui/icons/AddCircle';



const UserEntry = (props) => {
    const [isEditing, setIsEditing] = useState(false);
    const [username, setUsername] = useState(props.user.username);
    const [password, setPassword] = useState('');
    const [error, setError] = useState('')

    // const divStyle = {
    //     paddingBottom:'1%',
    //     paddingLeft:'1%',
    //     paddingRight:'1%',
    // };
    function editHandler() {
        setIsEditing(true);
    }
    function deleteHandler() {}

    function handleUsernameChange(event) {setUsername(event.target.value)}

    function handlePasswordChange(event) {setPassword(event.target.value)}

    function saveHandler() {
        let auth_token
        if (!!sessionStorage.getItem('auth_token')) {
            auth_token = sessionStorage.getItem('auth_token');
        }
        if (!!localStorage.getItem('auth_token')) {
            sessionStorage.setItem('auth_token', localStorage.getItem('auth_token'));
            auth_token = localStorage.getItem('auth_token');
          }

        const post_data = {
            password: password
        }
        // right now the patch endpoint patches logged-in user using auth token
        // how to patch any user??
        // also when is encode_auth_token called?
        fetch('/api/users/' + auth_token, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':'Bearer '+ sessionStorage.getItem('auth_token')
              },
            body: JSON.stringify(post_data),
        }).then(results => {
            return results.json();
        }).then(data => {
            if (data.status == 'success') {
                setUsername('');
                setPassword('');
                setError('');
                setIsEditing(false);
            } else {
                console.error('Unexpected error occurred.');
                console.error(data);
                setError("Error occurred. User was not updated successfully.")
            }
        })

    }

    return (
        <div style={{display: 'flex', justifyContent: 'space-between', marginLeft: '2%', marginRight: '2%'}}>
            {!isEditing ? 
            <div style={{marginTop: '1%'}}>
                <p>Username: {props.user.username}</p>{props.user.is_admin && <p>Admin</p>}
            </div>:
            <div>
                <div style={{display: 'flex', justifyContent: 'space-between'}}>
                    <span>
                        <TextField
                                    style={{width: "95%"}}
                                    required
                                    id="outlined-required"
                                    label="Username"
                                    name="username"
                                    margin="normal"
                                    variant="outlined"
                                    value={username}
                                    onChange={(event) => handleUsernameChange(event)}
                                    error={!(error === '')}/>
                    </span>
                    <span>
                    <TextField
                                style={{width: "95%"}}
                                required
                                id="outlined-required"
                                label="New Password"
                                name="password"
                                margin="normal"
                                variant="outlined"
                                value={password}
                                onChange={(event) => handlePasswordChange(event)}
                                error={!(error === '')}/>
                    </span>
                </div>
            </div>}
            {!(error === '') ? 
                <div>
                    <Typography style={{color: 'red'}}>
                        {error}
                    </Typography>
                </div>: null}
            {!isEditing ? 
            <div style={{display: 'flex', justifyContent: 'space-between'}}>
                <span>
                    <Button style={{marginBottom:"1%", width: "70%"}}
                    color = "primary"
                    onClick={editHandler}
                    variant = 'outlined'>Edit</Button>
                </span>
                {!props.user.is_admin &&
                <span>
                    <Button style={{marginBottom:"1%", width: "85%"}}
                    color = "primary"
                    onClick={deleteHandler}
                    variant = 'outlined'>Delete</Button>
                </span>}
            </div>:
            <div>
                <span>
                    <Button style={{marginTop:"30%",marginBottom:"1%"}}
                    color = "primary"
                    onClick={saveHandler}
                    variant = 'outlined'>Save</Button>
                </span>
            </div>}
        </div>
    )
}

class ManageUsers extends Component {
    constructor(){
        super();
        this.state = {
            users: [],
            is_empty: false,
            error_message: ''
        }
    }

    handleRefresh(){
        const auth_token = sessionStorage.getItem('auth_token');
        fetch('/api/users', {headers: {'Authorization':'Bearer '+ auth_token}})
            .then( response => {
                return response.json();
            }).then(data => {
                if (data.status == 'success'){
                    this.setState({
                        users: data.data.users,
                        is_empty: false
                    })
                } else{

                    console.log('get failed')
                    this.setState({
                        is_empty: true,
                        //error_message: 'error fetching messages: ' + data.message
                        error_message: 'error fetching users'
                    })
                }
            });
    }

    componentDidMount(){
        this.handleRefresh();
    }

    handleError(){
        if (!(this.state.error_message === '')){
            return  (
                <div>
                    <Typography style={{color: 'red'}}>
                        {this.state.error_message}
                    </Typography>
                </div>
            );
        }
    }

    render(){
        // const { classes } = this.props;
        return (
            <div>
                {this.handleError()}
                <div>
                    <Button
                        style={{
                            marginBottom:"1%"
                        }}
                        color="primary"
                        href = "/adduser"
                        variant="outlined">
                    <AddCircleIcon viewBox="-2 -2 30 30"></AddCircleIcon>
                    Add User
                    </Button>
                </div>
                <div>
                    <Paper style={{paddingTop:"2%", paddingBottom:"2%"}}>
                        <div>
                            {this.state.users.map(user => (
                            <UserEntry autoScroll={false} user={user}/>
                            ))}
                        </div>
                    </Paper>
                </div>
            </div>
        );
    }
}

export default ManageUsers;
