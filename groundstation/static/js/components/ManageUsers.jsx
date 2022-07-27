import React, { Component, useState } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import CommunicationsList from './CommunicationsListFull';
import Button from '@material-ui/core/Button';
import AddCircleIcon from '@material-ui/icons/AddCircle';


const UserEntry = (props) => {
    const [isEditing, setIsEditing] = useState(false);

    const divStyle = {};

    return (
        <div style={divStyle}>
            <p> <span>Username: {props.user.username}</span> {props.user.is_admin && <span margin-right = "0%">Admin</span>}</p>
            <p>Password: {props.user.password}</p>
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
        fetch('/api/communications?newest-first=true')
            .then( response => {
                return response.json();
            }).then(data => {
                if (data.status == 'success'){
                    this.setState({
                        messages: data.data.messages,
                        is_empty: false
                    })
                } else{

                    console.log('get failed')
                    this.setState({
                        is_empty: true,
                        error_message: 'error fetching messages: ' + data.message
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
                    <AddCircleIcon></AddCircleIcon>
                    Add User
                    </Button>
                </div>
                <div>
                    <Paper style={{paddingTop:"1%", paddingBottom:"2%"}}>
                        <UserEntry autoScroll={false} displayUsers={this.state.users} isEmpty={this.state.is_empty}/>
                    </Paper>
                </div>
            </div>
        );
    }
}

export default ManageUsers;
