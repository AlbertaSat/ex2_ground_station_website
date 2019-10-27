import React from 'react'
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

const FlightScheduleList = (props) => {
	return (
       <div>
		<Paper className="grid-containers">
       	  <h5 className="container-text">Upcoming Flight Schedules</h5>
          {props.flightschedule.map(flightschedule => (
             <ExpansionPanel key={flightschedule.id}>
               <ExpansionPanelSummary
                 expandIcon={<ExpandMoreIcon />}
                 aria-controls="panel1a-content"
                 id="panel1a-header"
               >
                  <Table aria-label="simple table">
                    <TableHead>
                      <TableRow>
                        <TableCell style={{backgroundColor: '#000', color: '#fff'}}>ID</TableCell>
                        <TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Creation Date</TableCell>
                        <TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Upload Date</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      <TableRow>
                        <TableCell component="th" scope="row">
                          {flightschedule.id}
                        </TableCell>
                        <TableCell align="right">{flightschedule.creationDate}</TableCell>
                        <TableCell align="right">{flightschedule.uploadDate}</TableCell>
                      </TableRow>
                    </TableBody>
                  </Table>
                </ExpansionPanelSummary>
                <ExpansionPanelDetails>
                  <Table aria-label="simple table">
                    <TableHead>
                      <TableRow>
                        <TableCell style={{backgroundColor: '#000', color: '#fff'}}>ID</TableCell>
                        <TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Command Name</TableCell>
                        <TableCell align="right" style={{backgroundColor: '#000', color: '#fff'}}>Time Stamp</TableCell>
                      </TableRow>
                    </TableHead>
                    {flightschedule.commands.map(commands => (
                      <TableBody>
                        <TableRow>
                          <TableCell component ="th" scope="row">
                            {commands.commandId}
                          </TableCell>
                          <TableCell align="right">{commands.commandName}</TableCell>
                          <TableCell align="right">{commands.timeStamp}</TableCell>
                        </TableRow>
                      </TableBody>
                    ))} 
                   </Table>
                  </ExpansionPanelDetails>
                </ExpansionPanel>
              ))}
            </Paper>
          </div>
	)
}

export default FlightScheduleList;