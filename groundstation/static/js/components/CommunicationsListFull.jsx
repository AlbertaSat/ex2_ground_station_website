import React from 'react'

const CommunicationEntry = (props) => {
    const divStyle = {
        paddingBottom:'1%',
        paddingLeft:'1%',
        paddingRight:'1%',
    };
    const idStyle = {};
    const messageStyle = {};
    const timestampStyle = {};
    const senderStyle = {};
    const receiverStyle = {};

    const type = props.entry.type;
    const data = props.entry.data;
    let timestampString;
    if (type === 'user-input') {
        divStyle.backgroundColor = '#f2f2f2';
        messageStyle.color = 'red';
        timestampString = type + ' at ' + data.timestamp;
    } else {
        divStyle.backgroundColor = '#e3e3e3';
        messageStyle.color = 'green';
        timestampString = type + ' from ' + data.timestamp;
    }
    console.log(timestampString)
    return (
        <div style={divStyle}>
            <p style={timestampStyle}>{timestampString}</p>
            <p style={messageStyle}>Message: {data.message}</p>
        </div>
    );
}


const CommunicationsList = (props) => {
    const divStyle = {margin:"2%"}
	if (props.isEmpty) {
      return (
        <div style={divStyle}>
        	No Messages to display
        </div>
      )
    }
	return (
        <div style={divStyle}>
            {props.displayLog.map(logEntry => (
                <CommunicationEntry entry={logEntry}/>
            ))}
        </div>
    );
}

export default CommunicationsList;
