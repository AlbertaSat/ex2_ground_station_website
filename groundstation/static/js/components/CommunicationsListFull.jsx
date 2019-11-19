import React, { useEffect, createRef } from 'react'


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
        infoStringPrefix = 'Message from';
    } else {
        divStyle.backgroundColor = '#f2f2f2';
        messageStyle.color = '#56b2bc';
        infoStringPrefix = 'Input from';
    }

    // this is pre janky but its the way it is
    infoStringTimestamp = props.entry.timestamp;
    if (infoStringTimestamp[infoStringTimestamp.length - 1] !== 'Z') {
        infoStringTimestamp = infoStringTimestamp + 'Z';
    }
    infoStringTimestamp = new Date(infoStringTimestamp).toString();
    return (
        <div style={divStyle}>
            <div>
                <p style={infoStringStyle}>{infoStringPrefix} <strong>{sender}</strong> on: </p><p>{infoStringTimestamp}</p>
            </div>
            <p style={messageStyle}>Message: {props.entry.message}</p>
        </div>
    );
}


const CommunicationsList = (props) => {
    const divStyle = {margin:"2%"}

    const messagesEndRef = createRef();
    const scrollToBottom = () => {
        messagesEndRef.current.scrollIntoView({behavior: "smooth"});
    };
    useEffect(scrollToBottom, [props.displayLog]);


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
            <div ref={messagesEndRef} />
        </div>
    );
}

export default CommunicationsList;
