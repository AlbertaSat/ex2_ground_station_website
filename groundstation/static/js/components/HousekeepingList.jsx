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
		return <CheckCircleIcon style={{ fill: '#479b4e' }}/>
	}else{
		return <WarningIcon style={{ fill: '#721c24' }}/>
	}
}

function tableColor(status){
  if(status == "Passive" || status == "Active Mission"){
    return {borderLeft: 'solid 8px #479b4e'}
  }else{
    return {border: 'solid 8px #721c24'}
  }
  //#c48b16 Warning
  //#f44336 Danger
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
                		<ExpansionPanel 
                      key={housekeeping.name}
                      defaultExpanded={(idx == 0) ? true : false}
                      style={tableColor(housekeeping.satellite_mode)}
                    >
                  			<ExpansionPanelSummary
                    			expandIcon={<ExpandMoreIcon style={{color: '#4bacb8'}} />}
                    			aria-controls="panel1a-content"
                    			id="panel1a-header"
                  			>
                    			<Typography>{housekeeping.last_beacon_time}</Typography>
                  			</ExpansionPanelSummary>
                  			<ExpansionPanelDetails>
                    			<Table aria-label="simple table">
                      				<TableHead>
                        				<TableRow>
                          					<TableCell 
                                       style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                                       ID
                                    </TableCell>
                          					<TableCell 
                                       align="right" 
                                       style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                                       Satellite Mode
                                    </TableCell>
                          					<TableCell 
                                       align="right" 
                                       style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                                       Battery Voltage
                                    </TableCell>
                          					<TableCell 
                                       align="right" 
                                       style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                                       Current In
                                    </TableCell>
                          					<TableCell 
                                       align="right" 
                                       style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                                       Current Out
                                    </TableCell>
                        				</TableRow>
                      				</TableHead>
                      				<TableBody>
                        				<TableRow>
                          					<TableCell component="th" scope="row">
                            					{housekeeping.id}
                          					</TableCell>
                          					<TableCell align="right">
                          						{modeIcon(housekeeping.satellite_mode)}
                          						<span style={{ marginLeft: '5px' }}>{housekeeping.satellite_mode}</span>
                          					</TableCell>
                          					<TableCell align="right">{housekeeping.battery_voltage}</TableCell>
                          					<TableCell align="right">{housekeeping.current_in}</TableCell>
                          					<TableCell align="right">{housekeeping.current_out}</TableCell>
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