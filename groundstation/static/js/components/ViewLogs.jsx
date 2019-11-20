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
            isEmpty: false
        }
    }

    handleRefresh(){
        fetch('/api/communications')
            .then( response => {
                return response.json();
            }).then(data => {
                console.log(data);
                if (data.status == 'success'){
                    console.log(data.data)
                    this.setState({messages: data.data.messages})
                    console.log(this.state.messages)
                } else{
                    console.log('get failed')
                }
            });
    }

    componentDidMount(){
        console.log('mounted');
        this.handleRefresh();        
        // fetch('/api/communications')
        //     .then( response => {
        //         return response.json();
        //     }).then(data => {
        //         console.log(data);
        //         if (data.status == 'success'){
        //             console.log(data.data)
        //             this.setState({messages: data.data.messages})
        //             console.log(this.state.messages)
        //         } else{
        //             console.log('get failed')
        //         }
        //     });
    }


    render(){
        // const { classes } = this.props;
        return (
            <div>
                <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                    LOGS
                </Typography>
                <Paper>
                    <CommunicationsList displayLog={this.state.messages} isEmpty={this.state.isEmpty}/>
                    <Button 
                        onClick={ () => this.handleRefresh()}
                        variant="contained"
                    >
                        Refresh
                    </Button>
                </Paper>
            </div>
        );
    }
}

export default Logs;