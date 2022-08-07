import React, { Component, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import CommunicationsList from './CommunicationsListFull';
import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';


const UserEntry = (props) => {
    const [isEditing, setIsEditing] = useState(false);

    // const divStyle = {
    //     paddingBottom:'1%',
    //     paddingLeft:'1%',
    //     paddingRight:'1%',
    // };
    function editHandler() {
        setIsEditing(true);
    }
    function deleteHandler() {}
    return (
        <div style={{display: 'flex', justifyContent: 'space-between', marginLeft: '2%', marginRight: '2%'}}>
            <div style={{marginTop: '1%'}}>
                <p>Username: {props.user.username}</p>{props.user.is_admin && <p>Admin</p>}
            </div>
            <div>
                <span>
                    <Button style={{marginBottom:"1%"}}
                    color = "primary"
                    onClick={editHandler}
                    variant = 'outlined'>Edit</Button>
                </span>
                {!props.user.is_admin &&
                <span>
                    <Button style={{marginBottom:"1%"}}
                    color = "primary"
                    onClick={deleteHandler}
                    variant = 'outlined'>Delete</Button>
                </span>}
            </div>
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
                    <Paper style={{paddingTop:"1%", paddingBottom:"2%"}}>
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
