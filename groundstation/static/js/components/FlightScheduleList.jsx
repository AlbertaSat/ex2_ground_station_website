import React from 'react'
import ErrorOutlineIcon from '@material-ui/icons/ErrorOutline';
import ExpansionPanel from '@material-ui/core/ExpansionPanel';
import ExpansionPanelSummary from '@material-ui/core/ExpansionPanelSummary';
import ExpansionPanelDetails from '@material-ui/core/ExpansionPanelDetails';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import DeleteIcon from '@material-ui/icons/Delete';
import EditIcon from '@material-ui/icons/Edit';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import LinearProgress from '@material-ui/core/LinearProgress';
import Button from '@material-ui/core/Button';

const FlightScheduleList = (props) => {
  if (props.isLoading) {
      return (
        <div>
          <LinearProgress />
        </div>
      )
  }
  if (props.empty && !props.isLoading) {
    return (
      <div>
        <ErrorOutlineIcon /> There are no flightschedules!
      </div>
    )
  }


  function tableColour(status){
    if(status == 3){
      return {borderLeft: 'solid 8px #479b4e'}
    }else if(status == 1){
      return {borderLeft: 'solid 8px #4bacb8'}
    }else if(status == 2){
      return {borderLeft: 'solid 8px #A9A9A9'}
    }
  }

  // format what our status div will look like
  function statusDiv(status){
    if(status == 3){
      return <div style={{fontSize: '14px', color: '#479b4e'}}>Uploaded</div>
    }else if(status == 1){
      return <div style={{fontSize: '14px', color: '#4bacb8'}}>Queued</div>
    }else if(status == 2){
      return <div style={{fontSize: '14px', color: '#A9A9A9'}}>Draft</div>
    }
  }

	return (
    <div>
      {props.flightschedule.map((flightschedule, idx) => (
        <ExpansionPanel key={flightschedule.flightschedule_id} style={tableColour(flightschedule.status)}>
          <ExpansionPanelSummary
            expandIcon={<ExpandMoreIcon style={{ color: '#4bacb8'}}/>}
            aria-controls="panel1a-content"
            id="panel1a-header"
          >
            <Table aria-label="simple table">
              <TableBody>
                <TableRow>
                  <TableCell component="th" scope="row">
                    <div style={{fontWeight: 'bold'}}>
                      {"Flight Schedule #" + flightschedule.flightschedule_id}
                    </div>
                    { statusDiv(flightschedule.status) }
                  </TableCell>
                  <TableCell align="right">
                    {"Created at " + flightschedule.creation_date.split('.')[0]}
                  </TableCell>
                  {
                    !props.isMinified && 
                        <TableCell align="right" style={{minWidth: '126px'}}>
                        {flightschedule.status != 3 &&
                          <div>
                            <Button
                              onClick={ (event) => props.handleEditCommandClick(event, idx, 
                                                    flightschedule.flightschedule_id) }
                              >
                                <EditIcon 
                                  display='none'
                                  style={{ color: '#4bacb8' }}
                                />
                            </Button>
                            <Button
                              onClick={ (event) => props.handleDeleteFlightOpenClick(event, idx,
                                                  flightschedule.flightschedule_id)}
                            >
                                <DeleteIcon 
                                  style={{ color: '#4bacb8'}}
                                />
                            </Button>
                          </div>
                        }
                        </TableCell>
                  }
                </TableRow>
              </TableBody>
            </Table>
          </ExpansionPanelSummary>
          <ExpansionPanelDetails>
            <Table aria-label="simple table">
                <TableHead>
                  <TableRow>
                      <TableCell 
                        style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                          Command
                    </TableCell>
                    <TableCell 
                      align="left"
                      style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                        Arguments
                    </TableCell>
                    <TableCell 
                        align="right"
                        style={{backgroundColor: '#212529', color: '#fff', paddingTop: '8px', paddingBottom: '8px'}}>
                          Timestamp
                    </TableCell>
                  </TableRow>
                </TableHead>
              {flightschedule.commands.map(commands => (
                <TableBody>
                  <TableRow>
                    <TableCell component ="th" scope="row">
                      {commands.command.command_name}
                    </TableCell>
                    <TableCell align="left">
                      {commands.args.map(arg => (
                        arg.argument)).join(', ')}
                    </TableCell>
                    <TableCell align="right">{commands.timestamp}</TableCell>
                  </TableRow>
                </TableBody>
              ))} 
              </Table>
            </ExpansionPanelDetails>
          </ExpansionPanel>
        ))}

    </div>
	)
}

export default FlightScheduleList;