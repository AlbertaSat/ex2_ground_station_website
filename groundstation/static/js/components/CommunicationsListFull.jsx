import React from 'react'

const CommunicationEntry = (props) => {
    const divStyle = {
        paddingBottom:'1%',
        paddingLeft:'1%',
        paddingRight:'1%',
    };
    const idStyle = {};
    const messageStyle = {};
    const infoStringStyle = {};

    const sender = props.entry.sender;

    let infoStringPrefix;
    let infoStringTimestamp;
    if (sender === 'comm') {
        divStyle.backgroundColor = '#e3e3e3';
        messageStyle.color = '#007b40';
        infoStringPrefix = 'message from';
        infoStringTimestamp = props.entry.timestamp;
    } else {
        divStyle.backgroundColor = '#f2f2f2';
        messageStyle.color = '#56b2bc';
        infoStringPrefix = 'input from';
        infoStringTimestamp = props.entry.timestamp;
    }
    return (
        <div style={divStyle}>
            <p style={infoStringStyle}>{infoStringPrefix} <strong>{sender}</strong> at {infoStringTimestamp}</p>
            <p style={messageStyle}>Message: {props.entry.message}</p>
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
