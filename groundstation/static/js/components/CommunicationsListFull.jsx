import React, { useEffect, createRef } from 'react'
import {formatDateToUTCString} from '../helpers.js'


const CommunicationEntry = (props) => {
    const divStyle = {
        paddingBottom:'1%',
        paddingLeft:'1%',
        paddingRight:'1%',
    };
    const contentStyle = {};
    const infoStringStyle = {};

    const sender = props.entry.sender;
    console.log(props.entry)

    let infoStringPrefix;
    let infoTimestamp;

    if (sender === 'comm') {
        divStyle.backgroundColor = '#e3e3e3';
        contentStyle.color = '#007b40';
        infoStringPrefix = 'Message from';
    } else {
        divStyle.backgroundColor = '#f2f2f2';
        contentStyle.color = '#56b2bc';
        infoStringPrefix = 'Input from';
    }

    // this is pre janky but its the way it is
    infoTimestamp = props.entry.timestamp;
    if (infoTimestamp[infoTimestamp.length - 1] !== 'Z') {
        infoTimestamp = infoTimestamp + 'Z';
    }
    infoTimestamp = new Date(infoTimestamp);
    let infoStringTimestamp = formatDateToUTCString(infoTimestamp);

    return (
        <div style={divStyle}>
            <div>
                <p style={infoStringStyle}>{infoStringPrefix} <strong>{sender}</strong> on: </p><p>{infoStringTimestamp}</p>
            </div>
            <p style={contentStyle}>Message: {props.entry.message}</p>
            <p style={contentStyle}>Is Queued: {props.entry.is_queued ? 'true' : 'false'}</p>
        </div>
    );
}


const CommunicationsList = (props) => {
    const divStyle = {margin:'2%'}

    const messagesEndRef = createRef();
    if (props.autoScroll === true) {
        const scrollToBottom = () => {
            messagesEndRef.current.scrollIntoView({behavior: 'smooth'});
        };
        useEffect(scrollToBottom, [props.displayLog]);
    }

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
