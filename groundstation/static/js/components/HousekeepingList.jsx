import React from 'react'

import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import Paper from '@material-ui/core/Paper';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import Typography from '@material-ui/core/Typography';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import WarningIcon from '@material-ui/icons/Warning';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import { withStyles } from '@material-ui/core/styles';

function modeIcon(status){
	if(status == "Passive" || status == "Active Mission"){
		return <CheckCircleIcon style={{ fill: '#155724' }}/>
	}else{
		return <WarningIcon style={{ fill: '#721c24' }}/>
	}
}

const HousekeepingLogList = (props) => {
	if (props.empty) {
      return (
        <div>
        	<ErrorOutlineIcon /> There is currently no housekeeping data!
        </div>
      )
    }

	return (
		<div>
			{
				<Paper className="grid-containers">
              		<h5>Recent Housekeeping Data</h5>
              
              		{props.housekeeping.map((housekeeping, idx) => (
                		<ExpansionPanel key={housekeeping.name} defaultExpanded={(idx == 0) ? true : false}>
                  			<ExpansionPanelSummary
                    			expandIcon={<ExpandMoreIcon style={{color: '#4bacb8'}} />}
                    			aria-controls="panel1a-content"
                    			id="panel1a-header"
                  			>
                    			<Typography>{housekeeping.lastBeaconTime}</Typography>
                  			</ExpansionPanelSummary>
                  			<ExpansionPanelDetails>
                    			<Table aria-label="simple table">
                      				<TableHead>
                        				<TableRow>
                          					<TableCell style={{backgroundColor: '#000', color: '#fff'}}>ID</TableCell>
                          					<TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Satellite Mode</TableCell>
                          					<TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Battery Voltage</TableCell>
                          					<TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Current In</TableCell>
                          					<TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Current Out</TableCell>
                        				</TableRow>
                      				</TableHead>
                      				<TableBody>
                        				<TableRow>
                          					<TableCell component="th" scope="row">
                            					{housekeeping.id}
                          					</TableCell>
                          					<TableCell align="right">
                          						{modeIcon(housekeeping.satelliteMode)}
                          						<span style={{ marginLeft: '5px' }}>{housekeeping.satelliteMode}</span>
                          					</TableCell>
                          					<TableCell align="right">{housekeeping.batteryVoltage}</TableCell>
                          					<TableCell align="right">{housekeeping.currentIn}</TableCell>
                          					<TableCell align="right">{housekeeping.currentOut}</TableCell>
                        				</TableRow>
                      				</TableBody>
                    			</Table>
                  			</ExpansionPanelDetails>
                		</ExpansionPanel>
              		))}
            	</Paper>
			}
		</div>
	)
};

export default HousekeepingLogList;