import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import CommunicationsList from './CommunicationsListFull';
import Button from '@material-ui/core/Button';
import RefreshIcon from '@material-ui/icons/Refresh';

class Logs extends Component {
    constructor(){
        super();
        this.state = {
            messages: [],
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
                        error_message: 'error fetching messages: '+ data.message
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
                        onClick={ () => this.handleRefresh()}
                        variant="outlined">
                    <RefreshIcon></RefreshIcon>
                    Refresh
                    </Button>
                </div>
                <div>
                    <Paper style={{paddingTop:"1%", paddingBottom:"2%"}}>
                        <CommunicationsList autoScroll={false} displayLog={this.state.messages} isEmpty={this.state.is_empty}/>
                    </Paper>
                </div>
            </div>
        );
    }
}

export default Logs;
