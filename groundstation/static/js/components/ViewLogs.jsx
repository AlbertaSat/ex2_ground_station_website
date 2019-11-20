import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import CommunicationsList from './CommunicationsListFull';
import Button from '@material-ui/core/Button';

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
        fetch('/api/communications')
            .then( response => {
                return response.json();
            }).then(data => {
                console.log(data);
                if (data.status == 'success'){
                    // console.log(data.data)
                    this.setState({
                        messages: data.data.messages,
                        is_empty: false
                    })
                    // console.log(this.state.messages)
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
                <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                    LOGS
                </Typography>
                <CommunicationsList displayLog={this.state.messages} isEmpty={this.state.is_empty}/>       
                {this.handleError()}
                <Button 
                    onClick={ () => this.handleRefresh()}
                    variant="contained"
                >
                    Refresh
                </Button>
            </div>
        );
    }
}

export default Logs;