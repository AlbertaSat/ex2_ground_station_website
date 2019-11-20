import React, { Component } from 'react';
import Typography from '@material-ui/core/Typography';

class Logs extends Component {
    constructor(){
        super();
        this.state = {
        }
    }


    render(){
        console.log('test')
        return (
            <div>
                <Typography variant="h4" displayInline style={{color: '#28324C'}}>
                    LOGS
                </Typography>
            </div>
        );
    }
}

export default Logs;