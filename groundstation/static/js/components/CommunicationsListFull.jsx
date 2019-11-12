import React from 'react'
// import Paper from '@material-ui/core/Paper';

const CommunicationEntry = (props) => {
    // const output = JSON.stringify(props.entry, null, 4);
    const divStyle = {color:'green'};
    if (props.entry.type === 'user-input') {
        divStyle.color = 'red';
    }
    return (
        <div>
            <p style={divStyle}>{props.entry.data.message}</p>
        </div>
    );
}


const CommunicationsList = (props) => {
	if (props.isEmpty) {
      return (
        <div>
        	No Messages to display
        </div>
      )
    }

	return (
        <div>
            {props.displayLog.map(logEntry => (
                <CommunicationEntry entry={logEntry}/>
            ))}
        </div>
    );
}

export default CommunicationsList;
